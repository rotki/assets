#!/usr/bin/env python3
"""Backfill missing EVM asset deployment timestamps in an updates SQL file.

Explorer results are preferred when available. The keyless fallback finds the
first block containing contract code through batched archive-RPC binary search.
Successful timestamps are cached, making later runs deterministic and offline.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

EVM_ROW_PATTERN = re.compile(
    r"evm_tokens\([^)]*\)\s+VALUES\('([^']+)',\s*'A',\s*(\d+),\s*'([^']+)'",
    re.IGNORECASE,
)
STARTED_PATTERN = re.compile(
    r"(common_asset_details\([^)]*\)\s+VALUES\('[^']+',\s*'[^']*',\s*[^,]*,"
    r"\s*[^,]*,\s*NULL,\s*)NULL(,\s*NULL\);)",
    re.IGNORECASE,
)
ARCHIVE_RPC_URLS = {
    1: ["https://eth-mainnet.public.blastapi.io", "https://eth.blockrazor.xyz"],
    10: ["https://optimism-mainnet.public.blastapi.io", "https://mainnet.optimism.io"],
    56: ["https://bsc-mainnet.public.blastapi.io"],
    100: ["https://gnosis-mainnet.public.blastapi.io", "https://rpc.gnosischain.com"],
    137: ["https://polygon-mainnet.public.blastapi.io", "https://polygon.drpc.org"],
    146: ["https://rpc.soniclabs.com"],
    8453: ["https://base-mainnet.public.blastapi.io", "https://base.llamarpc.com"],
    42161: ["https://arbitrum-one.public.blastapi.io", "https://arb1.arbitrum.io/rpc"],
    43114: [
        "https://ava-mainnet.public.blastapi.io/ext/bc/C/rpc",
        "https://api.avax.network/ext/bc/C/rpc",
    ],
}
ROUTESCAN_CREATION_CHAINS = {43114}


@dataclass(frozen=True)
class MissingStarted:
    identifier: str
    chain_id: int
    address: str

    @property
    def cache_key(self) -> str:
        return f"{self.chain_id}:{self.address.lower()}"


def parse_missing_started(sql_text: str) -> list[MissingStarted]:
    rows: list[MissingStarted] = []
    for chunk in sql_text.split("\n*\n"):
        if not STARTED_PATTERN.search(chunk):
            continue
        if match := EVM_ROW_PATTERN.search(chunk):
            identifier, chain_id, address = match.groups()
            rows.append(MissingStarted(identifier, int(chain_id), address))
    return rows


def load_cache(path: Path) -> dict[str, int]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text())
    return {str(key): int(value) for key, value in data.items() if isinstance(value, int)}


def save_cache(path: Path, cache: dict[str, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(f"{path.suffix}.tmp")
    temporary.write_text(json.dumps(dict(sorted(cache.items())), indent=2) + "\n")
    temporary.replace(path)


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'\""))


def blockscout_pro_timestamps(
        session: requests.Session,
        chain_id: int,
        rows: list[MissingStarted],
        api_key: str,
) -> dict[str, int]:
    found: dict[str, int] = {}
    for row_chunk in chunked(rows, 10):
        response = session.get(
            "https://api.blockscout.com/v2/api",
            params={
                "chain_id": chain_id,
                "module": "contract",
                "action": "getcontractcreation",
                "contractaddresses": ",".join(row.address for row in row_chunk),
                "apikey": api_key,
            },
            timeout=60,
        )
        response.raise_for_status()
        payload = response.json()
        result = payload.get("result") or []
        if not isinstance(result, list):
            continue
        by_address = {
            str(item.get("contractAddress") or "").lower(): item
            for item in result
            if isinstance(item, dict)
        }
        for row in row_chunk:
            item = by_address.get(row.address.lower())
            if not item:
                continue
            timestamp = item.get("timestamp")
            if isinstance(timestamp, str) and timestamp.isdigit():
                found[row.cache_key] = int(timestamp)
            elif isinstance(timestamp, int):
                found[row.cache_key] = timestamp
    return found


def routescan_creation_transactions(
        session: requests.Session,
        chain_id: int,
        rows: list[MissingStarted],
) -> dict[str, str]:
    if chain_id not in ROUTESCAN_CREATION_CHAINS:
        return {}
    found: dict[str, str] = {}
    for row_chunk in chunked(rows, 10):
        response = session.get(
            f"https://api.routescan.io/v2/network/mainnet/evm/{chain_id}/etherscan/api",
            params={
                "module": "contract",
                "action": "getcontractcreation",
                "contractaddresses": ",".join(row.address for row in row_chunk),
            },
            timeout=60,
        )
        response.raise_for_status()
        result = response.json().get("result") or []
        by_address = {
            str(item.get("contractAddress") or "").lower(): item
            for item in result
            if isinstance(item, dict)
        }
        for row in row_chunk:
            item = by_address.get(row.address.lower())
            if item and isinstance(tx_hash := item.get("txHash"), str) and tx_hash:
                found[row.cache_key] = tx_hash
    return found


def rpc_batch(
        session: requests.Session,
        rpc_url: str,
        calls: list[tuple[str, list[Any]]],
        retries: int = 5,
) -> list[Any]:
    payload = [
        {"jsonrpc": "2.0", "id": index, "method": method, "params": params}
        for index, (method, params) in enumerate(calls)
    ]
    for attempt in range(retries):
        try:
            response = session.post(rpc_url, json=payload, timeout=60)
            if response.status_code in {429, 500, 502, 503, 504}:
                raise requests.HTTPError(response=response)
            response.raise_for_status()
            raw = response.json()
            items = raw if isinstance(raw, list) else [raw]
            by_id = {int(item["id"]): item for item in items if "id" in item}
            results = []
            for index in range(len(calls)):
                item = by_id.get(index, {})
                if error := item.get("error"):
                    raise RuntimeError(str(error))
                results.append(item.get("result"))
            return results
        except (requests.RequestException, RuntimeError, ValueError):
            if attempt + 1 == retries:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError(f"RPC batch failed: {rpc_url}")


def chunked(items: list[Any], size: int) -> list[list[Any]]:
    return [items[index:index + size] for index in range(0, len(items), size)]


def discover_first_code_blocks(
        session: requests.Session,
        rpc_url: str,
        rows: list[MissingStarted],
        batch_size: int,
) -> dict[str, int]:
    latest_raw = rpc_batch(session, rpc_url, [("eth_blockNumber", [])])[0]
    latest_block = int(latest_raw, 16)
    bounds = {row.cache_key: [0, latest_block] for row in rows}
    by_key = {row.cache_key: row for row in rows}

    latest_calls = [("eth_getCode", [row.address, "latest"]) for row in rows]
    latest_results: list[Any] = []
    for calls in chunked(latest_calls, batch_size):
        latest_results.extend(rpc_batch(session, rpc_url, calls))
    active = {
        row.cache_key
        for row, code in zip(rows, latest_results, strict=True)
        if isinstance(code, str) and code not in {"0x", "0x0", ""}
    }

    while any(bounds[key][0] < bounds[key][1] for key in active):
        pending = [key for key in active if bounds[key][0] < bounds[key][1]]
        calls = []
        mids = []
        for key in pending:
            low, high = bounds[key]
            mid = (low + high) // 2
            calls.append(("eth_getCode", [by_key[key].address, hex(mid)]))
            mids.append(mid)
        results: list[Any] = []
        for call_chunk in chunked(calls, batch_size):
            results.extend(rpc_batch(session, rpc_url, call_chunk))
        for key, mid, code in zip(pending, mids, results, strict=True):
            if isinstance(code, str) and code not in {"0x", "0x0", ""}:
                bounds[key][1] = mid
            else:
                bounds[key][0] = mid + 1
    return {key: bounds[key][0] for key in active}


def timestamps_for_blocks(
        session: requests.Session,
        rpc_url: str,
        blocks: dict[str, int],
        batch_size: int,
) -> dict[str, int]:
    unique_blocks = sorted(set(blocks.values()))
    calls = [("eth_getBlockByNumber", [hex(block), False]) for block in unique_blocks]
    results: list[Any] = []
    for call_chunk in chunked(calls, batch_size):
        results.extend(rpc_batch(session, rpc_url, call_chunk))
    block_timestamps = {
        block: int(result["timestamp"], 16)
        for block, result in zip(unique_blocks, results, strict=True)
        if isinstance(result, dict) and result.get("timestamp")
    }
    return {
        key: block_timestamps[block]
        for key, block in blocks.items()
        if block in block_timestamps
    }


def timestamps_for_transactions(
        session: requests.Session,
        rpc_url: str,
        transactions: dict[str, str],
        batch_size: int,
) -> dict[str, int]:
    items = list(transactions.items())
    calls = [("eth_getTransactionByHash", [tx_hash]) for _key, tx_hash in items]
    results: list[Any] = []
    for call_chunk in chunked(calls, batch_size):
        results.extend(rpc_batch(session, rpc_url, call_chunk))
    blocks = {
        key: int(result["blockNumber"], 16)
        for (key, _tx_hash), result in zip(items, results, strict=True)
        if isinstance(result, dict) and result.get("blockNumber")
    }
    return timestamps_for_blocks(session, rpc_url, blocks, batch_size)


def discover_chain_timestamps(
        session: requests.Session,
        rows: list[MissingStarted],
        batch_size: int,
        blockscout_api_key: str | None,
) -> tuple[dict[str, int], str | None]:
    chain_id = rows[0].chain_id
    found: dict[str, int] = {}
    if blockscout_api_key:
        try:
            found.update(blockscout_pro_timestamps(
                session,
                chain_id,
                rows,
                blockscout_api_key,
            ))
        except (requests.RequestException, ValueError):
            pass
    remaining = [row for row in rows if row.cache_key not in found]
    if not remaining:
        return found, None
    try:
        creation_transactions = routescan_creation_transactions(session, chain_id, remaining)
    except (requests.RequestException, ValueError):
        creation_transactions = {}
    if creation_transactions:
        for rpc_url in reversed(ARCHIVE_RPC_URLS.get(chain_id, [])):
            try:
                found.update(timestamps_for_transactions(
                    session,
                    rpc_url,
                    creation_transactions,
                    batch_size,
                ))
                break
            except Exception:
                continue
        remaining = [row for row in remaining if row.cache_key not in found]
        if not remaining:
            return found, None
    errors = []
    for rpc_url in ARCHIVE_RPC_URLS.get(chain_id, []):
        try:
            blocks = discover_first_code_blocks(session, rpc_url, remaining, batch_size)
            found.update(timestamps_for_blocks(session, rpc_url, blocks, batch_size))
            return found, None
        except Exception as exc:
            errors.append(f"{rpc_url}: {exc}")
    return {}, "; ".join(errors) or f"no archive RPC configured for chain {chain_id}"


def backfill_sql(sql_text: str, timestamps: dict[str, int]) -> tuple[str, int]:
    updated_chunks = []
    updated_count = 0
    for chunk in sql_text.split("\n*\n"):
        match = EVM_ROW_PATTERN.search(chunk)
        if match and STARTED_PATTERN.search(chunk):
            identifier, _chain_id, _address = match.groups()
            if timestamp := timestamps.get(identifier):
                chunk = STARTED_PATTERN.sub(rf"\g<1>{timestamp}\g<2>", chunk, count=1)
                updated_count += 1
        updated_chunks.append(chunk)
    return "\n*\n".join(updated_chunks), updated_count


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--updates-sql", required=True)
    parser.add_argument("--cache", default=".asset_cache/deployment_timestamps.json")
    parser.add_argument("--unresolved", default=None)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--offline", action="store_true")
    args = parser.parse_args()

    load_env_file(Path(__file__).resolve().parent.parent / ".env")
    updates_sql = Path(args.updates_sql)
    cache_path = Path(args.cache)
    sql_text = updates_sql.read_text()
    missing = parse_missing_started(sql_text)
    cache = load_cache(cache_path)
    session = requests.Session()
    blockscout_api_key = os.getenv("BLOCKSCOUT_API_KEY")
    errors: dict[int, str] = {}

    if not args.offline:
        grouped: dict[int, list[MissingStarted]] = defaultdict(list)
        for row in missing:
            if row.cache_key not in cache:
                grouped[row.chain_id].append(row)
        for chain_id, rows in sorted(grouped.items()):
            found, error = discover_chain_timestamps(
                session,
                rows,
                args.batch_size,
                blockscout_api_key,
            )
            cache.update(found)
            save_cache(cache_path, cache)
            print(f"chain {chain_id}: resolved {len(found)}/{len(rows)}")
            if error:
                errors[chain_id] = error

    by_identifier = {
        row.identifier: cache[row.cache_key]
        for row in missing
        if row.cache_key in cache
    }
    updated_text, updated_count = backfill_sql(sql_text, by_identifier)
    updates_sql.write_text(updated_text)

    unresolved_rows = [row for row in missing if row.cache_key not in cache]
    unresolved_path = (
        Path(args.unresolved)
        if args.unresolved else
        updates_sql.with_name("unresolved_started_dates.txt")
    )
    unresolved_path.write_text("\n".join(
        f"{row.chain_id},{row.address},{row.identifier}"
        for row in unresolved_rows
    ) + ("\n" if unresolved_rows else ""))
    print(f"Backfilled started dates: {updated_count}")
    print(f"Remaining unresolved: {len(unresolved_rows)}")
    for chain_id, error in errors.items():
        print(f"[warn] chain {chain_id}: {error}")


if __name__ == "__main__":
    main()

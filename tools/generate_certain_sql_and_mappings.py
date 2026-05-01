#!/usr/bin/env python3
"""Generate deterministic SQL inserts and location mappings for certain symbol->CoinGecko matches.

Input is the CSV produced by scripts/check_symbols_against_coingecko.py.
Only rows with match_count == 1 are processed.

This script prefers local cache and only queries CoinGecko for missing coin details.
Fetched coin details are cached under .coingecko_cache/coins/ and reused on next runs.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

import requests

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

EVM_IDENTIFIER = "eip155:{blockchain}/erc20:{address}"
SOLANA_IDENTIFIER = "solana/token:{address}"

ASSETS_QUERY = "{insert} assets(identifier, name, type) VALUES('{identifier}', '{name}', '{asset_type}'); "
EVM_TOKENS_QUERY = "{insert} evm_tokens(identifier, token_kind, chain, address, decimals, protocol) VALUES('{identifier}', 'A', {blockchain}, '{address}', {decimals}, {protocol}); "
SOLANA_TOKENS_QUERY = "{insert} solana_tokens(identifier, token_kind, address, decimals, protocol) VALUES('{identifier}', 'D', '{address}', {decimals}, {protocol}); "
COMMON_ASSET_DETAILS_QUERY = "{insert} common_asset_details(identifier, symbol, coingecko, cryptocompare, forked, started, swapped_for) VALUES('{identifier}', '{symbol}', {coingecko}, NULL, NULL, {deployed_at}, NULL);"
ASSET_COLLECTION_QUERY = "{insert} asset_collections(id, name, symbol, main_asset) VALUES ({collection}, '{name}', '{symbol}', '{main_asset}');"
ASSET_MAPPING_QUERY = "{insert} multiasset_mappings(collection_id, asset) VALUES ({collection}, '{identifier}');"


class Chain(Enum):
    SOLANA = -1
    ETHEREUM = 1
    BINANCE = 56
    BASE = 8453
    ARBITRUM_ONE = 42161
    OPTIMISM = 10
    POLYGON_POS = 137
    GNOSIS = 100
    SCROLL = 534352
    FANTOM = 250
    AVALANCHE = 43114
    ARBITRUM_NOVA = 42170
    CRONOS = 25
    ZKSYNC = 324
    LINEA = 59144


COINGECKO_PLATFORM_TO_CHAIN = {
    "ethereum": Chain.ETHEREUM,
    "binance-smart-chain": Chain.BINANCE,
    "base": Chain.BASE,
    "arbitrum-one": Chain.ARBITRUM_ONE,
    "optimistic-ethereum": Chain.OPTIMISM,
    "polygon-pos": Chain.POLYGON_POS,
    "xdai": Chain.GNOSIS,
    "scroll": Chain.SCROLL,
    "fantom": Chain.FANTOM,
    "avalanche": Chain.AVALANCHE,
    "arbitrum-nova": Chain.ARBITRUM_NOVA,
    "cronos": Chain.CRONOS,
    "zksync": Chain.ZKSYNC,
    "linea": Chain.LINEA,
    "solana": Chain.SOLANA,
}

LOCATION_DB_CHAR = {
    # Centralized exchange names -> DB char (Location.serialize_for_db)
    "kraken": "B",
    "poloniex": "C",
    "bittrex": "D",
    "binance": "E",
    "bitmex": "F",
    "coinbase": "G",
    "coinbasepro": "K",
    "coinbase_pro": "K",
    "gemini": "L",
    "cryptocom": "P",
    "crypto_com": "P",
    "bitstamp": "R",
    "binanceus": "S",
    "binance_us": "S",
    "bitfinex": "T",
    "bitcoinde": "U",
    "bitcoin_de": "U",
    "iconomi": "V",
    "kucoin": "W",
    "ftx": "Z",
    "nexo": "a",
    "blockfi": "b",
    "independentreserve": "c",
    "independent_reserve": "c",
    "shapeshift": "f",
    "uphold": "g",
    "bitpanda": "h",
    "bisq": "i",
    "ftxus": "j",
    "ftx_us": "j",
    "okx": "k",
    "woo": "r",
    "bybit": "s",
    "htx": "v",
}

RPC_PROVIDERS = {
    Chain.ETHEREUM: "https://eth.llamarpc.com",
    Chain.BINANCE: "https://binance.llamarpc.com",
    Chain.POLYGON_POS: "https://polygon.drpc.org",
    Chain.AVALANCHE: "https://api.avax.network/ext/bc/C/rpc",
    Chain.FANTOM: "https://1rpc.io/ftm",
    Chain.OPTIMISM: "https://mainnet.optimism.io",
    Chain.ARBITRUM_ONE: "https://arbitrum.meowrpc.com",
    Chain.GNOSIS: "https://rpc.gnosischain.com",
    Chain.ARBITRUM_NOVA: "https://arbitrum-nova.drpc.org",
    Chain.BASE: "https://base.llamarpc.com",
    Chain.CRONOS: "https://cronos.drpc.org",
    Chain.SCROLL: "https://scroll.drpc.org",
    Chain.ZKSYNC: "https://1rpc.io/zksync2-era",
    Chain.LINEA: "https://rpc.linea.build",
}

BLOCKSCOUT_API = {
    Chain.ETHEREUM: "https://eth.blockscout.com/api",
    Chain.OPTIMISM: "https://explorer.optimism.io/api",
    Chain.BASE: "https://base.blockscout.com/api",
    Chain.ARBITRUM_ONE: "https://arbitrum.blockscout.com/api",
    Chain.GNOSIS: "https://gnosis.blockscout.com/api",
    Chain.POLYGON_POS: "https://polygon.blockscout.com/api",
    Chain.SCROLL: "https://scroll.blockscout.com/api",
}

ETHERSCAN_CHAIN_ID = {
    Chain.ETHEREUM: 1,
    Chain.OPTIMISM: 10,
    Chain.BINANCE: 56,
    Chain.GNOSIS: 100,
    Chain.POLYGON_POS: 137,
    Chain.FANTOM: 250,
    Chain.ZKSYNC: 324,
    Chain.LINEA: 59144,
    Chain.BASE: 8453,
    Chain.ARBITRUM_ONE: 42161,
    Chain.AVALANCHE: 43114,
}


@dataclass
class TokenRecord:
    address: str
    chain: Chain
    decimals: int | None
    name: str | None
    symbol: str | None
    started: int | str | None = "NULL"

    def identifier(self) -> str:
        if self.chain == Chain.SOLANA:
            return SOLANA_IDENTIFIER.format(address=self.address)
        return EVM_IDENTIFIER.format(blockchain=self.chain.value, address=self.address)


def sql_escape(value: str | None) -> str:
    return (value or "").replace("'", "''")


def insert_prefix(insert_or_ignore: bool) -> str:
    return "INSERT OR IGNORE INTO" if insert_or_ignore else "INSERT INTO"


def normalize_location_key(location: str) -> str:
    return location.strip().lower().replace("-", "_").replace(" ", "_")


def load_existing_identifiers(path: Path) -> set[str]:
    if not path.exists():
        return set()
    data = path.read_text()
    return set(re.findall(r"assets\(identifier[^)]*\)\s+VALUES\('([^']+)'", data, re.IGNORECASE))


def load_existing_location_rows(path: Path) -> set[tuple[str, str, str]]:
    if not path.exists():
        return set()
    data = path.read_text()
    rows = re.findall(
        r'location_asset_mappings\(location,exchange_symbol,local_id\)\s+VALUES\s*\("([^"]+)",\s*"([^"]+)",\s*"([^"]+)"\)',
        data,
        re.IGNORECASE,
    )
    return set(rows)


def load_existing_evm_address_map(path: Path) -> dict[tuple[int, str], str]:
    if not path.exists():
        return {}
    data = path.read_text()
    # Capture: identifier, chain, address from evm_tokens INSERT lines
    matches = re.findall(
        r"evm_tokens\(identifier,\s*token_kind,\s*chain,\s*address,\s*decimals,\s*protocol\)\s+VALUES\('\s*([^']+)\s*',\s*'[^']*',\s*(\d+),\s*'\s*([^']+)\s*',",
        data,
        re.IGNORECASE,
    )
    result: dict[tuple[int, str], str] = {}
    for identifier, chain, address in matches:
        key = (int(chain), address.lower())
        result[key] = identifier
    return result


def load_existing_location_json_additions(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
        additions = data.get("location_asset_mappings", {}).get("additions", [])
        if isinstance(additions, list):
            clean: list[dict[str, str]] = []
            for item in additions:
                if not isinstance(item, dict):
                    continue
                asset = str(item.get("asset") or "").strip()
                location = str(item.get("location") or "").strip()
                location_symbol = str(item.get("location_symbol") or "").strip()
                if asset and location and location_symbol:
                    clean.append(
                        {
                            "asset": asset,
                            "location": location,
                            "location_symbol": location_symbol,
                        }
                    )
            return clean
    except Exception:
        return []
    return []


def merge_location_json_additions(existing: list[dict[str, str]], new: list[dict[str, str]]) -> list[dict[str, str]]:
    merged: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for item in existing + new:
        key = (item["asset"], item["location"], item["location_symbol"])
        if key in seen:
            continue
        seen.add(key)
        merged.append(item)
    return merged


def parse_certain_rows(csv_path: Path) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            symbol = (row.get("symbol") or "").strip().upper()
            ids = (row.get("coingecko_ids") or "").strip()
            count = int((row.get("match_count") or "0").strip())
            if count != 1 or not ids or not symbol:
                continue
            rows.append((symbol, ids.split("|")[0]))
    return rows


def find_existing_identifier_by_chain_address(db_path: Path | None, chain: Chain, address: str) -> str | None:
    if db_path is None or not db_path.exists() or chain == Chain.SOLANA:
        return None
    try:
        with sqlite3.connect(db_path) as conn:
            row = conn.execute(
                "SELECT identifier FROM evm_tokens WHERE chain = ? AND lower(address) = lower(?) LIMIT 1",
                (chain.value, address),
            ).fetchone()
            return row[0] if row else None
    except sqlite3.Error:
        return None


def find_existing_identifier_by_coingecko(db_path: Path | None, coin_id: str) -> str | None:
    if db_path is None or not db_path.exists():
        return None
    try:
        with sqlite3.connect(db_path) as conn:
            row = conn.execute(
                """
                SELECT cad.identifier
                FROM common_asset_details cad
                LEFT JOIN evm_tokens et ON et.identifier = cad.identifier
                WHERE cad.coingecko = ?
                ORDER BY CASE WHEN et.chain = 1 THEN 0 ELSE 1 END, cad.identifier
                LIMIT 1
                """,
                (coin_id,),
            ).fetchone()
            return row[0] if row else None
    except sqlite3.Error:
        return None


def resolve_existing_identifier(db_path: Path | None, coin_id: str, tokens: list[TokenRecord]) -> str | None:
    for token in tokens:
        identifier = find_existing_identifier_by_chain_address(db_path, token.chain, token.address)
        if identifier:
            return identifier
    return find_existing_identifier_by_coingecko(db_path, coin_id)


def coin_cache_path(cache_dir: Path, coin_id: str) -> Path:
    return cache_dir / f"{coin_id}.json"


def coingecko_get_json(endpoint: str, api_key: str | None = None) -> dict[str, Any]:
    headers = {}
    if api_key:
        headers["x-cg-demo-api-key"] = api_key
    r = requests.get(endpoint, headers=headers, timeout=30)
    r.raise_for_status()
    return r.json()


def get_coin_data(coin_id: str, cache_dir: Path, fetch_missing: bool, api_key: str | None) -> dict[str, Any] | None:
    cache_file = coin_cache_path(cache_dir, coin_id)
    if cache_file.exists():
        cached = json.loads(cache_file.read_text())
        if isinstance(cached, dict) and "data" in cached:
            return cached["data"]
        if isinstance(cached, dict) and cached.get("id") == coin_id:
            return cached

    if not fetch_missing:
        return None

    try:
        data = coingecko_get_json(f"{COINGECKO_BASE_URL}/coins/{coin_id}", api_key=api_key)
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        cache_file.write_text(json.dumps({"data": data}, indent=2))
        return data
    except Exception as exc:
        print(f"[warn] failed to fetch coin {coin_id}: {exc}")
        return None


def rpc_call(rpc_url: str, method: str, params: list[Any]) -> Any:
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params,
    }
    r = requests.post(rpc_url, json=payload, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise RuntimeError(str(data["error"]))
    return data.get("result")


def get_timestamp_from_tx_hash(chain: Chain, tx_hash: str) -> int | str:
    rpc = RPC_PROVIDERS.get(chain)
    if not rpc:
        return "NULL"
    try:
        tx = rpc_call(rpc, "eth_getTransactionByHash", [tx_hash])
        if not tx or not tx.get("blockNumber"):
            return "NULL"
        block = rpc_call(rpc, "eth_getBlockByNumber", [tx["blockNumber"], False])
        if not block or not block.get("timestamp"):
            return "NULL"
        return int(block["timestamp"], 16)
    except Exception:
        return "NULL"


def blockscout_creation_tx(chain: Chain, address: str) -> str | None:
    base = BLOCKSCOUT_API.get(chain)
    if not base:
        return None
    try:
        r = requests.get(
            f"{base}?module=contract&action=getcontractcreation&contractaddresses={address}",
            timeout=20,
        )
        if r.status_code >= 400:
            return None
        data = r.json()
        result = data.get("result") or []
        if not result:
            return None
        tx_hash = result[0].get("txHash")
        return tx_hash if isinstance(tx_hash, str) and tx_hash else None
    except Exception:
        return None


def etherscan_started(chain: Chain, address: str, api_key: str | None) -> int | str:
    chainid = ETHERSCAN_CHAIN_ID.get(chain)
    if not chainid:
        return "NULL"
    params = {
        "chainid": chainid,
        "module": "contract",
        "action": "getcontractcreation",
        "contractaddresses": address,
    }
    if api_key:
        params["apikey"] = api_key
    try:
        r = requests.get("https://api.etherscan.io/v2/api", params=params, timeout=20)
        if r.status_code >= 400:
            return "NULL"
        data = r.json()
        result = data.get("result") or []
        if not result:
            return "NULL"
        item = result[0]
        direct = item.get("timestamp")
        if isinstance(direct, str) and direct.isdigit():
            return int(direct)
        tx_hash = item.get("txHash")
        if isinstance(tx_hash, str) and tx_hash:
            return get_timestamp_from_tx_hash(chain, tx_hash)
    except Exception:
        return "NULL"
    return "NULL"


def get_deployed_ts(chain: Chain, address: str, etherscan_api_key: str | None) -> int | str:
    if chain == Chain.SOLANA:
        return "NULL"
    tx_hash = blockscout_creation_tx(chain, address)
    if tx_hash:
        ts = get_timestamp_from_tx_hash(chain, tx_hash)
        if ts != "NULL":
            return ts
    return etherscan_started(chain, address, etherscan_api_key)


def extract_tokens_from_coin(data: dict[str, Any]) -> list[TokenRecord]:
    seen: set[tuple[Chain, str]] = set()
    tokens: list[TokenRecord] = []

    detail_platforms = data.get("detail_platforms") or {}
    for platform, details in detail_platforms.items():
        chain = COINGECKO_PLATFORM_TO_CHAIN.get(platform)
        if chain is None:
            continue
        address = (details or {}).get("contract_address") or ""
        if not address:
            continue
        key = (chain, address.lower())
        if key in seen:
            continue
        seen.add(key)
        tokens.append(
            TokenRecord(
                address=address,
                chain=chain,
                decimals=(details or {}).get("decimal_place"),
                name=data.get("name"),
                symbol=(data.get("symbol") or "").upper() or None,
            )
        )

    platforms = data.get("platforms") or {}
    for platform, address in platforms.items():
        chain = COINGECKO_PLATFORM_TO_CHAIN.get(platform)
        if chain is None or not address:
            continue
        key = (chain, address.lower())
        if key in seen:
            continue
        seen.add(key)
        tokens.append(
            TokenRecord(
                address=address,
                chain=chain,
                decimals=9 if chain == Chain.SOLANA else 18,
                name=data.get("name"),
                symbol=(data.get("symbol") or "").upper() or None,
            )
        )

    return tokens


def choose_main_asset(tokens: list[TokenRecord]) -> TokenRecord:
    for token in tokens:
        if token.chain == Chain.ETHEREUM:
            return token
    return tokens[0]


def token_sql(token: TokenRecord, coin_id: str, insert_or_ignore: bool) -> str:
    insert = insert_prefix(insert_or_ignore)
    identifier = token.identifier()
    decimals = token.decimals if token.decimals is not None else (9 if token.chain == Chain.SOLANA else 18)

    deployed_at = token.started if token.started not in (None, "") else "NULL"
    fmt = {
        "insert": insert,
        "identifier": identifier,
        "name": sql_escape(token.name),
        "asset_type": "Y" if token.chain == Chain.SOLANA else "C",
        "symbol": sql_escape(token.symbol),
        "coingecko": f"'{coin_id}'",
        "blockchain": token.chain.value,
        "address": token.address,
        "decimals": decimals,
        "protocol": "NULL",
        "deployed_at": deployed_at,
    }

    sql = ASSETS_QUERY.format(**fmt)
    sql += (SOLANA_TOKENS_QUERY if token.chain == Chain.SOLANA else EVM_TOKENS_QUERY).format(**fmt)
    sql += COMMON_ASSET_DETAILS_QUERY.format(**fmt)
    return sql


def placeholder_sql(symbol: str, coin_id: str, coin_name: str, insert_or_ignore: bool) -> str:
    insert = insert_prefix(insert_or_ignore)
    fmt = {
        "insert": insert,
        "identifier": sql_escape(symbol),
        "name": sql_escape(coin_name or symbol),
        "asset_type": "W",
        "symbol": sql_escape(symbol),
        "coingecko": f"'{coin_id}'",
        "deployed_at": "NULL",
    }
    return (
        ASSETS_QUERY.format(**fmt)
        + COMMON_ASSET_DETAILS_QUERY.format(**fmt)
    )


def append_sql(path: Path, chunks: list[str]) -> None:
    if not chunks:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    needs_leading_newline = False
    if path.exists() and path.stat().st_size > 0:
        with path.open("rb") as rf:
            rf.seek(-1, 2)
            needs_leading_newline = rf.read(1) != b"\n"

    with path.open("a") as f:
        if needs_leading_newline:
            f.write("\n")
        for chunk in chunks:
            f.write(chunk)
            if not chunk.endswith("\n"):
                f.write("\n")


def load_next_collection_id(path: Path, start: int, db_path: Path | None = None) -> int:
    if path.exists():
        data = path.read_text()
        ids = [
            int(x)
            for x in re.findall(
                r"asset_collections\(id,\s*name,\s*symbol,\s*main_asset\)\s+VALUES\s*\((\d+),",
                data,
            )
        ]
        if ids:
            return max(ids) + 1

    if db_path is not None and db_path.exists():
        try:
            with sqlite3.connect(db_path) as conn:
                row = conn.execute("SELECT MAX(id) FROM asset_collections").fetchone()
                max_id = row[0] if row else None
                if isinstance(max_id, int):
                    return max_id + 1
        except sqlite3.Error:
            pass

    return start


def update_started_in_updates_sql(path: Path, identifier: str, deployed_at: int | str) -> bool:
    if deployed_at in (None, "", "NULL") or not path.exists():
        return False
    data = path.read_text()
    escaped_identifier = re.escape(identifier)
    pattern = re.compile(
        rf"(common_asset_details\([^)]*started[^)]*\)\s+VALUES\('{escaped_identifier}',\s*'[^']*',\s*[^,]*,\s*[^,]*,\s*NULL,\s*)([^,]+)(,\s*NULL\);)",
        re.IGNORECASE,
    )
    updated = pattern.sub(rf"\g<1>{deployed_at}\g<3>", data)
    if updated == data:
        return False
    path.write_text(updated)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate updates SQL and location mappings from certainty CSV")
    parser.add_argument("certainty_csv", help="CSV from check_symbols_against_coingecko.py")
    parser.add_argument("--exchange", default="kraken")
    parser.add_argument("--location", default="kraken", help="Location for mapping JSON/SQL")
    parser.add_argument("--updates-sql", required=True)
    parser.add_argument("--collections-sql", required=True)
    parser.add_argument("--mappings-sql", required=True)
    parser.add_argument("--location-mappings-sql", required=True)
    parser.add_argument("--location-mappings-json", required=True)
    parser.add_argument("--collection-start", type=int, default=1)
    parser.add_argument("--insert-or-ignore", action="store_true")
    parser.add_argument("--no-fetch-missing", action="store_true", help="Do not query CoinGecko if coin cache missing")
    parser.add_argument("--coin-cache-dir", default=None)
    parser.add_argument(
        "--global-db",
        default=None,
        help="Path to global.db to check existing assets by address/coingecko (default: ./global.db if present)",
    )
    args = parser.parse_args()

    certainty_csv = Path(args.certainty_csv)
    updates_sql = Path(args.updates_sql)
    collections_sql = Path(args.collections_sql)
    mappings_sql = Path(args.mappings_sql)
    location_mappings_sql = Path(args.location_mappings_sql)
    location_mappings_json = Path(args.location_mappings_json)

    coin_cache_dir = Path(args.coin_cache_dir) if args.coin_cache_dir else (Path(__file__).resolve().parent.parent / ".coingecko_cache" / "coins")
    api_key = os.getenv("COINGECKO_API_KEY")
    etherscan_api_key = os.getenv("ETHERSCAN_API_KEY")

    default_global_db = Path(__file__).resolve().parent.parent / "global.db"
    global_db_path: Path | None = Path(args.global_db) if args.global_db else (default_global_db if default_global_db.exists() else None)

    location_key = normalize_location_key(args.location)
    if location_key not in LOCATION_DB_CHAR:
        raise SystemExit(f"Unsupported location '{args.location}'. Add it in LOCATION_DB_CHAR.")

    existing_identifiers = load_existing_identifiers(updates_sql)
    existing_evm_address_map = load_existing_evm_address_map(updates_sql)
    existing_location_rows = load_existing_location_rows(location_mappings_sql)
    existing_location_json_additions = load_existing_location_json_additions(location_mappings_json)
    next_collection_id = load_next_collection_id(
        collections_sql,
        args.collection_start,
        db_path=global_db_path,
    )

    rows = parse_certain_rows(certainty_csv)

    updates_chunks: list[str] = []
    collections_chunks: list[str] = []
    mappings_chunks: list[str] = []
    location_sql_chunks: list[str] = []
    location_json_additions: list[dict[str, str]] = []

    inserted = 0
    skipped = 0

    for symbol, coin_id in rows:
        coin_data = get_coin_data(
            coin_id=coin_id,
            cache_dir=coin_cache_dir,
            fetch_missing=not args.no_fetch_missing,
            api_key=api_key,
        )
        if coin_data is None:
            print(f"[skip] no coin data for {symbol}/{coin_id}")
            skipped += 1
            continue

        tokens = extract_tokens_from_coin(coin_data)
        mapped_identifier: str | None = None

        existing_identifier = resolve_existing_identifier(global_db_path, coin_id, tokens)
        if existing_identifier:
            mapped_identifier = existing_identifier
            print(f"[existing-db] {symbol}/{coin_id} -> {mapped_identifier}")
        elif not tokens:
            mapped_identifier = symbol
            if mapped_identifier not in existing_identifiers:
                updates_chunks.append(
                    placeholder_sql(
                        symbol=symbol,
                        coin_id=coin_id,
                        coin_name=coin_data.get("name") or symbol,
                        insert_or_ignore=args.insert_or_ignore,
                    ) + "\n*\n"
                )
                existing_identifiers.add(mapped_identifier)
                inserted += 1
        else:
            token_identifiers_written: list[str] = []
            token_records_to_map: list[TokenRecord] = []
            for token in tokens:
                if token.chain != Chain.SOLANA:
                    token.started = get_deployed_ts(token.chain, token.address, etherscan_api_key)
                identifier = token.identifier()
                token_records_to_map.append(token)

                existing_by_address_identifier: str | None = None
                if token.chain != Chain.SOLANA:
                    existing_by_address_identifier = existing_evm_address_map.get((token.chain.value, token.address.lower()))
                if existing_by_address_identifier:
                    if existing_by_address_identifier != identifier:
                        print(f"[skip-address] {identifier} already present as {existing_by_address_identifier}")
                    if update_started_in_updates_sql(updates_sql, existing_by_address_identifier, token.started):
                        print(f"[started] updated {existing_by_address_identifier} -> {token.started}")
                    continue

                if identifier in existing_identifiers:
                    if update_started_in_updates_sql(updates_sql, identifier, token.started):
                        print(f"[started] updated {identifier} -> {token.started}")
                    continue
                updates_chunks.append(token_sql(token, coin_id=coin_id, insert_or_ignore=args.insert_or_ignore) + "\n*\n")
                existing_identifiers.add(identifier)
                if token.chain != Chain.SOLANA:
                    existing_evm_address_map[(token.chain.value, token.address.lower())] = identifier
                token_identifiers_written.append(identifier)
                inserted += 1

            main_asset = choose_main_asset(token_records_to_map)
            if main_asset.chain != Chain.SOLANA:
                mapped_identifier = existing_evm_address_map.get(
                    (main_asset.chain.value, main_asset.address.lower()),
                    main_asset.identifier(),
                )
            else:
                mapped_identifier = main_asset.identifier()

            if len(token_records_to_map) > 1 and token_identifiers_written:
                insert = insert_prefix(args.insert_or_ignore)
                collections_chunks.append(
                    ASSET_COLLECTION_QUERY.format(
                        insert=insert,
                        collection=next_collection_id,
                        name=sql_escape(main_asset.name),
                        symbol=sql_escape(main_asset.symbol),
                        main_asset=main_asset.identifier(),
                    ) + "\n*\n"
                )
                for token in token_records_to_map:
                    mappings_chunks.append(
                        ASSET_MAPPING_QUERY.format(
                            insert=insert,
                            collection=next_collection_id,
                            identifier=token.identifier(),
                        ) + "\n*\n"
                    )
                next_collection_id += 1

        if mapped_identifier:
            db_char = LOCATION_DB_CHAR[location_key]
            row_key = (db_char, symbol, mapped_identifier)
            if row_key not in existing_location_rows:
                location_sql_chunks.append(
                    f'INSERT INTO location_asset_mappings(location,exchange_symbol,local_id) VALUES ("{db_char}", "{symbol}", "{mapped_identifier}");\n*\n'
                )
                existing_location_rows.add(row_key)
            location_json_additions.append(
                {
                    "asset": mapped_identifier,
                    "location": location_key,
                    "location_symbol": symbol,
                }
            )

    append_sql(updates_sql, updates_chunks)
    append_sql(collections_sql, collections_chunks)
    append_sql(mappings_sql, mappings_chunks)
    append_sql(location_mappings_sql, location_sql_chunks)

    location_mappings_json.parent.mkdir(parents=True, exist_ok=True)
    merged_location_json_additions = merge_location_json_additions(
        existing_location_json_additions,
        location_json_additions,
    )
    location_mappings_json.write_text(
        json.dumps({"location_asset_mappings": {"additions": merged_location_json_additions}}, indent=4)
    )

    print(f"Processed certain rows: {len(rows)}")
    print(f"Inserted/queued SQL entries: {inserted}")
    print(f"Skipped due to missing coin data: {skipped}")
    print(f"updates: {updates_sql}")
    print(f"collections: {collections_sql}")
    print(f"collection mappings: {mappings_sql}")
    print(f"location mappings sql: {location_mappings_sql}")
    print(f"location mappings json: {location_mappings_json}")


if __name__ == "__main__":
    main()

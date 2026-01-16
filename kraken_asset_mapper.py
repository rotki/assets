#!/usr/bin/env python3
"""
Script to map exchange symbols to CoinGecko IDs, fetch token details, and generate SQL.

Usage:
    python kraken_asset_mapper.py <symbols_file> [--cache <cache_file>]

Args:
    symbols_file: File with one symbol per line
    --cache: Optional path to previously downloaded exchange cache file

Environment:
    COINGECKO_API_KEY: Optional CoinGecko API key
"""

import argparse
import csv
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any
import re

import requests
from eth_utils.address import to_checksum_address
from web3 import HTTPProvider, Web3
from web3.middleware import ExtraDataToPOAMiddleware

COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"

# Identifier Templates
EVM_IDENTIFIER = "eip155:{blockchain}/erc20:{address}"
SOLANA_IDENTIFIER = "solana/token:{address}"

# SQL Query Templates
ASSETS_QUERY = "{insert} assets(identifier, name, type) VALUES('{identifier}', '{name}', '{asset_type}'); "
EVM_TOKENS_QUERY = "{insert} evm_tokens(identifier, token_kind, chain, address, decimals, protocol) VALUES('{identifier}', 'A', {blockchain}, '{address}', {decimals}, {protocol}); "
SOLANA_TOKENS_QUERY = "{insert} solana_tokens(identifier, token_kind, address, decimals, protocol) VALUES('{identifier}', 'D', '{address}', {decimals}, {protocol}); "
COMMON_ASSET_DETAILS_QUERY = "{insert} common_asset_details(identifier, symbol, coingecko, cryptocompare, forked, started, swapped_for) VALUES('{identifier}', '{symbol}', {coingecko}, {cryptocompare}, NULL, {deployed_at}, NULL);"
ASSET_COLLECTION_QUERY = "{insert} asset_collections(id, name, symbol, main_asset) VALUES ({collection}, '{name}', '{symbol}', '{main_asset}');"
ASSET_MAPPING_QUERY = "{insert} multiasset_mappings(collection_id, asset) VALUES ({collection}, '{identifier}');"


class Chain(Enum):
    """Supported blockchains and their chain IDs."""

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

RPC_PROVIDERS = {
    Chain.ETHEREUM: "https://mainnet.infura.io/v3/33457f352e1a44da89f36b2ee5dec263",
    Chain.BINANCE: "https://bsc-mainnet.infura.io/v3/33457f352e1a44da89f36b2ee5dec263",
    Chain.POLYGON_POS: "https://polygon.drpc.org",
    Chain.AVALANCHE: "https://api.avax.network/ext/bc/C/rpc",
    Chain.FANTOM: "https://1rpc.io/ftm",
    Chain.OPTIMISM: "https://mainnet.optimism.io",
    Chain.ARBITRUM_ONE: "https://arbitrum.meowrpc.com",
    Chain.GNOSIS: "https://rpc.gnosischain.com",
    Chain.ARBITRUM_NOVA: "https://arbitrum-nova.drpc.org",
    Chain.BASE: "https://base-mainnet.infura.io/v3/33457f352e1a44da89f36b2ee5dec263",
    Chain.CRONOS: "https://cronos.drpc.org",
    Chain.SCROLL: "https://scroll.drpc.org",
    Chain.ZKSYNC: "https://1rpc.io/zksync2-era",
    Chain.LINEA: "https://rpc.linea.build",
}

ERC20_ABI = """[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]"""


@dataclass
class TokenRecord:
    address: str
    chain: Chain
    decimals: int | None
    name: str | None
    symbol: str | None
    started: int | str | None
    source: str

    def identifier(self) -> str:
        if self.chain == Chain.SOLANA:
            return SOLANA_IDENTIFIER.format(address=self.address)
        return EVM_IDENTIFIER.format(blockchain=self.chain.value, address=self.address)


def get_api_key() -> str:
    return os.getenv("COINGECKO_API_KEY", "")


def get_cache_dir() -> Path:
    cache_dir = Path(__file__).parent / ".coingecko_cache"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir


def get_cache_filepath(exchange_name: str, date_str: str) -> Path:
    cache_dir = get_cache_dir()
    return cache_dir / f"{exchange_name}_{date_str}.json"


def get_coin_cache_path(coin_id: str) -> Path:
    cache_dir = get_cache_dir() / "coins"
    cache_dir.mkdir(exist_ok=True)
    return cache_dir / f"{coin_id}.json"


def get_token_cache_path(chain: Chain, address: str) -> Path:
    cache_dir = get_cache_dir() / "tokens"
    cache_dir.mkdir(exist_ok=True)
    safe_address = address.lower().replace(":", "_")
    return cache_dir / f"{chain.name.lower()}_{safe_address}.json"


def load_cached_data(cache_file: str | Path | None) -> dict[str, Any] | None:
    if not cache_file or not Path(cache_file).exists():
        return None

    try:
        with open(cache_file, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def prompt_yes_no(prompt: str, default: bool = True) -> bool:
    suffix = "Y/n" if default else "y/N"
    while True:
        value = input(f"{prompt} [{suffix}]: ").strip().lower()
        if value == "" and default is not None:
            return default
        if value in ("y", "yes"):
            return True
        if value in ("n", "no"):
            return False


def write_json(path: Path, data: dict[str, Any]) -> None:
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2)
    tmp_path.replace(path)


def load_progress(progress_path: Path, exchange: str, collection_start: int) -> dict[str, Any]:
    if progress_path.exists():
        data = load_cached_data(progress_path)
        if data:
            return data

    return {
        "meta": {
            "exchange": exchange,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "collection_start": collection_start,
            "next_collection_id": collection_start,
        },
        "symbols": {},
        "coins": {},
    }


def new_progress(exchange: str, collection_start: int) -> dict[str, Any]:
    return {
        "meta": {
            "exchange": exchange,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "collection_start": collection_start,
            "next_collection_id": collection_start,
        },
        "symbols": {},
        "coins": {},
    }


def save_progress(progress_path: Path, progress: dict[str, Any]) -> None:
    progress["meta"]["updated_at"] = datetime.now().isoformat()
    progress_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(progress_path, progress)


def fetch_exchange_data(exchange_name: str, api_key: str | None = None) -> dict[str, Any]:
    endpoint = f"{COINGECKO_BASE_URL}/exchanges/{exchange_name}/tickers"
    headers = {}
    params = {"per_page": 250}

    if api_key:
        headers["x-cg-demo-api-key"] = api_key

    print(f"Fetching tickers from CoinGecko for exchange: {exchange_name}")
    all_tickers = []
    page = 1

    while True:
        params["page"] = page
        try:
            response = requests.get(endpoint, params=params, headers=headers, timeout=20)
            if response.status_code != 200:
                print(f"Response status: {response.status_code}")
                print(f"Response body: {response.text}")
            response.raise_for_status()
            data = response.json()

            if "tickers" not in data or not data["tickers"]:
                break

            all_tickers.extend(data["tickers"])
            print(f"  Fetched page {page}: {len(data['tickers'])} tickers")
            page += 1
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}", file=sys.stderr)
            raise

    return {
        "exchange": exchange_name,
        "fetched_at": datetime.now().isoformat(),
        "tickers": all_tickers,
    }


def read_symbols_file(filepath: str) -> list[str]:
    with open(filepath, "r") as f:
        return [line.strip().upper() for line in f if line.strip()]


def filter_tickers_by_symbols(data: dict[str, Any], symbols: list[str]) -> list[dict[str, Any]]:
    symbol_set = set(symbols)
    matching = []

    print(f"\nSearching for {len(symbols)} symbols in {len(data['tickers'])} tickers")
    if data["tickers"]:
        print(f"Sample ticker structure: {data['tickers'][0]}")

    for ticker in data["tickers"]:
        ticker_symbol = ticker.get("symbol") or ticker.get("base")
        if ticker_symbol and ticker_symbol.upper() in symbol_set:
            matching.append(ticker)

    return matching


def build_csv_data(tickers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen_coin_ids = set()
    rows = []

    for ticker in tickers:
        coin_id = ticker.get("coin_id", "")
        if coin_id in seen_coin_ids:
            continue
        seen_coin_ids.add(coin_id)
        rows.append(
            {
                "ticker": ticker.get("market", {}).get("identifier", ""),
                "symbol": ticker.get("base", "").upper(),
                "coingecko_id": coin_id,
                "name": ticker.get("market", {}).get("name", ""),
            }
        )

    rows.sort(key=lambda x: x["symbol"])
    return rows


def write_csv_output(rows: list[dict[str, Any]], output_file: str) -> None:
    fieldnames = ["ticker", "symbol", "coingecko_id", "name"]

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Output written to: {output_file}")


def coingecko_get_json(endpoint: str, api_key: str | None = None, params: dict[str, Any] | None = None) -> dict[str, Any]:
    headers = {}
    if api_key:
        headers["x-cg-demo-api-key"] = api_key
    response = requests.get(endpoint, params=params, headers=headers, timeout=20)
    response.raise_for_status()
    return response.json()


def query_coingecko_coin(coin_id: str, api_key: str, retry_failed: bool) -> dict[str, Any] | None:
    cache_path = get_coin_cache_path(coin_id)
    cached = load_cached_data(cache_path)
    if cached and cached.get("data") and not retry_failed:
        return cached["data"]
    if cached and cached.get("error") and not retry_failed:
        return None

    try:
        data = coingecko_get_json(f"{COINGECKO_BASE_URL}/coins/{coin_id}", api_key=api_key)
        write_json(cache_path, {"fetched_at": datetime.now().isoformat(), "data": data})
        return data
    except Exception as exc:
        write_json(
            cache_path,
            {
                "fetched_at": datetime.now().isoformat(),
                "error": str(exc),
            },
        )
        return None


def extract_tokens_from_coingecko(data: dict[str, Any]) -> list[tuple[Chain, str, int | None]]:
    tokens = []
    seen = set()

    detail_platforms = data.get("detail_platforms") or {}
    if detail_platforms:
        for platform, details in detail_platforms.items():
            chain = COINGECKO_PLATFORM_TO_CHAIN.get(platform)
            if chain is None:
                continue
            address = (details or {}).get("contract_address") or ""
            if not address:
                continue
            decimals = (details or {}).get("decimal_place")
            key = (chain, address.lower())
            if key in seen:
                continue
            seen.add(key)
            tokens.append((chain, address, decimals))

    platforms = data.get("platforms") or {}
    for platform, address in platforms.items():
        chain = COINGECKO_PLATFORM_TO_CHAIN.get(platform)
        if chain is None:
            continue
        if not address:
            continue
        key = (chain, address.lower())
        if key in seen:
            continue
        seen.add(key)
        tokens.append((chain, address, None))

    return tokens


def sql_escape(value: str | None) -> str:
    if value is None:
        return ""
    return value.replace("'", "''")


def get_insert_prefix(insert_or_ignore: bool) -> str:
    return "INSERT OR IGNORE INTO" if insert_or_ignore else "INSERT INTO"


def get_deployed_ts(address: str, chain: Chain, web3_provider: Web3) -> int | str:
    try:
        match chain:
            case Chain.ETHEREUM:
                url = "https://eth.blockscout.com/api"
            case Chain.OPTIMISM:
                url = "https://explorer.optimism.io/api"
            case Chain.BASE:
                url = "https://base.blockscout.com/api"
            case Chain.ARBITRUM_ONE:
                url = "https://arbitrum.blockscout.com/api"
            case Chain.GNOSIS:
                url = "https://gnosis.blockscout.com/api"
            case Chain.POLYGON_POS:
                url = "https://polygon.blockscout.com/api"
            case Chain.SCROLL:
                url = "https://scroll.blockscout.com/api"
            case _:
                return "NULL"

        url += f"?module=contract&action=getcontractcreation&contractaddresses={address}"
        response = requests.get(url=url, timeout=20)
        if response.status_code == 429:
            print(f"[rate-limit] Blockscout for {chain.name} ({address}); started set to NULL")
            return "NULL"
        if response.status_code >= 500:
            print(f"[network] Blockscout {response.status_code} for {chain.name} ({address}); started set to NULL")
            return "NULL"
        tx_hash = response.json()["result"][0]["txHash"]
        tx = web3_provider.eth.get_transaction(tx_hash)
        block = web3_provider.eth.get_block(tx["blockNumber"])
        return block["timestamp"]
    except Exception as exc:
        print(f"[network] Could not fetch deployment timestamp for {address} on {chain.name}: {exc}; started set to NULL")
        return "NULL"


def fetch_evm_token_details(address: str, chain: Chain, retry_failed: bool) -> TokenRecord | None:
    cache_path = get_token_cache_path(chain, address)
    cached = load_cached_data(cache_path)
    if cached and cached.get("data") and not retry_failed:
        data = cached["data"]
        return TokenRecord(
            address=data["address"],
            chain=chain,
            decimals=data.get("decimals"),
            name=data.get("name"),
            symbol=data.get("symbol"),
            started=data.get("started"),
            source=data.get("source", "rpc"),
        )
    if cached and cached.get("error") and not retry_failed:
        return None

    try:
        address = to_checksum_address(address)
    except ValueError:
        pass

    try:
        provider = Web3(HTTPProvider(RPC_PROVIDERS[chain]))
        provider.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        contract = provider.eth.contract(address=address, abi=ERC20_ABI)
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        decimals = contract.functions.decimals().call()
        started = get_deployed_ts(address=address, chain=chain, web3_provider=provider)
        record = {
            "address": address,
            "name": name,
            "symbol": symbol,
            "decimals": decimals,
            "started": started,
            "source": "rpc",
        }
        write_json(cache_path, {"fetched_at": datetime.now().isoformat(), "data": record})
        return TokenRecord(
            address=address,
            chain=chain,
            decimals=decimals,
            name=name,
            symbol=symbol,
            started=started,
            source="rpc",
        )
    except Exception as exc:
        print(f"[network] RPC error for {address} on {chain.name}: {exc}; started set to NULL")
        write_json(
            cache_path,
            {
                "fetched_at": datetime.now().isoformat(),
                "error": str(exc),
            },
        )
        return None


def resolve_token_details(
    chain: Chain,
    address: str,
    decimals: int | None,
    fallback_name: str | None,
    fallback_symbol: str | None,
    retry_failed: bool,
) -> TokenRecord:
    if chain != Chain.SOLANA:
        token = fetch_evm_token_details(address=address, chain=chain, retry_failed=retry_failed)
        if token is not None:
            return token
        print(f"[fallback] Using CoinGecko data for {address} on {chain.name}; started set to NULL")

    try:
        address = to_checksum_address(address)
    except ValueError:
        pass

    if decimals is None:
        decimals = 9 if chain == Chain.SOLANA else 18

    return TokenRecord(
        address=address,
        chain=chain,
        decimals=decimals,
        name=fallback_name,
        symbol=fallback_symbol,
        started="NULL",
        source="coingecko",
    )


def build_token_sql(
    token: TokenRecord,
    coingecko_id: str | None,
    insert_or_ignore: bool,
) -> str:
    insert = get_insert_prefix(insert_or_ignore)
    name = sql_escape(token.name or "")
    symbol = sql_escape(token.symbol or "")
    decimals = token.decimals if token.decimals is not None else (9 if token.chain == Chain.SOLANA else 18)
    deployed_at = token.started if token.started not in (None, "") else "NULL"
    coingecko_value = f"'{coingecko_id}'" if coingecko_id else "NULL"

    format_kwargs = {
        "insert": insert,
        "identifier": token.identifier(),
        "name": name,
        "symbol": symbol,
        "decimals": decimals,
        "protocol": "NULL",
        "blockchain": token.chain.value,
        "address": token.address,
        "coingecko": coingecko_value,
        "cryptocompare": "NULL",
        "deployed_at": deployed_at,
        "asset_type": "Y" if token.chain == Chain.SOLANA else "C",
    }

    query = ASSETS_QUERY.format(**format_kwargs)
    if token.chain == Chain.SOLANA:
        query += SOLANA_TOKENS_QUERY.format(**format_kwargs)
    else:
        query += EVM_TOKENS_QUERY.format(**format_kwargs)
    query += COMMON_ASSET_DETAILS_QUERY.format(**format_kwargs)
    return query


def build_non_evm_sql(
    identifier: str,
    name: str,
    symbol: str,
    coingecko_id: str | None,
    asset_type: str,
    insert_or_ignore: bool,
) -> str:
    insert = get_insert_prefix(insert_or_ignore)
    format_kwargs = {
        "insert": insert,
        "identifier": sql_escape(identifier),
        "name": sql_escape(name),
        "symbol": sql_escape(symbol),
        "coingecko": f"'{coingecko_id}'" if coingecko_id else "NULL",
        "cryptocompare": "NULL",
        "deployed_at": "NULL",
        "asset_type": asset_type,
    }
    query = ASSETS_QUERY.format(**format_kwargs)
    query += COMMON_ASSET_DETAILS_QUERY.format(**format_kwargs)
    return query


def write_sql(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(content)
        if not content.endswith("\n"):
            f.write("\n")

def load_existing_collection_csv(path: Path) -> set[tuple[str, str, str]]:
    if not path.exists():
        return set()
    try:
        with open(path, "r") as f:
            reader = csv.DictReader(f)
            existing = set()
            for row in reader:
                asset = (row.get("asset") or "").strip()
                location = (row.get("location") or "").strip()
                location_symbol = (row.get("location_symbol") or "").strip()
                if asset and location and location_symbol:
                    existing.add((asset, location, location_symbol))
            return existing
    except Exception:
        return set()

def write_collection_csv_row(path: Path, asset: str, location: str, location_symbol: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    file_exists = path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["asset", "location", "location_symbol"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "asset": asset,
                "location": location,
                "location_symbol": location_symbol,
            }
        )


def update_started_in_updates_sql(path: Path, identifier: str, deployed_at: int | str) -> bool:
    if not path.exists():
        return False
    try:
        data = path.read_text()
    except Exception:
        return False

    escaped_identifier = re.escape(identifier)
    pattern = re.compile(
        rf"(common_asset_details\([^)]*started[^)]*\)\s+VALUES\('{escaped_identifier}',\s*'[^']*',\s*[^,]*,\s*[^,]*,\s*NULL,\s*)([^,]+)(,\s*NULL\);)",
        re.IGNORECASE,
    )
    if not pattern.search(data):
        return False
    updated = pattern.sub(rf"\g<1>{deployed_at}\g<3>", data)
    if updated == data:
        return False
    path.write_text(updated)
    return True

def load_existing_identifiers(path: Path) -> set[str]:
    if not path.exists():
        return set()
    try:
        data = path.read_text()
    except Exception:
        return set()
    pattern = re.compile(r"assets\(identifier[^)]*\)\s+VALUES\('([^']+)'", re.IGNORECASE)
    return set(pattern.findall(data))

def load_coingecko_symbol_map(path: Path) -> dict[str, list[str]]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except Exception:
        return {}
    symbol_map: dict[str, list[str]] = {}
    for entry in data:
        symbol = (entry.get("symbol") or "").upper()
        coin_id = entry.get("id")
        if not symbol or not coin_id:
            continue
        symbol_map.setdefault(symbol, []).append(coin_id)
    return symbol_map

def infer_coingecko_id(symbol: str, symbol_map: dict[str, list[str]]) -> str | None:
    ids = symbol_map.get(symbol.upper(), [])
    if len(ids) == 1:
        return ids[0]
    if len(ids) > 1:
        print(f"[coingecko] Multiple ids for symbol {symbol}: {ids}; leaving NULL")
    return None

def should_write_identifier(identifier: str, existing: set[str], written: set[str]) -> bool:
    if identifier in existing:
        print(f"[skip] Already in updates.sql: {identifier}")
        return False
    if identifier in written:
        return False
    return True


def process_coin_id(
    coin_id: str,
    progress: dict[str, Any],
    progress_path: Path,
    api_key: str,
    insert_or_ignore: bool,
    updates_sql: Path,
    collections_sql: Path,
    mappings_sql: Path,
    retry_failed: bool,
    resume: bool,
    existing_identifiers: set[str],
    written_identifiers: set[str],
    collections_csv: Path,
    collections_csv_existing: set[tuple[str, str, str]],
    location_symbol: str,
    exchange_name: str,
) -> None:
    coins_progress = progress.setdefault("coins", {})
    coin_entry = coins_progress.get(coin_id)
    if resume and coin_entry and coin_entry.get("status") == "completed" and coin_entry.get("sql_written"):
        return

    data = query_coingecko_coin(coin_id=coin_id, api_key=api_key, retry_failed=retry_failed)
    if data is None:
        coins_progress[coin_id] = {
            "status": "coingecko_failed",
            "updated_at": datetime.now().isoformat(),
        }
        save_progress(progress_path, progress)
        return

    coin_name = data.get("name") or ""
    coin_symbol = (data.get("symbol") or "").upper()

    tokens_raw = extract_tokens_from_coingecko(data)
    if not tokens_raw:
        platforms = data.get("platforms") or {}
        detail_platforms = data.get("detail_platforms") or {}
        asset_platform_id = data.get("asset_platform_id")
        is_native = not platforms and not detail_platforms and asset_platform_id not in (None, "", "null")
        asset_type = "B" if is_native else "W"
        placeholder_identifier = coin_symbol or coin_id
        if should_write_identifier(placeholder_identifier, existing_identifiers, written_identifiers):
            placeholder_sql = build_non_evm_sql(
                identifier=placeholder_identifier,
                name=coin_name or coin_symbol or coin_id,
                symbol=coin_symbol or coin_id,
                coingecko_id=coin_id,
                asset_type=asset_type,
                insert_or_ignore=insert_or_ignore,
            )
            write_sql(updates_sql, f"{placeholder_sql}\n*\n")
            written_identifiers.add(placeholder_identifier)
        coins_progress[coin_id] = {
            "status": "non_evm",
            "name": coin_name,
            "symbol": coin_symbol,
            "asset_type": asset_type,
            "sql_written": True,
            "updated_at": datetime.now().isoformat(),
        }
        save_progress(progress_path, progress)
        return

    if not coin_entry:
        coin_entry = {
            "status": "partial",
            "name": coin_name,
            "symbol": coin_symbol,
            "coingecko_id": coin_id,
            "tokens": [],
            "errors": [],
        }
        coins_progress[coin_id] = coin_entry
        save_progress(progress_path, progress)

    existing_tokens = {
        (t.get("chain"), (t.get("address") or "").lower())
        for t in coin_entry.get("tokens", [])
    }

    token_records: list[TokenRecord] = []
    for chain, address, decimals in tokens_raw:
        key = (chain.name, address.lower())
        if key in existing_tokens:
            continue
        token = resolve_token_details(
            chain=chain,
            address=address,
            decimals=decimals,
            fallback_name=coin_name,
            fallback_symbol=coin_symbol,
            retry_failed=retry_failed,
        )
        token_records.append(token)
        coin_entry["tokens"].append(
            {
                "address": token.address,
                "chain": token.chain.name,
                "decimals": token.decimals,
                "name": token.name,
                "symbol": token.symbol,
                "started": token.started,
                "source": token.source,
            }
        )
        save_progress(progress_path, progress)

    if coin_entry.get("tokens"):
        token_records = [
            TokenRecord(
                address=t["address"],
                chain=Chain[t["chain"]],
                decimals=t.get("decimals"),
                name=t.get("name"),
                symbol=t.get("symbol"),
                started=t.get("started"),
                source=t.get("source", "cache"),
            )
            for t in coin_entry["tokens"]
        ]

    if not token_records:
        coin_entry["status"] = "no_tokens"
        save_progress(progress_path, progress)
        return

    main_asset = None
    for token in token_records:
        if token.chain == Chain.ETHEREUM:
            main_asset = token
            break
    if main_asset is None:
        main_asset = token_records[0]

    collection_id = coin_entry.get("collection_id")

    updates_sql_str = ""
    written_this_coin: list[TokenRecord] = []
    for token in token_records:
        identifier = token.identifier()
        if not should_write_identifier(identifier, existing_identifiers, written_identifiers):
            continue
        updates_sql_str += build_token_sql(
            token=token,
            coingecko_id=coin_id,
            insert_or_ignore=insert_or_ignore,
        )
        updates_sql_str += "\n*\n"
        written_identifiers.add(identifier)
        written_this_coin.append(token)

    if updates_sql_str:
        write_sql(updates_sql, updates_sql_str)

    if len(written_this_coin) > 1:
        if collection_id is None:
            collection_id = progress["meta"]["next_collection_id"]
            progress["meta"]["next_collection_id"] = collection_id + 1
            coin_entry["collection_id"] = collection_id
            save_progress(progress_path, progress)
        insert = get_insert_prefix(insert_or_ignore)
        collection_sql = ASSET_COLLECTION_QUERY.format(
            insert=insert,
            collection=collection_id,
            name=sql_escape(main_asset.name or ""),
            symbol=sql_escape(main_asset.symbol or ""),
            main_asset=main_asset.identifier(),
        )
        write_sql(collections_sql, f"{collection_sql}\n*\n")

        mappings_sql_str = ""
        for token in written_this_coin:
            mappings_sql_str += ASSET_MAPPING_QUERY.format(
                insert=insert,
                collection=collection_id,
                identifier=token.identifier(),
            )
            mappings_sql_str += "\n*\n"
        write_sql(mappings_sql, mappings_sql_str)

        main_identifier = main_asset.identifier()
        csv_key = (main_identifier, exchange_name, location_symbol)
        if csv_key not in collections_csv_existing:
            write_collection_csv_row(
                path=collections_csv,
                asset=main_identifier,
                location=exchange_name,
                location_symbol=location_symbol,
            )
            collections_csv_existing.add(csv_key)

    coin_entry["status"] = "completed"
    coin_entry["sql_written"] = True
    coin_entry["main_asset_identifier"] = main_asset.identifier()
    save_progress(progress_path, progress)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch exchange symbols from CoinGecko and generate SQL",
    )
    parser.add_argument("symbols_file", help="File with symbols (one per line)")
    parser.add_argument("--cache", help="Previously downloaded cache file to use")
    parser.add_argument("--exchange", default="kraken", help="Exchange name (default: kraken)")
    parser.add_argument(
        "--output",
        help="Output CSV file (default: raptor/<exchange>/<exchange>_symbols_YYYY-MM-DD.csv)",
    )
    parser.add_argument(
        "--updates-sql",
        default=None,
        help="Output SQL file for assets (default: raptor/<exchange>/updates.sql)",
    )
    parser.add_argument(
        "--existing-updates-sql",
        default=None,
        help="Existing updates.sql to read for deduping (read-only; never modified)",
    )
    parser.add_argument(
        "--collections-sql",
        default=None,
        help="Output SQL file for asset collections (default: raptor/<exchange>/asset_collections_updates.sql)",
    )
    parser.add_argument(
        "--mappings-sql",
        default=None,
        help="Output SQL file for collection mappings (default: raptor/<exchange>/asset_collections_mappings_updates.sql)",
    )
    parser.add_argument(
        "--collections-csv",
        default=None,
        help="Output CSV for collection main assets (default: raptor/<exchange>/asset_collections.csv)",
    )
    parser.add_argument(
        "--progress",
        default=None,
        help="Progress file path (default: progress/<exchange>_asset_mapper.json)",
    )
    parser.add_argument(
        "--collection-start",
        type=int,
        default=1,
        help="Starting collection id (default: 1)",
    )
    parser.add_argument(
        "--insert-or-ignore",
        action="store_true",
        help="Use INSERT OR IGNORE instead of INSERT",
    )
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Ignore existing progress and reprocess",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Retry cached failures for CoinGecko/RPC calls",
    )

    args = parser.parse_args()

    if not Path(args.symbols_file).exists():
        print(f"Error: Symbols file not found: {args.symbols_file}", file=sys.stderr)
        sys.exit(1)

    symbols = read_symbols_file(args.symbols_file)
    print(f"Read {len(symbols)} symbols from {args.symbols_file}")

    data = None
    if args.cache:
        print(f"Loading cache from: {args.cache}")
        data = load_cached_data(args.cache)
        if data:
            print("Successfully loaded cached data")
        else:
            print("Cache file not found or invalid, will fetch fresh data")
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        default_cache = get_cache_filepath(args.exchange, today)
        if default_cache.exists():
            if prompt_yes_no(f"Cache found at {default_cache}. Use it?", default=True):
                data = load_cached_data(default_cache)
                if data:
                    print("Successfully loaded cached data")
                else:
                    print("Cache file invalid, will fetch fresh data")

    if not data:
        api_key = get_api_key()
        data = fetch_exchange_data(args.exchange, api_key)
        today = datetime.now().strftime("%Y-%m-%d")
        cache_file = get_cache_filepath(args.exchange, today)
        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Cached data saved to: {cache_file}")

    matching_tickers = filter_tickers_by_symbols(data, symbols)
    print(f"Found {len(matching_tickers)} matching tickers")

    if not args.output:
        today = datetime.now().strftime("%Y-%m-%d")
        args.output = str(Path("raptor") / args.exchange / f"{args.exchange}_symbols_{today}.csv")

    if not args.updates_sql:
        args.updates_sql = str(Path("raptor") / args.exchange / "updates.sql")
    if not args.collections_sql:
        args.collections_sql = str(Path("raptor") / args.exchange / "asset_collections_updates.sql")
    if not args.mappings_sql:
        args.mappings_sql = str(Path("raptor") / args.exchange / "asset_collections_mappings_updates.sql")
    if not args.collections_csv:
        args.collections_csv = str(Path("raptor") / args.exchange / "asset_collections.csv")

    for output_path in (args.output, args.updates_sql, args.collections_sql, args.mappings_sql, args.collections_csv):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    csv_rows = build_csv_data(matching_tickers)
    write_csv_output(csv_rows, args.output)

    progress_path = Path(args.progress) if args.progress else Path("raptor") / args.exchange / "progress.json"
    if args.no_resume:
        if progress_path.exists():
            progress_path.unlink()
        progress = new_progress(args.exchange, args.collection_start)
    else:
        progress = load_progress(progress_path, args.exchange, args.collection_start)
    existing_identifiers = load_existing_identifiers(Path(args.updates_sql))
    if args.existing_updates_sql:
        existing_identifiers |= load_existing_identifiers(Path(args.existing_updates_sql))
    written_identifiers: set[str] = set()
    coingecko_symbol_map: dict[str, list[str]] = {}
    collections_csv_path = Path(args.collections_csv)
    collections_csv_existing = load_existing_collection_csv(collections_csv_path)

    symbol_tickers: dict[str, list[dict[str, Any]]] = {}
    for ticker in matching_tickers:
        ticker_symbol = ticker.get("base") or ticker.get("symbol")
        if not ticker_symbol:
            continue
        symbol_tickers.setdefault(ticker_symbol.upper(), []).append(ticker)

    api_key = get_api_key()
    resume = not args.no_resume

    total_symbols = len(symbols)
    for idx, symbol in enumerate(symbols, start=1):
        remaining = total_symbols - idx
        print(f"[{idx}/{total_symbols}] {symbol} (remaining: {remaining})")
        symbol_entry = progress.setdefault("symbols", {}).get(symbol, {})
        if resume and (symbol_entry.get("status") == "completed" or symbol_entry.get("sql_written")):
            status = symbol_entry.get("status")
            if status in ("missing_ticker", "missing_coin_id"):
                if symbol in existing_identifiers or symbol in written_identifiers:
                    continue
            else:
                continue

        tickers = symbol_tickers.get(symbol, [])
        if not tickers:
            if not coingecko_symbol_map:
                coingecko_symbol_map = load_coingecko_symbol_map(Path("coingecko_coins.json"))
            inferred_id = infer_coingecko_id(symbol, coingecko_symbol_map)
            if should_write_identifier(symbol, existing_identifiers, written_identifiers):
                placeholder_sql = build_non_evm_sql(
                    identifier=symbol,
                    name=symbol,
                    symbol=symbol,
                    coingecko_id=inferred_id,
                    asset_type="W",
                    insert_or_ignore=args.insert_or_ignore,
                )
                write_sql(Path(args.updates_sql), f"{placeholder_sql}\n*\n")
                written_identifiers.add(symbol)
            progress["symbols"][symbol] = {
                "status": "missing_ticker",
                "coingecko_id": inferred_id,
                "sql_written": True,
                "updated_at": datetime.now().isoformat(),
            }
            save_progress(progress_path, progress)
            continue

        coin_ids = sorted({t.get("coin_id") for t in tickers if t.get("coin_id")})
        if not coin_ids:
            if not coingecko_symbol_map:
                coingecko_symbol_map = load_coingecko_symbol_map(Path("coingecko_coins.json"))
            inferred_id = infer_coingecko_id(symbol, coingecko_symbol_map)
            if should_write_identifier(symbol, existing_identifiers, written_identifiers):
                placeholder_sql = build_non_evm_sql(
                    identifier=symbol,
                    name=symbol,
                    symbol=symbol,
                    coingecko_id=inferred_id,
                    asset_type="W",
                    insert_or_ignore=args.insert_or_ignore,
                )
                write_sql(Path(args.updates_sql), f"{placeholder_sql}\n*\n")
                written_identifiers.add(symbol)
            progress["symbols"][symbol] = {
                "status": "missing_coin_id",
                "coingecko_id": inferred_id,
                "sql_written": True,
                "updated_at": datetime.now().isoformat(),
            }
            save_progress(progress_path, progress)
            continue

        progress["symbols"][symbol] = {
            "status": "completed",
            "coin_ids": coin_ids,
            "updated_at": datetime.now().isoformat(),
        }
        save_progress(progress_path, progress)

        for coin_id in coin_ids:
            process_coin_id(
                coin_id=coin_id,
                progress=progress,
                progress_path=progress_path,
                api_key=api_key,
                insert_or_ignore=args.insert_or_ignore,
                updates_sql=Path(args.updates_sql),
                collections_sql=Path(args.collections_sql),
                mappings_sql=Path(args.mappings_sql),
                retry_failed=args.retry_failed,
                resume=resume,
                existing_identifiers=existing_identifiers,
                written_identifiers=written_identifiers,
                collections_csv=collections_csv_path,
                collections_csv_existing=collections_csv_existing,
                location_symbol=symbol,
                exchange_name=args.exchange,
            )

    coins_progress = progress.get("coins", {})
    if coins_progress:
        print("[started] Rechecking missing started timestamps...")
    for coin_id, coin_entry in coins_progress.items():
        tokens = coin_entry.get("tokens") or []
        for token in tokens:
            chain_name = token.get("chain")
            if not chain_name or chain_name == "SOLANA":
                continue
            started = token.get("started")
            if started not in (None, "", "NULL"):
                continue
            chain = Chain[chain_name]
            address = token.get("address")
            if not address or chain not in RPC_PROVIDERS:
                continue
            updated = fetch_evm_token_details(address=address, chain=chain, retry_failed=True)
            if updated is None or updated.started in (None, "", "NULL"):
                continue
            token["started"] = updated.started
            identifier = updated.identifier()
            updated_sql = update_started_in_updates_sql(
                path=Path(args.updates_sql),
                identifier=identifier,
                deployed_at=updated.started,
            )
            if updated_sql:
                print(f"[started] Updated insert for {identifier} -> {updated.started}")
            else:
                print(f"[started] Could not update insert for {identifier}")
            save_progress(progress_path, progress)
    if coins_progress:
        print("[started] Recheck complete.")

    print("Done.")


if __name__ == "__main__":
    main()

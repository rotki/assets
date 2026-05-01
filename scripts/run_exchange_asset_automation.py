#!/usr/bin/env python3
"""Orchestrate exchange asset automation end-to-end.

Given a warnings file and an update version, this script:
1) Extracts unknown symbols from warnings
2) Writes symbols file
3) Ensures local CoinGecko coins list exists (optionally refreshes)
4) Builds certainty CSV (symbol -> CoinGecko matches)
5) Generates SQL/mappings for updates/<version>

Example:
  python scripts/run_exchange_asset_automation.py \
    --warnings testwarnings/kraken.txt \
    --version 40
"""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from pathlib import Path

import requests
from eth_utils import to_checksum_address

COINGECKO_COINS_LIST_URL = "https://api.coingecko.com/api/v3/coins/list?include_platform=true"


def extract_unknown_symbols(warnings_path: Path, exchange: str) -> list[str]:
    text = warnings_path.read_text()

    # Kraken-style:
    #   Found unknown primary asset BASED in kraken
    primary_pattern = re.compile(
        rf"unknown\s+primary\s+asset\s+([A-Z0-9._-]+)\s+in\s+{re.escape(exchange)}\b",
        re.IGNORECASE,
    )

    # Coinbase-style:
    #   Found unknown asset BASED1 with symbol BASED1 in Coinbase
    # Prefer the symbol token for mapping, fall back to the asset token if missing.
    with_symbol_pattern = re.compile(
        rf"unknown\s+asset\s+([A-Z0-9._-]+)(?:\s+with\s+symbol\s+([A-Z0-9._-]+))?\s+in\s+{re.escape(exchange)}\b",
        re.IGNORECASE,
    )

    symbols: list[str] = []
    symbols.extend(primary_pattern.findall(text))
    for asset_token, symbol_token in with_symbol_pattern.findall(text):
        symbols.append(symbol_token or asset_token)

    deduped: list[str] = []
    seen: set[str] = set()
    for symbol in symbols:
        sym = symbol.upper()
        if sym not in seen:
            seen.add(sym)
            deduped.append(sym)
    return deduped


def write_symbols_file(path: Path, symbols: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(symbols) + ("\n" if symbols else ""))


def ensure_coingecko_list(path: Path, refresh: bool) -> None:
    if path.exists() and not refresh:
        return
    r = requests.get(COINGECKO_COINS_LIST_URL, timeout=60)
    r.raise_for_status()
    path.write_text(r.text)


def run_cmd(cmd: list[str], dry_run: bool) -> None:
    print("$", " ".join(cmd))
    if dry_run:
        return
    subprocess.run(cmd, check=True)


def read_certainty_summary(csv_path: Path) -> tuple[int, int, int, int]:
    total = unique = ambiguous = missing = 0
    with csv_path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            count = int((row.get("match_count") or "0").strip())
            if count == 1:
                unique += 1
            elif count == 0:
                missing += 1
            else:
                ambiguous += 1
    return total, unique, ambiguous, missing


def normalize_sql_file(path: Path) -> tuple[int, int]:
    if path.exists() is False:
        return 0, 0

    text = path.read_text()
    insert_count = text.count("INSERT OR IGNORE INTO")
    text = text.replace("INSERT OR IGNORE INTO", "INSERT INTO")

    checksummed = 0

    def _replace_address(match: re.Match[str]) -> str:
        nonlocal checksummed
        original = match.group(0)
        fixed = to_checksum_address(original)
        if fixed != original:
            checksummed += 1
        return fixed

    text = re.sub(r"0x[a-fA-F0-9]{40}", _replace_address, text)
    path.write_text(text)
    return insert_count, checksummed


def normalize_generated_sql_files(paths: list[Path]) -> None:
    for path in paths:
        replaced_inserts, checksummed_addresses = normalize_sql_file(path)
        if replaced_inserts or checksummed_addresses:
            print(
                f"  normalized {path}: INSERT OR IGNORE -> INSERT ({replaced_inserts}), "
                f"checksummed addresses ({checksummed_addresses})",
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Kraken asset automation workflow")
    parser.add_argument("--warnings", required=True, help="Path to warnings file (e.g. testwarnings/kraken.txt)")
    parser.add_argument("--version", required=True, help="Updates version folder (e.g. 40)")
    parser.add_argument("--exchange", default="kraken", help="Exchange name used in warnings and mappings")
    parser.add_argument("--coingecko-file", default=None, help="Path to local coingecko_coins.json")
    parser.add_argument("--refresh-coingecko", action="store_true", help="Refresh coingecko_coins.json from CoinGecko")
    parser.add_argument("--global-db", default=None, help="Path to global.db (default: ./global.db)")
    parser.add_argument("--no-fetch-missing", action="store_true", help="Do not fetch missing CoinGecko coin details")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing subprocesses")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    warnings_path = Path(args.warnings)
    if not warnings_path.exists():
        raise SystemExit(f"Warnings file not found: {warnings_path}")

    symbols_file = warnings_path.with_name(f"{warnings_path.stem}_symbols.txt")
    certainty_csv = warnings_path.with_name(f"{warnings_path.stem}_symbols_vs_coingecko.csv")

    coingecko_file = Path(args.coingecko_file) if args.coingecko_file else (repo_root / "coingecko_coins.json")

    updates_dir = repo_root / "updates" / str(args.version)
    updates_sql = updates_dir / "updates.sql"
    collections_sql = updates_dir / "asset_collections_updates.sql"
    mappings_sql = updates_dir / "asset_collections_mappings_updates.sql"
    location_sql = updates_dir / "location_asset_mappings_updates.sql"
    location_json = updates_dir / "location_asset_mappings.json"

    print(f"[1/5] Extracting symbols from: {warnings_path}")
    symbols = extract_unknown_symbols(warnings_path, exchange=args.exchange)
    write_symbols_file(symbols_file, symbols)
    print(f"  extracted: {len(symbols)} symbols -> {symbols_file}")

    print(f"[2/5] Ensuring CoinGecko list file: {coingecko_file}")
    if not args.dry_run:
        ensure_coingecko_list(coingecko_file, refresh=args.refresh_coingecko)

    print("[3/5] Building certainty CSV")
    check_script = repo_root / "scripts" / "check_symbols_against_coingecko.py"
    run_cmd(
        [
            sys.executable,
            str(check_script),
            str(symbols_file),
            "--coingecko-file",
            str(coingecko_file),
            "--output",
            str(certainty_csv),
        ],
        dry_run=args.dry_run,
    )

    if not args.dry_run:
        total, unique, ambiguous, missing = read_certainty_summary(certainty_csv)
        print(f"  certainty summary: total={total} unique={unique} ambiguous={ambiguous} missing={missing}")

    print(f"[4/5] Generating SQL and mappings for updates/{args.version}")
    gen_script = repo_root / "tools" / "generate_certain_sql_and_mappings.py"
    gen_cmd = [
        sys.executable,
        str(gen_script),
        str(certainty_csv),
        "--exchange",
        args.exchange,
        "--location",
        args.exchange,
        "--updates-sql",
        str(updates_sql),
        "--collections-sql",
        str(collections_sql),
        "--mappings-sql",
        str(mappings_sql),
        "--location-mappings-sql",
        str(location_sql),
        "--location-mappings-json",
        str(location_json),
    ]
    if args.global_db:
        gen_cmd += ["--global-db", args.global_db]
    if args.no_fetch_missing:
        gen_cmd += ["--no-fetch-missing"]

    run_cmd(gen_cmd, dry_run=args.dry_run)

    if not args.dry_run:
        normalize_generated_sql_files([
            updates_sql,
            collections_sql,
            mappings_sql,
            location_sql,
        ])

    print("[5/5] Done")
    print(f"  symbols:      {symbols_file}")
    print(f"  certainty:    {certainty_csv}")
    print(f"  updates.sql:  {updates_sql}")
    print(f"  collections:  {collections_sql}")
    print(f"  mappings:     {mappings_sql}")
    print(f"  loc sql:      {location_sql}")
    print(f"  loc json:     {location_json}")


if __name__ == "__main__":
    main()

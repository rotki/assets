#!/usr/bin/env python3
"""Check asset symbols against a local CoinGecko coins list file.

Usage:
  python scripts/check_symbols_against_coingecko.py <symbols_file> \
      [--coingecko-file coingecko_coins.json] \
      [--output symbols_vs_coingecko.csv]
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def read_symbols(path: Path) -> list[str]:
    return [line.strip().upper() for line in path.read_text().splitlines() if line.strip()]


def load_coingecko(path: Path) -> list[dict]:
    data = json.loads(path.read_text())
    if not isinstance(data, list):
        raise ValueError(f"Expected list in {path}, got {type(data).__name__}")
    return data


def build_symbol_index(coins: list[dict]) -> dict[str, list[tuple[str, str]]]:
    index: dict[str, list[tuple[str, str]]] = {}
    for entry in coins:
        symbol = (entry.get("symbol") or "").upper()
        coin_id = entry.get("id")
        name = entry.get("name") or ""
        if not symbol or not coin_id:
            continue
        index.setdefault(symbol, []).append((coin_id, name))
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description="Check symbols against local CoinGecko coins list")
    parser.add_argument("symbols_file", help="File with one symbol per line")
    parser.add_argument(
        "--coingecko-file",
        default="coingecko_coins.json",
        help="Path to local CoinGecko coins list JSON (default: coingecko_coins.json)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output CSV path (default: <symbols_file_stem>_vs_coingecko.csv)",
    )
    args = parser.parse_args()

    symbols_path = Path(args.symbols_file)
    cg_path = Path(args.coingecko_file)
    out_path = Path(args.output) if args.output else symbols_path.with_name(f"{symbols_path.stem}_vs_coingecko.csv")

    if not symbols_path.exists():
        raise SystemExit(f"Symbols file not found: {symbols_path}")
    if not cg_path.exists():
        raise SystemExit(f"CoinGecko file not found: {cg_path}")

    symbols = read_symbols(symbols_path)
    coins = load_coingecko(cg_path)
    index = build_symbol_index(coins)

    rows = []
    for symbol in symbols:
        matches = index.get(symbol, [])
        rows.append(
            {
                "symbol": symbol,
                "match_count": len(matches),
                "coingecko_ids": "|".join([m[0] for m in matches]),
                "names": "|".join([m[1] for m in matches]),
            }
        )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol", "match_count", "coingecko_ids", "names"])
        writer.writeheader()
        writer.writerows(rows)

    unique = [r for r in rows if r["match_count"] == 1]
    multi = [r for r in rows if r["match_count"] > 1]
    none = [r for r in rows if r["match_count"] == 0]

    print(f"Checked symbols: {len(symbols)}")
    print(f"Unique matches: {len(unique)}")
    print(f"Ambiguous matches: {len(multi)}")
    print(f"No matches: {len(none)}")
    if none:
        print("No-match symbols: " + ", ".join([r["symbol"] for r in none]))
    print(f"Wrote: {out_path}")


if __name__ == "__main__":
    main()

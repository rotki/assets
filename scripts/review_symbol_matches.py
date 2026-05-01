#!/usr/bin/env python3
"""Review and persist manual decisions for ambiguous symbol->CoinGecko matches.

This script lets you pause/resume manual review at any time.
Decisions are stored in a JSON state file and can be exported into a
"resolved" CSV that the SQL generator can consume directly.

Typical flow:
1) Build certainty CSV with check_symbols_against_coingecko.py
2) Review ambiguous rows with this script (interactive or --set)
3) Export resolved CSV
4) Run generate_certain_sql_and_mappings.py on resolved CSV
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Row:
    symbol: str
    match_count: int
    coingecko_ids: list[str]
    names: list[str]


def parse_row(raw: dict[str, str]) -> Row:
    symbol = (raw.get("symbol") or "").strip().upper()
    match_count = int((raw.get("match_count") or "0").strip() or "0")
    ids = [x.strip() for x in (raw.get("coingecko_ids") or "").split("|") if x.strip()]
    names = [x.strip() for x in (raw.get("names") or "").split("|") if x.strip()]
    return Row(symbol=symbol, match_count=match_count, coingecko_ids=ids, names=names)


def read_rows(path: Path) -> list[Row]:
    with path.open("r", newline="") as f:
        reader = csv.DictReader(f)
        return [parse_row(r) for r in reader]


def default_state_path(certainty_csv: Path) -> Path:
    return certainty_csv.with_name(f"{certainty_csv.stem}_review_state.json")


def load_state(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            return {k.upper(): str(v) for k, v in data.items()}
    except Exception:
        pass
    return {}


def save_state(path: Path, decisions: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dict(sorted(decisions.items())), indent=2))


def find_ambiguous(rows: list[Row]) -> list[Row]:
    return [r for r in rows if r.match_count > 1]


def list_status(rows: list[Row], decisions: dict[str, str]) -> None:
    ambiguous = find_ambiguous(rows)
    resolved = 0
    for row in ambiguous:
        if decisions.get(row.symbol) in set(row.coingecko_ids):
            resolved += 1
    pending = len(ambiguous) - resolved

    print(f"Ambiguous symbols: {len(ambiguous)}")
    print(f"Resolved: {resolved}")
    print(f"Pending: {pending}")
    print()

    for row in ambiguous:
        chosen = decisions.get(row.symbol)
        status = "RESOLVED" if chosen in set(row.coingecko_ids) else "PENDING"
        print(f"[{status}] {row.symbol}")
        for idx, coin_id in enumerate(row.coingecko_ids, start=1):
            name = row.names[idx - 1] if idx - 1 < len(row.names) else ""
            marker = "*" if coin_id == chosen else " "
            print(f"  {marker} {idx}. {coin_id} ({name})")
        print()


def set_decision(rows: list[Row], decisions: dict[str, str], symbol: str, coin_id: str) -> None:
    symbol = symbol.upper()
    target = next((r for r in rows if r.symbol == symbol), None)
    if target is None:
        raise SystemExit(f"Symbol not found in CSV: {symbol}")
    if target.match_count <= 1:
        print(f"Warning: {symbol} is not ambiguous (match_count={target.match_count}), storing decision anyway")
    if target.match_count > 1 and coin_id not in set(target.coingecko_ids):
        raise SystemExit(f"coin_id '{coin_id}' is not in candidates for {symbol}: {target.coingecko_ids}")
    decisions[symbol] = coin_id


def interactive_review(rows: list[Row], decisions: dict[str, str]) -> None:
    ambiguous = find_ambiguous(rows)
    for row in ambiguous:
        chosen = decisions.get(row.symbol)
        if chosen in set(row.coingecko_ids):
            continue

        print(f"\n{row.symbol} has {len(row.coingecko_ids)} candidates:")
        for idx, coin_id in enumerate(row.coingecko_ids, start=1):
            name = row.names[idx - 1] if idx - 1 < len(row.names) else ""
            print(f"  {idx}. {coin_id} ({name})")
        print("  s. skip for now")

        while True:
            ans = input("Choose number (or s): ").strip().lower()
            if ans in {"s", "skip", ""}:
                break
            if ans.isdigit() and 1 <= int(ans) <= len(row.coingecko_ids):
                decisions[row.symbol] = row.coingecko_ids[int(ans) - 1]
                print(f"Saved: {row.symbol} -> {decisions[row.symbol]}")
                break
            print("Invalid selection")


def export_resolved_csv(input_csv: Path, output_csv: Path, decisions: dict[str, str]) -> tuple[int, int]:
    with input_csv.open("r", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    converted = 0
    unresolved_ambiguous = 0
    out_rows: list[dict[str, str]] = []

    for raw in rows:
        row = parse_row(raw)
        if row.match_count > 1:
            chosen = decisions.get(row.symbol)
            if chosen in set(row.coingecko_ids):
                idx = row.coingecko_ids.index(chosen)
                name = row.names[idx] if idx < len(row.names) else ""
                raw["match_count"] = "1"
                raw["coingecko_ids"] = chosen
                raw["names"] = name
                converted += 1
            else:
                unresolved_ambiguous += 1
        out_rows.append(raw)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with output_csv.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["symbol", "match_count", "coingecko_ids", "names"])
        writer.writeheader()
        writer.writerows(out_rows)

    return converted, unresolved_ambiguous


def main() -> None:
    parser = argparse.ArgumentParser(description="Review ambiguous symbol matches and persist decisions")
    parser.add_argument("--certainty-csv", required=True, help="Input certainty CSV")
    parser.add_argument("--state-file", default=None, help="Decision state JSON path")
    parser.add_argument("--list", action="store_true", help="List ambiguous symbols and decision status")
    parser.add_argument("--interactive", action="store_true", help="Run interactive review for pending ambiguous symbols")
    parser.add_argument("--set", nargs=2, metavar=("SYMBOL", "COINGECKO_ID"), help="Set decision for a symbol")
    parser.add_argument("--clear", metavar="SYMBOL", help="Clear saved decision for symbol")
    parser.add_argument("--export", metavar="OUTPUT_CSV", help="Export resolved CSV with applied decisions")
    args = parser.parse_args()

    certainty_csv = Path(args.certainty_csv)
    if not certainty_csv.exists():
        raise SystemExit(f"certainty csv not found: {certainty_csv}")

    state_file = Path(args.state_file) if args.state_file else default_state_path(certainty_csv)
    rows = read_rows(certainty_csv)
    decisions = load_state(state_file)

    changed = False

    if args.set:
        symbol, coin_id = args.set
        set_decision(rows, decisions, symbol, coin_id)
        changed = True
        print(f"Saved decision: {symbol.upper()} -> {coin_id}")

    if args.clear:
        symbol = args.clear.upper()
        if symbol in decisions:
            decisions.pop(symbol, None)
            changed = True
            print(f"Cleared decision for {symbol}")

    if args.interactive:
        interactive_review(rows, decisions)
        changed = True

    if changed:
        save_state(state_file, decisions)
        print(f"State saved: {state_file}")

    if args.list or (not args.set and not args.clear and not args.interactive and not args.export):
        list_status(rows, decisions)
        print(f"State file: {state_file}")

    if args.export:
        out = Path(args.export)
        converted, unresolved = export_resolved_csv(certainty_csv, out, decisions)
        print(f"Exported: {out}")
        print(f"Converted ambiguous -> unique: {converted}")
        print(f"Remaining unresolved ambiguous: {unresolved}")


if __name__ == "__main__":
    main()

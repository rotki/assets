# Kraken asset automation workflow

## Multi-exchange missing-assets compiler

For warning files containing multiple exchanges, use the cache-first compiler:

```bash
.venv/bin/python tools/compile_missing_assets.py \
  --missing missing.txt \
  --version 41 \
  --global-db /path/to/rotkehlchen/data/global.db \
  --refresh
```

The compiler:

- parses and deduplicates every supported exchange warning;
- excludes symbols ending in `UP` or `DOWN`;
- refreshes the large CoinGecko and CryptoCompare catalogues once, then reuses
  them according to `--cache-max-age-hours`;
- checks both the global database and pending update SQL before generating rows;
- accepts unique exact CoinGecko symbol/name matches and leaves unsupported or
  ambiguous matches unresolved;
- supports evidence-backed decisions in
  `updates/<version>/asset_compilation/reviewed_overrides.json`;
- invokes the SQL generator per exchange and reconciles collection-main asset
  mappings into SQL, JSON, and the root `mappings.csv`;
- backfills missing EVM `started` timestamps using Blockscout PRO when
  configured, then chain explorers and batched archive-RPC lookup, with all
  successful results stored in a persistent deployment cache;
- writes the full evidence manifest, resolved CSVs, ignored assets, and
  unresolved assets under `updates/<version>/asset_compilation/`.

Use `--resolve-only` to rebuild reports without changing SQL or mappings. Use
`--offline` for a fully cached rerun. If CryptoCompare requires authentication,
set `CRYPTOCOMPARE_API_KEY` and rerun with `--refresh`; until then, the manifest
records the missing authentication and CryptoCompare IDs remain null.

For authenticated Blockscout deployment lookups, create an ignored `.env` file
at the repository root:

```dotenv
BLOCKSCOUT_API_KEY=your-key
```

`tools/backfill_started_dates.py` reads this file automatically and never
writes the credential to generated output or the deployment cache.

This document describes all scripts used in this asset-mapping workflow, the order to run them, and expected outputs.

## Goal

Given Kraken warnings, automatically:
1. Extract unknown symbols
2. Match symbols to CoinGecko IDs (using a local cached CoinGecko asset list)
3. Generate SQL inserts for `updates/<version>`
4. Generate collection mappings
5. Generate location mappings (SQL + JSON)
6. Populate/backfill `common_asset_details.started` (deployment timestamp) for EVM tokens

## One-command orchestrator (recommended)

Use:

```bash
/Users/yabirgb/work/rotki/.venv/bin/python scripts/run_exchange_asset_automation.py \
  --warnings testwarnings/kraken.txt \
  --version 40
```

Useful flags:
- `--exchange <name>` -> exchange/location key for mappings (examples: `kraken`, `binance`, `coinbase`, `okx`)
- `--no-fetch-missing` -> avoid CoinGecko coin-detail network fetches, cache-only mode
- `--refresh-coingecko` -> refresh local `coingecko_coins.json`
- `--global-db /path/to/global.db` -> override default `./global.db`
- `--dry-run` -> print commands only

The rest of this document describes each underlying script and manual step-by-step mode.

## Manual review workflow for ambiguous assets (pause/resume)

When `match_count > 1`, use the review helper to store decisions and resume anytime.

List pending/resolved ambiguous symbols:

```bash
/Users/yabirgb/work/rotki/.venv/bin/python scripts/review_symbol_matches.py \
  --certainty-csv testwarnings/kraken_symbols_vs_coingecko.csv \
  --list
```

Interactive review (saves state in `*_review_state.json`):

```bash
/Users/yabirgb/work/rotki/.venv/bin/python scripts/review_symbol_matches.py \
  --certainty-csv testwarnings/kraken_symbols_vs_coingecko.csv \
  --interactive
```

Set one decision directly:

```bash
/Users/yabirgb/work/rotki/.venv/bin/python scripts/review_symbol_matches.py \
  --certainty-csv testwarnings/kraken_symbols_vs_coingecko.csv \
  --set USDT0 usdt0
```

Export a resolved CSV (ambiguous rows with decisions are converted to `match_count=1`):

```bash
/Users/yabirgb/work/rotki/.venv/bin/python scripts/review_symbol_matches.py \
  --certainty-csv testwarnings/kraken_symbols_vs_coingecko.csv \
  --export testwarnings/kraken_symbols_vs_coingecko_resolved.csv
```

Then run generation using the resolved CSV:

```bash
/Users/yabirgb/work/rotki/.venv/bin/python tools/generate_certain_sql_and_mappings.py \
  testwarnings/kraken_symbols_vs_coingecko_resolved.csv \
  --updates-sql updates/40/updates.sql \
  --collections-sql updates/40/asset_collections_updates.sql \
  --mappings-sql updates/40/asset_collections_mappings_updates.sql \
  --location-mappings-sql updates/40/location_asset_mappings_updates.sql \
  --location-mappings-json updates/40/location_asset_mappings.json \
  --insert-or-ignore
```

---

## Prerequisites

- Repo root: `/Users/yabirgb/work/assets`
- Python env used in examples: `/Users/yabirgb/work/rotki/.venv/bin/python`
- Local CoinGecko list file: `coingecko_coins.json`
- Optional env vars:
  - `COINGECKO_API_KEY` (reduces rate-limit issues)
  - `ETHERSCAN_API_KEY` (used as fallback for deployment timestamp lookup)

Example:

```bash
export COINGECKO_API_KEY=...
export ETHERSCAN_API_KEY=...
```

---

## Scripts and what they do

## 1) `tools/extract_from_warnings.py`

Purpose:
- Extract unknown assets from warning logs.

Input:
- Text file with warnings (e.g. `testwarnings/kraken.txt`)

Output:
- Prints extracted symbols list (you can redirect to a file)

Usage:

```bash
/Users/yabirgb/work/rotki/.venv/bin/python tools/extract_from_warnings.py testwarnings/kraken.txt
```

Notes:
- This is a helper parser.
- For this workflow, we keep a one-symbol-per-line file (e.g. `testwarnings/kraken_symbols.txt`).

---

## 2) `scripts/check_symbols_against_coingecko.py`

Purpose:
- Match symbols against local `coingecko_coins.json`.
- Produce a certainty CSV with unique/ambiguous/missing matches.

Input:
- Symbols file (one symbol per line)
- Local CoinGecko list JSON

Output:
- CSV with columns:
  - `symbol`
  - `match_count`
  - `coingecko_ids`
  - `names`

Usage:

```bash
/Users/yabirgb/work/rotki/.venv/bin/python scripts/check_symbols_against_coingecko.py \
  testwarnings/kraken_symbols.txt \
  --coingecko-file coingecko_coins.json \
  --output testwarnings/kraken_symbols_vs_coingecko.csv
```

Interpretation:
- `match_count == 1`: safe to automate
- `match_count > 1`: ambiguous, manual decision needed
- `match_count == 0`: not found

---

## 3) `tools/generate_certain_sql_and_mappings.py`

Purpose:
- Consume certainty CSV and automate only `match_count == 1` rows.
- Before generating inserts, check `global.db` for existing assets:
  - First by `(chain, address)` in `evm_tokens`
  - Then by `coingecko` in `common_asset_details`
- If an asset already exists in DB, reuse that identifier and create location mapping only (skip asset insert SQL).
- Additionally, before inserting any EVM token, the script checks `updates/<version>/updates.sql` and skips insertion when the same `(chain, address)` already appears (even if added previously by another exchange run).
- DB path default: `./global.db` (repo root). Override with `--global-db` if needed.
- Generate/update:
  - `updates.sql`
  - `asset_collections_updates.sql`
  - `asset_collections_mappings_updates.sql`
  - `location_asset_mappings_updates.sql`
  - `location_asset_mappings.json` (merged with existing entries, not overwritten)
- Fetch and cache missing coin details under `.coingecko_cache/coins/`.
- Populate/backfill `common_asset_details.started` for EVM assets:
  - Blockscout creation tx lookup + RPC block timestamp
  - Etherscan fallback (if available)

Usage (normal, cache-first + fetch missing):

```bash
/Users/yabirgb/work/rotki/.venv/bin/python tools/generate_certain_sql_and_mappings.py \
  testwarnings/kraken_symbols_vs_coingecko.csv \
  --updates-sql updates/40/updates.sql \
  --collections-sql updates/40/asset_collections_updates.sql \
  --mappings-sql updates/40/asset_collections_mappings_updates.sql \
  --location-mappings-sql updates/40/location_asset_mappings_updates.sql \
  --location-mappings-json updates/40/location_asset_mappings.json \
  --collection-start 1 \
  --insert-or-ignore
```

Usage (strict offline/cache-only mode):

```bash
/Users/yabirgb/work/rotki/.venv/bin/python tools/generate_certain_sql_and_mappings.py \
  testwarnings/kraken_symbols_vs_coingecko.csv \
  --updates-sql updates/40/updates.sql \
  --collections-sql updates/40/asset_collections_updates.sql \
  --mappings-sql updates/40/asset_collections_mappings_updates.sql \
  --location-mappings-sql updates/40/location_asset_mappings_updates.sql \
  --location-mappings-json updates/40/location_asset_mappings.json \
  --collection-start 1 \
  --insert-or-ignore \
  --no-fetch-missing
```

Notes:
- Idempotent behavior via dedupe checks against existing identifiers/mappings.
- `started` values are updated in-place if existing rows had `NULL`.

---

## 4) `tools/location_mappings.py` (reference utility)

Purpose:
- Reference implementation for converting location string to DB enum char and outputting location mapping SQL/JSON.

In this workflow:
- Not required to run directly.
- Its location mapping behavior is replicated in `generate_certain_sql_and_mappings.py`.

---

## Recommended run order

1. Prepare symbols file (`testwarnings/kraken_symbols.txt`)
   - either manually or via `tools/extract_from_warnings.py`
2. Ensure local `coingecko_coins.json` is fresh (periodically)
3. Run `scripts/check_symbols_against_coingecko.py`
4. Review ambiguous/missing symbols from CSV
5. Run `tools/generate_certain_sql_and_mappings.py`
6. Inspect git diff for `updates/40/*.sql` and location mapping outputs

---

## Refreshing local CoinGecko list (one-time / periodic)

```bash
curl -sS --fail 'https://api.coingecko.com/api/v3/coins/list?include_platform=true' -o coingecko_coins.json
```

Recommendation:
- Refresh this file occasionally, not on every run.

---

## Verification commands

Check generated file diffs:

```bash
git diff -- updates/40/updates.sql
git diff -- updates/40/asset_collections_updates.sql
git diff -- updates/40/asset_collections_mappings_updates.sql
git diff -- updates/40/location_asset_mappings_updates.sql
git diff -- updates/40/location_asset_mappings.json
```

Run generator tests:

```bash
/Users/yabirgb/work/rotki/.venv/bin/python -m pytest tests/test_generate_certain_sql_and_mappings.py -q
```

---

## Known limitations

- CoinGecko rate limits can skip some IDs in fetch mode.
- Ambiguous symbols (`match_count > 1`) are intentionally excluded from automation.
- Non-EVM assets or unsupported chains may keep `started = NULL`.
- Timestamp quality depends on indexer/RPC/API availability.

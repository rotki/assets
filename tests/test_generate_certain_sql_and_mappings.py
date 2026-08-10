import sqlite3
from pathlib import Path

from tools.generate_certain_sql_and_mappings import (
    COINGECKO_PLATFORM_TO_CHAIN,
    Chain,
    TokenRecord,
    choose_main_asset,
    extract_tokens_from_coin,
    find_existing_identifier_by_chain_address,
    find_existing_identifier_by_coingecko,
    load_existing_evm_address_map,
    load_collection_main_by_symbol,
    load_next_collection_id,
    merge_location_json_additions,
    parse_certain_rows,
    resolve_existing_identifier,
    token_sql,
)


def test_robinhood_chain_is_coin_gecko_only() -> None:
    assert Chain.ROBINHOOD.value == 4663
    assert COINGECKO_PLATFORM_TO_CHAIN['robinhood'] == Chain.ROBINHOOD


def test_parse_certain_rows_only_unique(tmp_path: Path) -> None:
    csv_path = tmp_path / "in.csv"
    csv_path.write_text(
        "symbol,match_count,coingecko_ids,names\n"
        "AAA,1,aaa-token,AAA\n"
        "BBB,0,,\n"
        "CCC,2,ccc1|ccc2,C1|C2\n"
    )

    assert parse_certain_rows(csv_path) == [("AAA", "aaa-token", None, None)]


def test_extract_tokens_from_coin_dedupes_and_maps_supported_chains() -> None:
    data = {
        "name": "My Token",
        "symbol": "mtk",
        "detail_platforms": {
            "ethereum": {"contract_address": "0xabc", "decimal_place": 18},
            "polygon-pos": {"contract_address": "0xdef", "decimal_place": 6},
        },
        "platforms": {
            "ethereum": "0xabc",  # duplicate
            "solana": "So11111111111111111111111111111111111111112",
            "unknown-chain": "0x123",  # ignored
        },
    }

    tokens = extract_tokens_from_coin(data)
    pairs = {(t.chain, t.address) for t in tokens}

    assert (Chain.ETHEREUM, "0xabc") in pairs
    assert (Chain.POLYGON_POS, "0xdef") in pairs
    assert (Chain.SOLANA, "So11111111111111111111111111111111111111112") in pairs
    assert len(tokens) == 3


def test_choose_main_asset_prefers_ethereum() -> None:
    tokens = [
        type("T", (), {"chain": Chain.SOLANA})(),
        type("T", (), {"chain": Chain.ETHEREUM})(),
    ]
    assert choose_main_asset(tokens).chain == Chain.ETHEREUM


def test_token_sql_uses_started_timestamp() -> None:
    token = TokenRecord(
        address="0x0000000000000000000000000000000000000abc",
        chain=Chain.ETHEREUM,
        decimals=18,
        name="Token",
        symbol="TOK",
        started=1700000000,
    )
    sql = token_sql(token, coin_id="token-id", cryptocompare_id="TOK", insert_or_ignore=True)
    assert "'TOK', NULL, 1700000000, NULL);" in sql
    assert "'token-id', 'TOK'" in sql
    assert "0x0000000000000000000000000000000000000aBc" in sql


def test_find_existing_identifier_by_chain_address(tmp_path: Path) -> None:
    db = tmp_path / "global.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE evm_tokens(identifier TEXT, chain INTEGER, address TEXT)")
        conn.execute(
            "INSERT INTO evm_tokens(identifier, chain, address) VALUES (?, ?, ?)",
            ("eip155:1/erc20:0xAbC", 1, "0xAbC"),
        )

    found = find_existing_identifier_by_chain_address(db, Chain.ETHEREUM, "0xabc")
    assert found == "eip155:1/erc20:0xAbC"


def test_resolve_existing_identifier_prefers_address_then_coingecko(tmp_path: Path) -> None:
    db = tmp_path / "global.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE evm_tokens(identifier TEXT, chain INTEGER, address TEXT)")
        conn.execute("CREATE TABLE common_asset_details(identifier TEXT, coingecko TEXT)")
        conn.execute(
            "INSERT INTO evm_tokens(identifier, chain, address) VALUES (?, ?, ?)",
            ("eip155:8453/erc20:0x111", 8453, "0x111"),
        )
        conn.execute(
            "INSERT INTO common_asset_details(identifier, coingecko) VALUES (?, ?)",
            ("eip155:1/erc20:0x999", "coin-1"),
        )

    tokens = [
        TokenRecord(address="0x111", chain=Chain.BASE, decimals=18, name="A", symbol="A"),
        TokenRecord(address="0x222", chain=Chain.ETHEREUM, decimals=18, name="A", symbol="A"),
    ]
    assert resolve_existing_identifier(db, "coin-1", tokens) == "eip155:8453/erc20:0x111"

    tokens_no_addr_match = [TokenRecord(address="0x333", chain=Chain.BASE, decimals=18, name="A", symbol="A")]
    assert find_existing_identifier_by_coingecko(db, "coin-1") == "eip155:1/erc20:0x999"
    assert resolve_existing_identifier(db, "coin-1", tokens_no_addr_match) == "eip155:1/erc20:0x999"


def test_load_existing_evm_address_map_from_updates_sql(tmp_path: Path) -> None:
    sql_path = tmp_path / "updates.sql"
    sql_path.write_text(
        "INSERT INTO evm_tokens(identifier, token_kind, chain, address, decimals, protocol) "
        "VALUES('eip155:1/erc20:0xAbC', 'A', 1, '0xAbC', 18, NULL);\n"
    )
    addr_map = load_existing_evm_address_map(sql_path)
    assert addr_map[(1, "0xabc")] == "eip155:1/erc20:0xAbC"


def test_merge_location_json_additions_preserves_existing_and_dedupes() -> None:
    existing = [
        {"asset": "a1", "location": "kraken", "location_symbol": "AAA"},
        {"asset": "a2", "location": "binance", "location_symbol": "BBB"},
    ]
    new = [
        {"asset": "a2", "location": "binance", "location_symbol": "BBB"},
        {"asset": "a3", "location": "kraken", "location_symbol": "CCC"},
    ]
    merged = merge_location_json_additions(existing, new)
    assert len(merged) == 3
    assert {tuple(x.values()) for x in merged} == {
        ("a1", "kraken", "AAA"),
        ("a2", "binance", "BBB"),
        ("a3", "kraken", "CCC"),
    }


def test_merge_location_json_additions_replaces_same_location_symbol() -> None:
    merged = merge_location_json_additions(
        [{"asset": "old", "location": "kraken", "location_symbol": "AAA"}],
        [{"asset": "new", "location": "kraken", "location_symbol": "AAA"}],
    )

    assert merged == [{"asset": "new", "location": "kraken", "location_symbol": "AAA"}]


def test_load_collection_main_by_symbol(tmp_path: Path) -> None:
    path = tmp_path / "collections.sql"
    path.write_text(
        "INSERT INTO asset_collections(id, name, symbol, main_asset) "
        "VALUES (1, 'Nesa', 'NES', 'eip155:56/erc20:0x123');\n"
    )

    assert load_collection_main_by_symbol(path) == {"NES": "eip155:56/erc20:0x123"}


def test_load_next_collection_id_prefers_collections_sql(tmp_path: Path) -> None:
    collections_sql = tmp_path / "asset_collections_updates.sql"
    collections_sql.write_text(
        "INSERT INTO asset_collections(id, name, symbol, main_asset) VALUES (10, 'A', 'A', 'a');\n"
        "INSERT INTO asset_collections(id, name, symbol, main_asset) VALUES (14, 'B', 'B', 'b');\n"
    )

    db = tmp_path / "global.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE asset_collections(id INTEGER)")
        conn.execute("INSERT INTO asset_collections(id) VALUES (999)")

    assert load_next_collection_id(collections_sql, start=1, db_path=db) == 15


def test_load_next_collection_id_falls_back_to_db_when_sql_empty(tmp_path: Path) -> None:
    collections_sql = tmp_path / "asset_collections_updates.sql"
    collections_sql.write_text("")

    db = tmp_path / "global.db"
    with sqlite3.connect(db) as conn:
        conn.execute("CREATE TABLE asset_collections(id INTEGER)")
        conn.executemany("INSERT INTO asset_collections(id) VALUES (?)", [(41,), (42,)])

    assert load_next_collection_id(collections_sql, start=1, db_path=db) == 43

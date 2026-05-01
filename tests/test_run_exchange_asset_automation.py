from pathlib import Path
import importlib.util


def _load_module():
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "run_exchange_asset_automation.py"
    spec = importlib.util.spec_from_file_location("run_exchange_asset_automation", script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_extract_unknown_symbols_kraken_format(tmp_path: Path) -> None:
    mod = _load_module()
    warnings = tmp_path / "kraken.txt"
    warnings.write_text(
        "UserWarning: Found unknown primary asset BASED in kraken.\n"
        "UserWarning: Found unknown primary asset OPN in kraken.\n"
        "UserWarning: Found unknown primary asset based in kraken.\n"
    )

    symbols = mod.extract_unknown_symbols(warnings, exchange="kraken")
    assert symbols == ["BASED", "OPN"]


def test_extract_unknown_symbols_coinbase_format(tmp_path: Path) -> None:
    mod = _load_module()
    warnings = tmp_path / "coinbase.txt"
    warnings.write_text(
        "UserWarning: Found unknown asset BASED1 with symbol BASED1 in Coinbase.\n"
        "UserWarning: Found unknown asset EDGEX with symbol EDGEX in Coinbase.\n"
        "UserWarning: Found unknown asset based1 with symbol based1 in coinbase.\n"
    )

    symbols = mod.extract_unknown_symbols(warnings, exchange="coinbase")
    assert symbols == ["BASED1", "EDGEX"]


def test_extract_unknown_symbols_ignores_other_exchanges(tmp_path: Path) -> None:
    mod = _load_module()
    warnings = tmp_path / "mixed.txt"
    warnings.write_text(
        "UserWarning: Found unknown primary asset AAA in kraken.\n"
        "UserWarning: Found unknown asset BBB with symbol BBB in Coinbase.\n"
    )

    assert mod.extract_unknown_symbols(warnings, exchange="kraken") == ["AAA"]
    assert mod.extract_unknown_symbols(warnings, exchange="coinbase") == ["BBB"]

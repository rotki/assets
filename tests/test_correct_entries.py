import json
import warnings
from pathlib import Path

import pytest
from eth_utils.address import to_checksum_address
from validator.checker import UpdateChecker
from validator.utils import get_latest_version


@pytest.fixture(name='schema_versions')
def fixture_schema_version():
    root_dir = infojson = Path(__file__).parents[1]
    infojson = root_dir / 'updates' / 'info.json'
    assert infojson.is_file()

    with open(infojson) as f:
        data = json.load(f)

    info = {}
    for version, schemas in data['updates'].items():
        info[int(version)] = schemas['max_schema_version']

    return info


@pytest.mark.parametrize('version', range(1, get_latest_version() + 1))
def test_valid_sql_sentences(version, schema_versions):
    root_dir = Path(__file__).parents[1]
    upgrade = root_dir / 'updates' / str(version) / 'updates.sql'
    updater = UpdateChecker()
    with open(upgrade) as f:
        data = f.read()
        updater.check_single_version_update(data, schema_versions[version])


@pytest.mark.parametrize('version', range(1, get_latest_version() + 1))
def test_valid_identifiers_mappings(version, schema_versions):
    """Test that identifiers have checksummed addresses in multiassets mappings"""
    root_dir = Path(__file__).parents[1]
    upgrade = root_dir / 'updates' / str(version) / 'asset_collections_mappings_updates.sql'

    if upgrade.exists() is False:
        return

    with open(upgrade) as f:
        for line in f.readlines():
            if '*' in line:
                continue
            print('---', line)
            try:
                eip_pos = line.index('eip155')
            except ValueError:
                continue  # this is not an evm token, can skip

            address = line[eip_pos:].split(':')[-1].strip().replace('");', '')
            assert to_checksum_address(address) == address

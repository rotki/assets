import json
import re
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
def test_asset_collection_mappings(version, schema_versions):
    """Test that the multiassets mappings update files are valid"""
    root_dir = Path(__file__).parents[1]
    upgrade = root_dir / 'updates' / str(version) / 'asset_collections_mappings_updates.sql'
    # keep this re in sync with the one in the main repo
    multiasset_mappings_re = re.compile(r'.*INSERT +INTO +multiasset_mappings\( *collection_id *, *asset *\) *VALUES +\(([^,]*?), *"([^,]+?)"\).*?')  # noqa: E501

    if upgrade.exists() is False:
        return

    with open(upgrade) as f:
        for line in f.readlines():
            if '*' in line:
                continue

            mappings_match = multiasset_mappings_re.match(line)
            assert mappings_match is not None
            groups = mappings_match.groups()
            assert len(groups) == 2

            lineid = int(groups[0])
            assert lineid >= 0

            identifier = groups[1]
            assert isinstance(identifier, str)
            if identifier.startswith('eip155'):
                address = identifier.split(':')[-1]
                assert to_checksum_address(address) == address


@pytest.mark.parametrize('version', range(1, get_latest_version() + 1))
def test_asset_collections_updates(version, schema_versions):
    """Test that the asset collections update files are valid"""
    root_dir = Path(__file__).parents[1]
    upgrade = root_dir / 'updates' / str(version) / 'asset_collections_updates.sql'
    # keep this re in sync with the one in the main repo
    assets_collection_re = re.compile(r'.*INSERT +INTO +asset_collections\( *id *, *name *, *symbol *\) *VALUES +\(([^,]*?),([^,]*?),([^,]*?)\).*?')  # noqa: E501

    if upgrade.exists() is False:
        return

    with open(upgrade) as f:
        for line in f.readlines():
            if '*' in line:
                continue

            collections_match = assets_collection_re.match(line)
            assert collections_match is not None
            groups = collections_match.groups()
            assert len(groups) == 3

            lineid = int(groups[0])
            assert lineid >= 0
            assert isinstance(groups[1], str)  # collection name
            assert isinstance(groups[2], str)  # collection symbol

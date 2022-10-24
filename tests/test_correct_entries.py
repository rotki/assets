import argparse
import json
from pathlib import Path

import pytest

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

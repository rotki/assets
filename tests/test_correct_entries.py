import argparse
from pathlib import Path

import pytest

from validator.checker import UpdateChecker
from validator.utils import get_latest_version

@pytest.mark.parametrize('version', range(1, get_latest_version() + 1))
def test_valid_sql_sentences(version):
    root_dir = Path(__file__).parents[1]
    upgrade = root_dir / 'updates' / str(version) / 'updates.sql'
    updater = UpdateChecker()
    with open(upgrade) as f:
        data = f.read()
        updater.check_single_version_update(data)

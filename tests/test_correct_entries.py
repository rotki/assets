import argparse
from pathlib import Path

from validator.checker import UpdateChecker
from validator import get_latest_version

def test_valid_sql_sentences():
    root_dir = Path(__file__).parents[1]
    upgrade = root_dir / 'updates' / str(get_latest_version()) / 'updates.sql'
    updater = UpdateChecker()
    with open(upgrade) as f:
        data = f.read()
        updater.check_single_version_update(data)

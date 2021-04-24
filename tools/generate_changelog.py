import argparse
from pathlib import Path

from validator.checker import UpdateChecker
from validator.utils import get_latest_version

root_dir = Path(__file__).parents[1]

if __name__ == '__main__':
    root_dir = Path(__file__).parents[1]
    parser = argparse.ArgumentParser(description='Validate update file for version')
    parser.add_argument('-v', '--version', nargs='?', default=get_latest_version(), type=int)
    args = parser.parse_args()
    upgrade = root_dir / 'updates' / str(args.version) / 'updates.sql'
    updater = UpdateChecker()
    with open(upgrade) as f:
        data = f.read()
        print(updater.generate_report(data))

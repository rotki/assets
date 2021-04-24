import json
from pathlib import Path


def get_latest_version():
    # Read latest version
    root_dir = infojson = Path(__file__).parents[1]
    infojson = root_dir / 'updates' / 'info.json'
    with open(infojson) as f:
        data = json.load(f)
    return data['latest']

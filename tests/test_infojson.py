"""
Small sanity checks

TODO: Probably should turn this into part of a pytest suite
"""
import json
from pathlib import Path

def test_valid_infojson():
    root_dir = infojson = Path(__file__).parents[1]
    infojson = root_dir / 'updates' / 'info.json'
    assert infojson.is_file()

    with open(infojson) as f:
        data = json.load(f)
    assert isinstance(data, dict)
    assert 'latest' in data
    updates = data['updates']
    for update, update_data in updates.items():
        assert update_data['min_schema_version'] <= update_data['max_schema_version']
        update_dir = root_dir / 'updates' / update
        assert update_dir.is_dir()
        update_file = update_dir / 'updates.sql'
        assert update_file.is_file()
        with open(update_file) as f:
            changes = sum(1 for line in f) / 2
        assert changes == update_data['changes']

    infojson_indented = root_dir / 'updates' / 'pretty_info.json'
    with open(infojson_indented) as f:
        assert data == json.load(f)

"""Script to automatically populate info.json

min/max schema version can't be calculated automatically so if not already existing
a constant value is given
"""
import json
from pathlib import Path


root_dir = infojson = Path(__file__).parents[1]
infojson = root_dir / 'updates' / 'info.json'
assert infojson.is_file()

with open(infojson, 'r') as f:
    infojson_data = json.load(f)
assert isinstance(infojson_data, dict)


if 'updates' not in infojson_data:
    infojson_data['updates'] = {}

latest = 0
updates_data = infojson_data['updates']
for child in (root_dir / 'updates').iterdir():
    if not child.is_dir():
        continue

    try:
        update = int(child.name)
    except ValueError:
        continue

    update_key = str(update)

    latest = max(update, latest)
    if update_key not in infojson_data['updates']:
        infojson_data['updates'][update_key] = {'min_schema_version': 0, 'max_schema_version': 0}
        print(
            f'Adding new section for update {update_key} with min/max schema versions of 0.\n'
            f'You must manually set these limits to the correct values.'
        )

    update_file = child / 'updates.sql'
    assert update_file.is_file()
    with open(update_file) as f:
        changes = int(sum(1 for line in f) / 2)
    infojson_data['updates'][update_key]['changes'] = changes

infojson_data['latest'] = latest
with open(infojson, 'w') as f:
    json.dump(infojson_data, f)

# this file is to only check the diff and is always equal to infojson
pretty_infojson = root_dir / 'updates' / 'pretty_info.json'
with open(pretty_infojson, 'w') as f:
    json.dump(infojson_data, f, indent=2)
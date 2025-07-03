import json
import re
from pathlib import Path


def get_latest_version():
    # Read latest version
    root_dir = infojson = Path(__file__).parents[1]
    infojson = root_dir / 'updates' / 'info.json'
    with open(infojson) as f:
        data = json.load(f)
    return data['latest']


REGEX_ASSETS_V2 = {
    "assets_re": re.compile(r'.*INSERT +INTO +assets *\( *identifier *, *type *, *name *, *symbol *, *started *, *swapped_for *, *coingecko *, *cryptocompare *, *details_reference *\) *VALUES\((.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)\).*?'),
    "ethereum_tokens_re": re.compile(r'.*INSERT +INTO +ethereum_tokens *\( *address *, *decimals *, *protocol *\) *VALUES *\((.*?),(.*?),(.*?)\).*'),
    "common_asset_details_re": re.compile(r'.*INSERT +INTO +common_asset_details *\( *asset_id *, *forked *\) *VALUES *\((.*?),(.*?)\).*')
}

REGEX_ASSETS_V3 = {  # Keep these in sync with the main repo ones
    "assets_re": re.compile(r'.*INSERT +INTO +assets *\( *identifier *, *name *, *type *\) *VALUES *\(([^,]*?),([^,]*?),([^,]*?)\).*?'),
    "ethereum_tokens_re": re.compile(r'.*INSERT +INTO +evm_tokens *\( *identifier *, *token_kind *, *chain *, *address *, *decimals *, *protocol *\) *VALUES *\(([^,]*?),([^,]*?),([^,]*?),([^,]*?),([^,]*?),([^,]*?)\).*'),
    "solana_tokens_re": re.compile(r'.*INSERT +INTO +solana_tokens *\( *identifier *, *token_kind *, *address *, *decimals *, *protocol *\) *VALUES *\(([^,]*?),([^,]*?),([^,]*?),([^,]*?),([^,]*?)\).*'),
    "common_asset_details_re": re.compile(r'.*INSERT +INTO +common_asset_details *\( *identifier *, *symbol *, *coingecko *, *cryptocompare *, *forked *, *started *, *swapped_for *\) *VALUES *\((.*?),(.*?),(.*?),(.*?),(.*?),([^,]*?),([^,]*?)\).*')
}

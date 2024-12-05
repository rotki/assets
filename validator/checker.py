"""
Code extracted from the rotki's updater for version 1.16.0
https://github.com/rotki/rotki/blob/8f41fcba4732fba4af563c45c34ad9ad288906a2/rotkehlchen/globaldb/updates.py
"""

import re
from typing import NamedTuple, NewType, Optional, Tuple, Union

from eth_utils import is_checksum_address

from validator.utils import REGEX_ASSETS_V2, REGEX_ASSETS_V3

T_Timestamp = int
Timestamp = NewType('Timestamp', T_Timestamp)

CHANGELOG_MSG = """
Added support for the following assets:

{}

Updated the information of the following assets:

{}
"""


class DeserializationError(Exception):
    """Raised when deserializing data from the outside and something unexpected is found"""


class ParsedAssetData(NamedTuple):
    identifier: str
    asset_type: str
    name: str
    symbol: str
    started: Optional[int]
    swapped_for: Optional[str]
    coingecko: Optional[str]
    cryptocompare: Optional[str]


class AssetData(NamedTuple):
    identifier: str
    asset_type: str
    name: str
    symbol: str
    started: Optional[int]
    swapped_for: Optional[str]
    coingecko: Optional[str]
    cryptocompare: Optional[str]
    forked: Optional[str]
    ethereum_address: Optional[str]
    protocol: Optional[str]
    decimals: Optional[int]
    chain: Optional[int]
    token_kind: Optional[str]

CHAIN_ID_TO_NAME = {
    1: 'ethereum',
    10: 'optimism',
    56: 'binance',
    100: 'gnosis',
    137: 'matic',
    250: 'fantom',
    324: 'zksync',
    42161: 'arbitrum',
    43114: 'avalanche',
    42220: 'celo',
    8453: 'base',
    534352: 'scroll',
}

# In V2 anyone can create a vault and there are some that are endorsed by yearn once they
# are battle tested. The information seen here comes from the yearn v2 graph that tracks every
# yearn v2 vault, even the ones that are not endorsed. All the vaults in yearn v2 were
# extracted from the yearn v2 graph.
DUPLICATED_NAMES = (
    'Curve Y Pool yVault',
    'ALCX yVault',
    'eCRV yVault',
    'USDC yVault',
    'LINK yVault',
    'USDT yVault',
    'RAI yVault',
    'WETH yVault',
    'sUSD yVault',
    'UNI yVault',
    'WBTC yVault',
    'HBTC yVault',
    'AAVE yVault',
    'DAI yVault',
    'SUSHI yVault',
    'COMP yVault',
    'crvRenWBTC yVault',
    'SNX yVault',
    # Compund cWBTC-2
    'Compound Wrapped BTC',
    # Tricrypto got upgraded with the same name
    'Curve.fi USD-BTC-ETH',
    'pickling Uniswap V2',
    'pickling SushiSwap LP Token',
)

DUPLICATED_SYMBOLS = (
    'yUSD',
    'yvALCX',
    'yveCRV',
    'yvUSDC',
    'yvLINK',
    'yvUSDT',
    'yvRAI',
    'yvWETH',
    'yvsUSD',
    'yvUNI',
    'yvWBTC',
    'yvAAVE',
    'yvDAI',
    'yvSUSHI',
    'yvCOMP',
    'yvcrvRenWBTC',
    'yvHBTC',
    'yvSNX',
    # Compund cWBTC-2
    'cWBTC',
    'pUNI-V2',
    'pSLP',
)

class UpdateChecker:

    def __init__(self):
        self.versions = {
            2: REGEX_ASSETS_V2,
            3: REGEX_ASSETS_V3,
            4: REGEX_ASSETS_V3,
            5: REGEX_ASSETS_V3,
            6: REGEX_ASSETS_V3,
            7: REGEX_ASSETS_V3,
            8: REGEX_ASSETS_V3,
            9: REGEX_ASSETS_V3,
        }
        self.string_re = re.compile(r'.*"(.*?)".*')
        self.test_version = 2

    def _parse_value(self, value: str) -> Optional[Union[str, int]]:
        match = self.string_re.match(value)
        if match is not None:
            return match.group(1)

        value = value.strip()
        if value == 'NULL':
            return None

        try:
            return int(value)
        except ValueError:
            return value

    def _parse_str(self, value: str, name: str, insert_text: str) -> str:
        result = self._parse_value(value)
        if not isinstance(result, str):
            raise DeserializationError(
                f'At asset DB update got invalid {name} {value} from {insert_text}',
            )
        return result

    def _parse_optional_str(self, value: str, name: str, insert_text: str) -> Optional[str]:
        result = self._parse_value(value)
        if result is not None and not isinstance(result, str):
            raise DeserializationError(
                f'At asset DB update got invalid {name} {value} from {insert_text}',
            )
        return result

    def _parse_optional_int(self, value: str, name: str, insert_text: str) -> Optional[int]:
        result = self._parse_value(value)
        if result is not None and not isinstance(result, int):
            raise DeserializationError(
                f'At asset DB update got invalid {name} {value} from {insert_text}',
            )
        return result

    def _parse_asset_data(self, insert_text: str, schema_version: int) -> ParsedAssetData:
        match = self.versions[schema_version]['assets_re'].match(insert_text)
        if match is None:
            raise DeserializationError(
                f'At asset DB update could not parse asset data out of {insert_text}',
            )
        if schema_version == 2:
            if len(match.groups()) != 9:
                raise DeserializationError(
                    f'At asset DB update could not parse asset data out of {insert_text}',
                )

            raw_type = self._parse_str(match.group(2), 'asset type', insert_text)
            asset_type = raw_type
            raw_started = self._parse_optional_int(match.group(5), 'started', insert_text)
            started = Timestamp(raw_started) if raw_started else None
            return {
                'identifier': self._parse_str(match.group(1), 'identifier', insert_text),
                'asset_type': asset_type,
                'name': self._parse_str(match.group(3), 'name', insert_text),
                'symbol': self._parse_str(match.group(4), 'symbol', insert_text),
                'started': started,
                'swapped_for': self._parse_optional_str(match.group(6), 'swapped_for', insert_text),
                'coingecko': self._parse_optional_str(match.group(7), 'coingecko', insert_text),
                'cryptocompare': self._parse_optional_str(match.group(8), 'cryptocompare', insert_text),
            }
        else:
            if len(match.groups()) != 3:
                raise DeserializationError(
                    f'At asset DB update could not parse asset data out of {insert_text}',
                )
            return {
                'identifier': self._parse_str(match.group(1), 'identifier', insert_text),
                'name': self._parse_str(match.group(2), 'name', insert_text),
                'asset_type': self._parse_str(match.group(3), 'asset type', insert_text),
            }

    def _parse_evm_token_data(self, insert_text: str, schema_version: int) -> Tuple[str, Optional[int], Optional[str]]:  # noqa: E501
        match = self.versions[schema_version]['ethereum_tokens_re'].match(insert_text)
        if match is None:
            raise DeserializationError(
                f'At asset DB update could not parse ethereum token data out '
                f'of {insert_text}',
            )

        if schema_version == 2:
            if len(match.groups()) != 3:
                raise DeserializationError(
                    f'At asset DB update could not parse ethereum token data out of {insert_text}',
                )

            return {
                'address': self._parse_str(match.group(1), 'address', insert_text),
                'decimals': self._parse_optional_int(match.group(2), 'decimals', insert_text),
                'protocol': self._parse_optional_str(match.group(3), 'protocol', insert_text),
            }
        # else
        if len(match.groups()) != 6:
            raise DeserializationError(
                f'At asset DB update could not parse ethereum token data out of {insert_text}',
            )

        return {
            'identifier': self._parse_str(match.group(1), 'identifier', insert_text),
            'token_kind': self._parse_str(match.group(2), 'token_kind', insert_text),
            'chain': self._parse_optional_int(match.group(3), 'chain', insert_text),
            'address': self._parse_str(match.group(4), 'address', insert_text),
            'decimals': self._parse_optional_int(match.group(5), 'decimals', insert_text),
            'protocol': self._parse_optional_str(match.group(6), 'protocol', insert_text),
        }

    def _parse_full_insert(self, insert_text: str, schema_version: int) -> AssetData:
        """Parses the full insert line for an asset to give information for the conflict to the user

        Note: In the future this needs to be different for each version
        May raise:
        - DeserializationError if the appropriate data is not found or if it can't
        be properly parsed.
        """
        asset_data = self._parse_asset_data(insert_text, schema_version)
        evm_data = {
            'identifier': None,
            'forked': None,
            'address': None,
            'decimals': None,
            'protocol': None,
            'chain': None,
            'token_kind': None,
        }
        if asset_data['asset_type'] == 'C':
            evm_data |= self._parse_evm_token_data(insert_text, schema_version)

        if len(asset_data['asset_type']) != 1:
            raise DeserializationError(
                f'At asset DB update could not parse asset type '
                f'details data out of {insert_text}',
            )

        if schema_version == 2 and asset_data['asset_type'] != 'C':
            match = self.versions[schema_version]['common_asset_details_re'].match(insert_text)
            common_details = {
                'forked': self._parse_optional_str(match.group(2), 'forked', insert_text),
            }
            if match is None:
                raise DeserializationError(
                    f'At asset DB update could not parse common asset '
                    f'details data out of {insert_text}',
                )
        elif schema_version == 2:
            common_details = {'forked': None}
        elif schema_version >= 3:
            match = self.versions[schema_version]['common_asset_details_re'].match(insert_text)
            if match is None:
                raise DeserializationError(
                    f'At asset DB update could not parse common asset '
                    f'details data out of {insert_text}',
                )
            assert self._parse_str(match.group(1), 'identifier', insert_text) == asset_data['identifier'], f'Identifiers of assets {asset_data["identifier"]} and common_asset_details {match.group(1)} are not same'
            if asset_data['asset_type'] == 'C':
                assert evm_data['identifier'] == asset_data['identifier'], f'Identifiers of assets {asset_data["identifier"]} and evm_token {evm_data["identifier"]} are not same'
            common_details = {
                'symbol': self._parse_optional_str(match.group(2), 'symbol', insert_text),
                'coingecko': self._parse_optional_str(match.group(3), 'coingecko', insert_text),
                'cryptocompare': self._parse_optional_str(match.group(4), 'cryptocompare', insert_text),
                'forked': self._parse_optional_str(match.group(5), 'forked', insert_text),
                'started': self._parse_optional_int(match.group(6), 'started', insert_text),
                'swapped_for': self._parse_optional_str(match.group(7), 'swapped_for', insert_text),
            }

        asset_data |= evm_data
        asset_data |= common_details

        return AssetData(  # types are not really proper here (except for asset_type)
            identifier=asset_data['identifier'],
            name=asset_data['name'],
            symbol=asset_data['symbol'],
            asset_type=asset_data['asset_type'],
            started=asset_data['started'],
            forked=asset_data['forked'],
            swapped_for=asset_data['swapped_for'],
            ethereum_address=asset_data['address'],
            decimals=asset_data['decimals'],
            cryptocompare=asset_data['cryptocompare'],
            coingecko=asset_data['coingecko'],
            protocol=asset_data['protocol'],
            token_kind=asset_data['token_kind'],
            chain=asset_data['chain'],
        )

    def check_single_version_update(
            self,
            text: str,
            schema_version: int
    ) -> None:
        lines = text.splitlines()
        seen_elements = set()
        for action, full_insert in zip(*[iter(lines)] * 2):
            insert = False
            if full_insert == '*':
                full_insert = action
                insert = True

            # Use the same regex as in the rotki repo to obtain the assets
            asset_data = self._parse_full_insert(full_insert, schema_version)

            assert asset_data.cryptocompare is not None or asset_data.coingecko is not None
            assert len(asset_data.name) != 0, f'Empty name in {asset_data}'
            assert len(asset_data.symbol) != 0
            if asset_data.asset_type == 'C' and schema_version > 2:
                assert asset_data.identifier == f'eip155:{asset_data.chain}/erc20:{asset_data.ethereum_address}', f'Mismatch in identifier, chain id, and/or address for {asset_data.identifier}'

            # Check against duplicate information. Before schema version 3 we couldn't have duplicates
            if insert and schema_version == 2:
                assert asset_data.cryptocompare not in seen_elements, f'Duplicate cryptocompare {asset_data.cryptocompare}'
                assert asset_data.coingecko not in seen_elements, f'Duplicate coingecko {asset_data.coingecko}'
                if asset_data.name not in DUPLICATED_NAMES:
                    assert asset_data.name not in seen_elements, f'Duplicate name {asset_data.name}'
                if asset_data.symbol not in DUPLICATED_SYMBOLS:
                    assert asset_data.symbol not in seen_elements, f'Duplicate symbol {asset_data.symbol}'

            # For ethereum address, make a checksum of addresses
            if asset_data.ethereum_address is not None:
                assert is_checksum_address(asset_data.ethereum_address), f'Address not checksummed in {asset_data}, {asset_data.ethereum_address}'
                assert asset_data.ethereum_address in action
                if insert:
                    assert (asset_data.ethereum_address, asset_data.chain) not in seen_elements, f'Duplicate address {asset_data.ethereum_address}-{asset_data.chain}'
                    seen_elements.add((asset_data.ethereum_address, asset_data.chain))

            if insert:
                seen_elements.update((asset_data.symbol, asset_data.name))
                if (asset_data.cryptocompare is not None) and len(asset_data.cryptocompare) != 0:
                    seen_elements.add(asset_data.cryptocompare)
                if (asset_data.coingecko is not None) and len(asset_data.coingecko) != 0:
                    seen_elements.add(asset_data.coingecko)

    def generate_report(
        self,
        text: str,
    ) -> str:
        lines = text.splitlines()
        new_assets = []
        updated_assets = []
        for action, full_insert in zip(*[iter(lines)] * 2):
            is_new = False
            if full_insert == '*':
                full_insert = action
                is_new = True
            asset_data = self._parse_full_insert(full_insert, schema_version=max(self.versions.keys()))
            if asset_data.coingecko is not None:
                msg = f'- [{asset_data.name} ({asset_data.symbol})](https://www.coingecko.com/en/coins/{asset_data.coingecko})'
            elif asset_data.cryptocompare is not None:
                msg = f'- [{asset_data.name} ({asset_data.symbol})](https://www.cryptocompare.com/coins/{asset_data.cryptocompare}/overview/)'
            else:
                msg = f'- {asset_data.name} ({asset_data.symbol})'

            if asset_data.chain is not None:
                assert asset_data.chain in CHAIN_ID_TO_NAME, f'Chain {asset_data.chain} is missing in the mapping of chains'
                msg += f' on {CHAIN_ID_TO_NAME[asset_data.chain]}'

            if is_new:
                new_assets.append(msg)
            else:
                updated_assets.append(msg)


        return CHANGELOG_MSG.format('\n'.join(new_assets), '\n'.join(updated_assets))

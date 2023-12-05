"""
Script to extract information about the assets to CSV files that can be consumed by others
"""

import csv
from enum import Enum
import sqlite3

class AssetType(Enum):
    FIAT = 1
    OWN_CHAIN = 2
    EVM_TOKEN = 3
    OMNI_TOKEN = 4
    NEO_TOKEN = 5
    COUNTERPARTY_TOKEN = 6
    BITSHARES_TOKEN = 7
    ARDOR_TOKEN = 8
    NXT_TOKEN = 9
    UBIQ_TOKEN = 10
    NUBITS_TOKEN = 11
    BURST_TOKEN = 12
    WAVES_TOKEN = 13
    QTUM_TOKEN = 14
    STELLAR_TOKEN = 15
    TRON_TOKEN = 16
    ONTOLOGY_TOKEN = 17
    VECHAIN_TOKEN = 18
    BINANCE_TOKEN = 19
    EOS_TOKEN = 20
    FUSION_TOKEN = 21
    LUNIVERSE_TOKEN = 22
    OTHER = 23
    AVALANCHE_TOKEN = 24
    SOLANA_TOKEN = 25
    NFT = 26
    CUSTOM_ASSET = 27
    @classmethod
    def deserialize_from_db(cls, value: str):
        number = ord(value)
        if number < 65 or number > list(cls)[-1].value + 64:
            raise ValueError(f'Failed to deserialize {cls.__name__} DB value {value}')
        return cls(number - 64).name.lower()


conn = sqlite3.connect('../databases/v8_global.db')
cursor = conn.cursor()

cursor.execute(
    'SELECT evm_tokens.identifier, address, chain, name, symbol, decimals, '
    'coingecko, cryptocompare, started, protocol FROM evm_tokens JOIN assets ON '
    'evm_tokens.identifier=assets.identifier JOIN common_asset_details ON '
    'common_asset_details.identifier=evm_tokens.identifier WHERE type="C"'
)
header = [
    'identifier',
    'address',
    'chain',
    'name',
    'symbol',
    'decimals',
    'coingecko',
    'cryptocompare',
    'started',
    'protocol',
] 
with open('evm_tokens.csv', 'w', newline='\n') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL, )
    wr.writerow(header)
    wr.writerows(cursor)


cursor.execute(
    'SELECT assets.identifier, name, symbol, type, coingecko, cryptocompare, started FROM assets '
    'JOIN common_asset_details ON common_asset_details.identifier=assets.identifier WHERE type!="C"'
)

header = [
    'identifier',
    'name',
    'symbol',
    'type',
    'coingecko',
    'cryptocompare',
    'started',
] 
with open('other_assets.csv', 'w', newline='\n') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL, )
    wr.writerow(header)
    for row in cursor:
        row = list(row)
        row[3] = str(AssetType.deserialize_from_db(row[3]))
        wr.writerow(row)


cursor.execute('SELECT id, name, symbol FROM asset_collections')
header = [
    'identifier',
    'name',
    'symbol',
] 
with open('assets_collections.csv', 'w', newline='\n') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL, )
    wr.writerow(header)
    wr.writerows(cursor)


cursor.execute('SELECT collection_id, asset FROM multiasset_mappings')
header = [
    'collection_identifier',
    'asset',
] 
with open('multiassets_mappings.csv', 'w', newline='\n') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_MINIMAL, )
    wr.writerow(header)
    wr.writerows(cursor)
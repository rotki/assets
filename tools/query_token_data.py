from dateutil import parser as dp
import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Literal

from web3 import Web3, HTTPProvider
from web3.middleware import ExtraDataToPOAMiddleware
import requests
from eth_utils.address import to_checksum_address

API_KEY = ""  # loaded on run and saved to config file
CONFIG_FILE = '.token_query_config.json'
COLLECTION_IDX = 400
ERC20_ABI = """[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]"""

# Identifier Templates
EVM_IDENTIFIER = 'eip155:{blockchain}/erc20:{address}'
SOLANA_IDENTIFIER = 'solana/token:{address}'

# SQL Query Templates
ASSETS_QUERY = "INSERT INTO assets(identifier, name, type) VALUES('{identifier}', '{name}', 'C'); "
EVM_TOKENS_QUERY = "INSERT INTO evm_tokens(identifier, token_kind, chain, address, decimals, protocol) VALUES('{identifier}', 'A', {blockchain}, '{address}', {decimals}, {protocol}); "
SOLANA_TOKENS_QUERY = "INSERT INTO solana_tokens(identifier, token_kind, address, decimals, protocol) VALUES('{identifier}', 'D', '{address}', {decimals}, {protocol}); "
COMMON_ASSET_DETAILS_QUERY = "INSERT INTO common_asset_details(identifier, symbol, coingecko, cryptocompare, forked, started, swapped_for) VALUES('{identifier}', '{symbol}', '{coingecko}', '{cryptocompare}', NULL, {deployed_at}, NULL);"
UNDERLYING_TOKEN_QUERY = " INSERT INTO underlying_tokens_list(identifier, weight, parent_token_entry) VALUES('{underlying_identifier}', '1', '{parent_identifier}');"
ASSET_COLLECTION_QUERY = "INSERT INTO asset_collections(id, name, symbol, main_asset) VALUES ({collection}, '{name}', '{symbol}', '{main_asset}');"
ASSET_MAPPING_QUERY = "INSERT INTO multiasset_mappings(collection_id, asset) VALUES ({collection}, '{identifier}');"


class Chain(Enum):
    """Supported blockchains and their chain IDs."""
    SOLANA = 999999999999999999  # arbitrary id just to allow solana to be part of the same enum
    ETHEREUM = 1
    BINANCE = 56
    BASE = 8453
    ARBITRUM_ONE = 42161
    OPTIMISM = 10
    POLYGON_POS = 137
    GNOSIS = 100
    SCROLL = 534352
    FANTOM = 250
    AVALANCHE = 43114
    ARBITRUM_NOVA = 42170
    CRONOS = 25
    ZKSYNC = 324


CHAINS_TO_COINGECKO_IDS = {  # id used on coingecko for each chain
    Chain.ETHEREUM: "ethereum",
    Chain.OPTIMISM: "optimistic-ethereum",
    Chain.BINANCE: "binance-smart-chain",
    Chain.GNOSIS: "xdai",
    Chain.POLYGON_POS: "polygon-pos",
    Chain.FANTOM: "fantom",
    Chain.ARBITRUM_ONE: "arbitrum-one",
    Chain.AVALANCHE: "avalanche",
    Chain.ARBITRUM_NOVA: "arbitrum-nova",
    Chain.BASE: "base",
    Chain.CRONOS: "cronos",
    Chain.SCROLL: "scroll",
    Chain.ZKSYNC: "zksync",
    Chain.SOLANA: "solana",
}
RPC_PROVIDERS = {  # RPC endpoints for each supported chain
    Chain.ETHEREUM: "https://eth.llamarpc.com",
    Chain.BINANCE: "https://binance.llamarpc.com",
    Chain.POLYGON_POS: "https://polygon.drpc.org",
    Chain.AVALANCHE: "https://avax.meowrpc.com",
    Chain.FANTOM: "https://1rpc.io/ftm",
    Chain.OPTIMISM: "https://mainnet.optimism.io",
    Chain.ARBITRUM_ONE: "https://arbitrum.meowrpc.com",
    Chain.GNOSIS: "https://rpc.gnosischain.com",
    Chain.ARBITRUM_NOVA: "https://arbitrum-nova.drpc.org",
    Chain.BASE: "https://base.llamarpc.com",
    Chain.CRONOS: "https://cronos.drpc.org",
    Chain.SCROLL: "https://scroll.drpc.org",
    Chain.ZKSYNC: "https://1rpc.io/zksync2-era",
}


@dataclass
class TokenInfo:
    name: str | None = None
    symbol: str | None = None
    timestamp: int | None = None
    chain: Chain | None = None
    address: str | None = None
    decimals: int | None = None
    protocol: str = "NULL"
    underlying_tokens: list[str] = field(default_factory=list)

    def identifier(self) -> str:
        """Get the identifier for this token."""
        if self.chain == Chain.SOLANA:
            return SOLANA_IDENTIFIER.format(address=self.address)
        else:
            return EVM_IDENTIFIER.format(blockchain=self.chain.value, address=self.address)

    def get_address(self) -> None:
        self.address = get_input(prompt='Contract Address', default=(old_address := self.address))
        if self.address != old_address:
            try:  # properly checksum the address if EVM and set chain so default is on a likely value when selecting chain next
                self.address = to_checksum_address(self.address)
                self.chain = Chain.ETHEREUM
            except ValueError:
                self.chain = Chain.SOLANA

    def get_chain(self) -> None:
        self.chain = get_chain_selection(default=self.chain)

    def get_decimals(self) -> None:
        if self.decimals is None:
            self.decimals = 9 if self.chain == Chain.SOLANA else 18

        self.decimals = int(get_input(prompt='Decimals', default=self.decimals, validate_fn=lambda x: x.isdigit()))

    def get_name(self) -> None:
        self.name = get_input(prompt='Token Name', default=self.name)

    def get_symbol(self) -> None:
        self.symbol = get_input(prompt='Token Symbol', default=self.symbol)

    def get_timestamp(self) -> None:
        while True:
            deployed_time = get_input(prompt='Deployed at (date or timestamp)', default=self.timestamp)
            if deployed_time.isdigit():
                self.timestamp = int(deployed_time)
                return
            else:
                try:
                    if ' +UTC' in deployed_time:  # dates from solscan have a plus here that confuses the time parser
                        deployed_time = deployed_time.replace(' +UTC', ' UTC')

                    self.timestamp = int(dp.parse(deployed_time.strip()).timestamp())
                    return
                except Exception:
                    print("Invalid date format. Please enter a valid date or timestamp.")
                    continue

    def get_protocol(self) -> None:
        self.protocol = get_input(prompt='Protocol', default=self.protocol)

    def get_underlying_tokens(self) -> None:
        if get_yes_no(prompt='Add underlying tokens?', default='n'):
            self.underlying_tokens = []
            print("\nEnter underlying token identifiers (press Enter on empty line to finish):")
            while True:
                if not (identifier := input(f"Underlying token {len(self.underlying_tokens) + 1}: ").strip()):
                    break
                self.underlying_tokens.append(identifier)
                print(f"Added: {identifier}")


@dataclass
class CollectionInfo:
    tokens: list[TokenInfo]
    main_asset: TokenInfo | None = None
    coingecko_id: str = ""
    cryptocompare_id: str | None = None


def print_header(header: str, level: Literal[0, 1] = 0, space_above: bool = False) -> None:
    separator = "=" * 60 if level == 0 else "-" * 50
    new_line = "\n" if space_above else ""
    print(f'{new_line}{separator}\n{header}\n{separator}')


def get_yes_no(prompt: str, default: str = 'n') -> bool:
    """Get yes/no input from user."""
    response = get_input(
        prompt=f"{prompt} (y/n)",
        default=default,
        validate_fn=lambda x: x.lower() in ['y', 'n', 'yes', 'no'],
    )
    return response.lower() in ['y', 'yes']


def get_input(prompt: str, default=None, validate_fn=None) -> str:
    """Get input with optional default value and validation."""
    while True:
        default_str = f" [{default}]" if default is not None else ""
        value = input(f"{prompt}{default_str}: ").strip()
        if default is not None and value == '':
            value = str(default)
        if validate_fn is None or validate_fn(value):
            return value


def get_item_selection(items: list[str], header: str, prompt: str, default=None) -> str | None:
    """Allows the user to select an item from a list, with an optional default choice."""
    print(header)
    default_index = None
    for idx, item in enumerate(items, start=1):
        print(f"{idx:2d}. {item}")
        if item == default:
            default_index = idx

    while True:
        try:
            if 1 <= (choice := int(get_input(prompt=prompt, default=default_index))) <= len(items):
                return items[choice - 1]
            print(f"Invalid choice. Please enter a number between 1 and {len(items)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_chain_selection(default: Chain | None = Chain.ETHEREUM) -> Chain:
    return Chain[get_item_selection(
        items=[x.name for x in Chain],
        header="Available chains:",
        default=default.name if default is not None else None,
        prompt="Select chain",
    )]


def get_deployed_ts(address: str, chain: Chain) -> int | str:
    """Retrieves the token deployment tx hash and then the timestamp of that tx."""
    try:
        tx_hash = requests.get(
            url=f"https://api.etherscan.io/v2/api?chainid={chain.value}&module=contract&action=getcontractcreation&contractaddresses={address}&apikey={API_KEY}",
        ).json()["result"][0]["txHash"]
        web3_provider = Web3(HTTPProvider(RPC_PROVIDERS[chain]))
        web3_provider.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
        return web3_provider.eth.get_block(
            block_identifier=web3_provider.eth.get_transaction(tx_hash)["blockNumber"]
        )["timestamp"]
    except Exception as e:
        print(f"Could not fetch deployment timestamp: {e}")
        return "NULL"


def fetch_evm_token_info(address: str, chain: Chain) -> TokenInfo:
    """Fetch token information from etherscan and web3 RPCs."""
    print(f"Querying token info for {address} on {chain.name}...")
    address = to_checksum_address(address)
    web3_provider = Web3(HTTPProvider(RPC_PROVIDERS[chain]))
    contract = web3_provider.eth.contract(address=address, abi=ERC20_ABI)
    name = contract.functions.name().call()
    decimals = contract.functions.decimals().call()
    symbol = contract.functions.symbol().call()
    timestamp = get_deployed_ts(address=address, chain=chain)
    print(f"Found token: {name} ({symbol}) with {decimals} decimals deployed at {timestamp}")
    return TokenInfo(
        address=address,
        chain=chain,
        decimals=decimals,
        name=name,
        symbol=symbol,
        timestamp=timestamp,
    )


def query_coingecko_data(address: str, chain: Chain) -> tuple[str, str, str, list[tuple[str, Chain, int]]] | None:
    """Query Coingecko API for token data.
    Returns tuple(coingecko_id, name, symbol, list[address, chain, decimals])
    """
    print(f"\nQuerying Coingecko...")
    try:
        data = requests.get(f"https://api.coingecko.com/api/v3/coins/{CHAINS_TO_COINGECKO_IDS[chain]}/contract/{address}").json()
        if (coingecko_id := data.get('id')) is None:
            return None

        tokens, coingecko_to_chain = [], {v: k for k, v in CHAINS_TO_COINGECKO_IDS.items()}
        for platform, details in data.get('detail_platforms', {}).items():
            if (chain := coingecko_to_chain.get(platform)) is not None:
                tokens.append(((addr := details['contract_address']), chain, details['decimal_place']))
                print(f"Found {chain.name} token: {addr}")
            else:  # we don't have this chain in our chain enum
                print(f'Skipping unsupported platform: {platform}')

        return coingecko_id, data['name'], data['symbol'], tokens
    except Exception as e:
        print(f"Error querying Coingecko: {e}")
        return None


def process_collection(collection: CollectionInfo) -> None:
    """Process a collection of tokens and generate SQL queries."""
    global COLLECTION_IDX
    if len(collection.tokens) > 1:
        COLLECTION_IDX = int(get_input(
            prompt='Enter collection index',
            default=str(COLLECTION_IDX + 1),
            validate_fn=lambda x: x.isdigit(),
        ))

    # Generate SQL queries for each token
    main_query_str = ""
    for token in collection.tokens:
        format_kwargs = {
            "identifier": token.identifier(),
            "name": token.name,
            "symbol": token.symbol,
            "decimals": token.decimals,
            "protocol": token.protocol,
            "blockchain": token.chain.value,
            "address": token.address if token.chain == Chain.SOLANA else to_checksum_address(token.address),
            "coingecko": collection.coingecko_id,
            "cryptocompare": collection.cryptocompare_id,
            "deployed_at": token.timestamp,
        }
        main_query_str += ASSETS_QUERY.format(**format_kwargs)
        main_query_str += (SOLANA_TOKENS_QUERY if token.chain == Chain.SOLANA else EVM_TOKENS_QUERY).format(**format_kwargs)
        main_query_str += COMMON_ASSET_DETAILS_QUERY.format(**format_kwargs)
        main_query_str += " ".join([
            UNDERLYING_TOKEN_QUERY.format(
                underlying_identifier=underlying_identifier,
                parent_identifier=token.identifier(),
            ) for underlying_identifier in token.underlying_tokens
        ])
        main_query_str += f'\n*\n'

    print_header("updates.sql", level=1, space_above=True)
    print(main_query_str)

    if len(collection.tokens) > 1:  # only do the collection queries for multiple tokens
        collection_query = ASSET_COLLECTION_QUERY.format(
            collection=COLLECTION_IDX,
            name=collection.main_asset.name,
            symbol=collection.main_asset.symbol,
            main_asset=collection.main_asset.identifier(),
        )
        print_header("asset_collections_updates.sql", level=1)
        print(f'{collection_query}\n*\n')

        mapping_query_str = ""
        for token in collection.tokens:
            mapping_query = ASSET_MAPPING_QUERY.format(collection=COLLECTION_IDX, identifier=token.identifier())
            mapping_query_str += f'{mapping_query}\n*\n'
        print_header("asset_collections_mappings_updates.sql", level=1)
        print(mapping_query_str)


def edit_collection_details(collection: CollectionInfo, edit_existing: bool = False) -> CollectionInfo:
    """Edit the details of a collection. Allows setting the Cryptocompare ID and main asset."""
    if collection.cryptocompare_id is None or edit_existing:
        collection.cryptocompare_id = get_input(prompt="\nCryptocompare ID", default=collection.cryptocompare_id)
    if len(collection.tokens) > 1 and edit_existing:
        default_option = None
        asset_map = {}
        for token in collection.tokens:
            asset_map[f"{token.name} ({token.symbol}) with address {token.address} on {token.chain.name}"] = token
            if token == collection.main_asset:
                default_option = f"{token.name} ({token.symbol}) with address {token.address} on {token.chain.name}"

        collection.main_asset = asset_map[get_item_selection(
            items=list(asset_map.keys()),
            default=default_option,
            header="Collection Tokens",
            prompt="Select Main Asset",
        )]

    return collection


def edit_token_details(
        token_info: TokenInfo | None = None,
        edit_existing: bool = False,
) -> TokenInfo:
    creating_new_token = False
    if token_info is None:
        creating_new_token = True
        token_info = TokenInfo()
    elif edit_existing and len(info_strings := [
        f'{k.capitalize()}: {v}'
        for k, v in asdict(token_info).items() if v is not None
    ]) > 0:
        print(f'\nEditing Existing Token - {", ".join(info_strings)}')

    print('\nEnter token information:')
    if creating_new_token and token_info.chain != Chain.SOLANA:
        token_info.get_address()
        token_info.get_chain()
        try:  # attempt to query evm token details if we are creating a new token
            return fetch_evm_token_info(address=token_info.address, chain=token_info.chain)
        except Exception as e:
            print(f"Failed to query token info for {token_info.address} on {token_info.chain}: {e}")
            print('Please enter token information manually.')

    for attr in ('address', 'chain', 'name', 'symbol', 'decimals', 'timestamp', 'protocol', 'underlying_tokens'):
        if edit_existing or (
            getattr(token_info, attr) is None and  # no existing value
            attr not in ('protocol', 'underlying_tokens')  # skip these uncommon attributes unless editing an existing token
        ):
            getattr(token_info, f'get_{attr}')()

    return token_info


def load_tokens_by_address():
    """Process tokens starting from a contract address."""
    print_header("New Asset Collection...", space_above=True)
    token_info = TokenInfo()
    token_info.get_address()
    token_info.get_chain()

    # Try to fetch from Coingecko
    if (coingecko_data := query_coingecko_data(address=token_info.address, chain=token_info.chain)) is None:
        print("\nToken not found on Coingecko. Token details must be entered manually.")
        token_info = edit_token_details(token_info=token_info)
        collection = CollectionInfo(tokens=[token_info], main_asset=token_info)
    else:
        coingecko_id, token_name, token_symbol, token_addresses = coingecko_data
        print(f"Found on Coingecko: {token_name} ({token_symbol}) with API ID: {coingecko_id}")
        tokens, main_asset = [], None
        for _address, _chain, _decimals in token_addresses:
            if _chain != Chain.SOLANA:
                try:
                    tokens.append(_token_info := fetch_evm_token_info(address=_address, chain=_chain))
                    if _chain == Chain.ETHEREUM:
                        main_asset = _token_info
                    continue
                except Exception as e:
                    print(f"Error fetching token info for {_address} on {_chain.name}: {e}")

            tokens.append(edit_token_details(token_info=TokenInfo(
                address=_address,
                chain=_chain,
                decimals=_decimals,
                name=token_name,
                symbol=token_symbol,
            )))

        if not main_asset and len(tokens) > 0:
            main_asset = tokens[0]

        collection = CollectionInfo(tokens=tokens, main_asset=main_asset, coingecko_id=coingecko_id)

    collection = edit_collection_details(collection)
    while True:
        print_header("Current Asset Collection:", level=1, space_above=True)
        print(f"Coingecko ID: {collection.coingecko_id or 'None'}")
        print(f"Cryptocompare ID: {collection.cryptocompare_id or 'None'}")
        print(f"Tokens:")
        for token in collection.tokens:
            chain_name = token.chain.name if token.chain else "Unknown"
            main_str = " **MAIN ASSET**" if token == collection.main_asset else ""
            print(f"  - {token.name} ({token.symbol}) with address {token.address} on {chain_name}{main_str}")

        finish_option = 'Finish and generate SQL'
        add_token_option = 'Add another token to collection'
        edit_tokens_option = 'Edit tokens details'
        edit_metadata_option = 'Edit collection details'
        cancel_option = 'Discard collection and start over'
        choice = get_item_selection(
            items=[finish_option, add_token_option, edit_tokens_option, edit_metadata_option, cancel_option],
            default=finish_option,
            header="\nNext action:",
            prompt="Select",
        )
        if choice == add_token_option:
            collection.tokens.append(edit_token_details())
        elif choice == edit_tokens_option:
            for idx, token in enumerate(collection.tokens):
                collection.tokens[idx] = edit_token_details(token_info=token, edit_existing=True)
        elif choice == edit_metadata_option:
            collection = edit_collection_details(collection=collection, edit_existing=True)
        elif choice == finish_option:
            process_collection(collection)
            break
        else:
            print("Cancelled.")
            break


if __name__ == "__main__":
    print(
        "Asset Info Query Tool - Query Coingecko, Etherscan, etc for token data and generate SQL queries.\n"
        "Press Ctrl+C to exit."
    )

    try:  # Load API key
        with open(CONFIG_FILE, 'r') as f:
            API_KEY = json.load(f)['api_key']
            print('\nLoaded Etherscan API key from config file.')
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        while True:
            if (API_KEY := input("\nEnter your Etherscan API key: ").strip()):
                with open(CONFIG_FILE, 'w') as f:
                    json.dump({'api_key': API_KEY}, f)
                print(f"API key saved to {CONFIG_FILE}")
                break
            print("API key cannot be empty.")

    try:  # Run main loop
        while True:
            load_tokens_by_address()
    except KeyboardInterrupt:
        print("\nExiting...")

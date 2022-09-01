# Rotki assets

This repository contains the rotki assets database and all the asset addition upgrades.

## How to add new assets

Assets are pulled from the master branch for releases and from develop for all other ways of running rotki.

So when we make a new release develop should be merged to master.

Updates are organized in the appropriate directories under ``updates``. Each updates has its own directory and sql file. For example update 1 would be: ``updates/1/updates.sql``.

Each sql file contains a number of statements. For each changes introduced we need to have two lines. The first line is the actual change such as

```
UPDATE assets SET swapped_for="eip155:1/erc20:0x1B175474E89094C44Da98b954EedeAC495271d0F" WHERE identifier="eip155:1/erc20:0xC2FEC534c461c45533e142f724d0e3930650929c";
```

or

```
INSERT INTO assets(identifier,type, started, swapped_for) VALUES("eip155:1/erc20:0xC2FEC534c461c45533e142f724d0e3930650929c", "C", 123, NULL); INSERT INTO evm_tokens(identifier, token_kind, chain, address, decimals, protocol) VALUES("eip155:1/erc20:0xC2FEC534c461c45533e142f724d0e3930650929c", "A", "A", "0xC2FEC534c461c45533e142f724d0e3930650929c", 18, NULL); INSERT INTO common_asset_details(identifier, name, symbol, coingecko, cryptocompare, forked) VALUES("eip155:1/erc20:0xC2FEC534c461c45533e142f724d0e3930650929c", "AKB token", "AKB", NULL, "AIDU", NULL);
```

and the second line needs to be a simple insertion statement. If the first line, the actual change, is also just inserting a new asset then the seconde line can simply be an ``*`` which means "the same thing".

Make sure that the `updates/info.json` file is always kept up to date with the updates, the amount of changes in each update and what's the min/max schema that each update can be applied to.

Only the last one needs to be done manually. The rest can be taken care of by running the ``populate_infojson.py`` script.

### Adding evm tokens

```
INSERT INTO assets(identifier,type, started, swapped_for) VALUES("eip155:1/erc20:0x422866a8F0b032c5cf1DfBDEf31A20F4509562b0", "C", 123, NULL); INSERT INTO evm_tokens(identifier, token_kind, chain, address, decimals, protocol) VALUES("eip155:1/erc20:0xC2FEC534c461c45533e142f724d0e3930650929c", "A", "A", "0xC2FEC534c461c45533e142f724d0e3930650929c", 18, NULL); INSERT INTO common_asset_details(identifier, name, symbol, coingecko, cryptocompare, forked) VALUES("eip155:1/erc20:0x422866a8F0b032c5cf1DfBDEf31A20F4509562b0", "Adshares", "ADST", "adshares", "ADS", NULL);
```

An evm token addition needs to look like the above. First an insertion into the `assets` table:

- **identifier**: The asset identifier.
- **asset_type**: The type of the asset. Must be one of the characters from [here](https://github.com/rotki/rotki/blob/c7a133e00a7cceb0ef84eab16488f056ceb0dae1/rotkehlchen/globaldb/schema.py#L29).
- **swapped_for**: Optional, can be ``NULL``. A string representing the identifier of the asset this asset can be swapped for. For example GLM for GNT.
- **started**: Optional, can be ``NULL``. An integer representing a Unix timestamp for when the asset started existing.

Second insertion into the `common_asset_details` table:

- **identifier**: The asset identifier.
- **name**: The name of the asset. Can also technically be ``NULL`` but should be avoided.
- **symbol**: The symbol of the asset. Can also technically be ``NULL`` but should be avoided.
- **coingecko**: Optional, can be ``NULL``. A string representing the coingecko identifier for the asset.
- **cryptocompare**: Optional, can be ``NULL``. A string representing the cryptocompare identifier for the asset.
- **forked**: Optional value representing another asset out of which this asset is forked from.

And then insert into the `evm_tokens` table:

- **identifier**: The asset identifier.
- **token_kind**: Type of the token. Supports values can be found [here](https://github.com/rotki/rotki/blob/c434df2561ce4ccfe967713f8fb626ed405440d1/rotkehlchen/globaldb/schema.py#L98)
- **chain**: Chain of the token. Supported values can be found [here](https://github.com/rotki/rotki/blob/c434df2561ce4ccfe967713f8fb626ed405440d1/rotkehlchen/globaldb/schema.py#L74)
- **address**: A valid AND checksummed evm address
- **decimals**: The decimals of the ethereum token. An integer. 0-18. Can also technically be ``NULL`` but should be avoided.
- **protocol**: Optional. Can be ``NULL``. The protocol of the ethereum token. For example ``"uniswap"`` for uniswap LP tokens e.t.c.

### Adding other assets

```
INSERT INTO assets(identifier,type, started, swapped_for) VALUES("121-ada-FADS-as", "F", NULL, NULL); INSERT INTO common_asset_details(identifier, name, symbol, coingecko, cryptocompare, forked) VALUES("121-ada-FADS-as", "A name", "SYMBOL", "", "", "BTC");
```

A non evm token addition needs to look like the above. It should be an insertion to the `assets` and `common_asset_details` table for exactly the same fields as outlined in the previous section.

## Test your changes

To detect some errors we have a test that checks every entry:

1. Install the dependencies with

        pip install -r requirements.txt

2. Run the tests with

        pytest tests

## Generate a list of changes

To generate a list of changes for a specific version use

    python -m tools.generate_changelog -v 1

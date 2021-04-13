# Rotki assets

This repository contains the rotki assets database and all the asset addition upgrades.

## How to add new assets

Assets are pulled from the master branch for releases and from develop for all other ways of running rotki.

So when we make a new release develop should be merged to master.

Updates are organized in the appropriate directories under ``updates``. Each updates has its own directory and sql file. For example update 1 would be: ``updates/1/updates.sql``.

Each sql file contains a number of statements. For each changes introduced we need to have two lines. The first line is the actual change such as

```
UPDATE assets SET swapped_for="_ceth_0xA8d35739EE92E69241A2Afd9F513d41021A07972" WHERE identifier="_ceth_0xa74476443119A942dE498590Fe1f2454d7D4aC0d";
```

or

```
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xa74476443119A942dE498590Fe1f2454d7D4aC0d", 18, NULL);INSERT INTO assets(identifier,type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xa74476443119A942dE498590Fe1f2454d7D4aC0d", "C", "Golem", "GNT", 1478810650, "_ceth_0xA8d35739EE92E69241A2Afd9F513d41021A07972", "golem", NULL, "0xa74476443119A942dE498590Fe1f2454d7D4aC0d");
```

and the second line needs to be a simple insertion statement. If the first line, the actual change, is also just inserting a new asset then the seconde line can simply be an ``*`` which means "the same thing".

Make sure that the `updates/info.json` file is always kept up to date with the updates and the amount of changes in each update.

### Adding ethereum tokens

```
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x6B175474E89094C44Da98b954EedeAC495271d0F", 8, "maker");INSERT INTO assets(identifier,type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x6B175474E89094C44Da98b954EedeAC495271d0F", "C", "New Multi Collateral DAI", "NDAI", 1573672677, NULL, "dai", NULL, "0x6B175474E89094C44Da98b954EedeAC495271d0F");
```

An ethereum token addition needs to look like the above. First an insertion into the ethereum tokens table for address, decimals, protocol.

Valid values are:

- **address**: A valid AND checksummed ethereum address
- **decimals**: The decimals of the ethereum token. An integer. 0-18. Can also technically be ``NULL`` but should be avoided.
- **protocol**: Optional. Can be ``NULL``. The protocol of the ethereum token. For example ``"uniswap"`` for uniswap LP tokens e.t.c.

And then to the all assets table.

- **identifier**: The asset identifier. _ceth_0xaddress, for tokens.
- **asset_type**: The type of the asset. Must be one of the characters from [here](https://github.com/rotki/rotki/blob/c7a133e00a7cceb0ef84eab16488f056ceb0dae1/rotkehlchen/globaldb/schema.py#L29).
- **name**: The name of the asset. Can also technically be ``NULL`` but should be avoided.
- **symbol**: The symbol of the asset. Can also technically be ``NULL`` but should be avoided.
- **started**: Optional, can be ``NULL``. An integer representing a Unix timestamp for when the asset started existing.
- **swapped_for**: Optional, can be ``NULL``. An string representing the identifier of the asset this asset can be swapped for. For example GLM for GNT.
- **coingecko**: Optional, can be ``NULL``. A string representing the coingecko identifier for the asset.
- **coingecko**: Optional, can be ``NULL``. A string representing the cryptocompare identifier for the asset.
- **details_reference**: This is the link to the tokens or to the common asset details table. It's the address for ethereum tokens and the asset identifier for assets.

### Adding other assets

```
INSERT INTO assets(identifier,type,name,symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("121-ada-FADS-as", "F","A name","SYMBOL",NULL, NULL,"", "", "121-ada-FADS-as");INSERT INTO common_asset_details(asset_id, forked) VALUES("121-ada-FADS-as", "BTC");
```

A non ethereum token addition needs to look like the above. First is an insertion to the assets table for exactly the same fields as outlined in the previous section.

Then an addition to the common asset details which at the moment consist only of:

- **asset_id**: This is the asset identifier.
- **forked**: Optional. Can be ``NULL``. This is the asset identifier of the asset from which this asset was forked if any. For example for `BCH` this is `BTC` and for `ETC` this is `ETH`.

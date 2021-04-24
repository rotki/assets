UPDATE assets SET cryptocompare="SOL" WHERE identifier="SOL-2";/*Update cryptocompare identifier for Solana*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("SOL-2", "B", "Solana", "SOL", 1586494758, NULL, "solana", "SOL", "SOL-2"); INSERT INTO common_asset_details(asset_id, forked) VALUES("SOL-2", NULL);
UPDATE assets SET coingecko="gochain", cryptocompare="GO" WHERE identifier="GO";/*Update coingecko identifier for GoChain*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("GO", "B", "GoChain", "GO", 1526428800, NULL, "gochain", "GO", "GO"); INSERT INTO common_asset_details(asset_id, forked) VALUES("GO", NULL);

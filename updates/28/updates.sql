UPDATE common_asset_details SET coingecko="extra-finance" WHERE identifier="eip155:10/erc20:0x2dAD3a13ef0C6366220f989157009e501e7938F8";
INSERT INTO assets(identifier, name, type) VALUES("eip155:10/erc20:0x2dAD3a13ef0C6366220f989157009e501e7938F8", "Extra Finance", "C"); INSERT INTO evm_tokens(identifier, token_kind, chain, address, decimals, protocol) VALUES("eip155:10/erc20:0x2dAD3a13ef0C6366220f989157009e501e7938F8", "A", 10, "0x2dAD3a13ef0C6366220f989157009e501e7938F8", 18, ""); INSERT INTO common_asset_details(identifier, symbol, coingecko, cryptocompare, forked, started, swapped_for) VALUES("eip155:10/erc20:0x2dAD3a13ef0C6366220f989157009e501e7938F8", "EXTRA", "extra-finance", "EXTRA", NULL, 1684751172, NULL);
UPDATE common_asset_details SET coingecko="extra-finance", cryptocompare="EXTRA" WHERE identifier="eip155:8453/erc20:0x2dAD3a13ef0C6366220f989157009e501e7938F8";
INSERT INTO assets(identifier, name, type) VALUES("eip155:8453/erc20:0x2dAD3a13ef0C6366220f989157009e501e7938F8", "Extra Finance", "C"); INSERT INTO evm_tokens(identifier, token_kind, chain, address, decimals, protocol) VALUES("eip155:8453/erc20:0x2dAD3a13ef0C6366220f989157009e501e7938F8", "A", 8453, "0x2dAD3a13ef0C6366220f989157009e501e7938F8", 18, ""); INSERT INTO common_asset_details(identifier, symbol, coingecko, cryptocompare, forked, started, swapped_for) VALUES("eip155:8453/erc20:0x2dAD3a13ef0C6366220f989157009e501e7938F8", "EXTRA", "extra-finance", "EXTRA", NULL, 1690955247, NULL);
UPDATE common_asset_details SET cryptocompare="WELL" WHERE identifier="WELL";
INSERT INTO assets(identifier, name, type) VALUES("WELL", "Extra Finance", "W"); INSERT INTO common_asset_details(identifier, symbol, coingecko, cryptocompare, forked, started, swapped_for) VALUES("WELL", "WELL", "moonwell-artemis", "WELL", NULL, 1652303490, NULL);

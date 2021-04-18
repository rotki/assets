INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xaac41EC512808d64625576EDdd580e7Ea40ef8B2", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xaac41EC512808d64625576EDdd580e7Ea40ef8B2", "C", "Gameswap", "GSWAP", 1604022038, NULL, "gameswap-org", "GSWAP", "0xaac41EC512808d64625576EDdd580e7Ea40ef8B2");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x88ACDd2a6425c3FaAE4Bc9650Fd7E27e0Bebb7aB", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x88ACDd2a6425c3FaAE4Bc9650Fd7E27e0Bebb7aB", "C", "Alchemist", "MIST", 1612643126, NULL, "alchemist", "MIST", "0x88ACDd2a6425c3FaAE4Bc9650Fd7E27e0Bebb7aB");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0", "C", "Tellor", "TRB", 1613850551, NULL, "tellor", "TRB", "0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0");
*
UPDATE assets SET swapped_for="_ceth_0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0" WHERE identifier="_ceth_0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5";/*Introduce TRB token swap*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5", "C", "Tellor Tributes", "TRB", 1564671864, "_ceth_0x88dF592F8eb5D7Bd38bFeF7dEb0fBc02cf3778a0", "tellor", "TRB", "0x0Ba45A8b5d5575935B8158a88C631E9F9C95a2e5");
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xaea46A60368A7bD060eec7DF8CBa43b7EF41Ad85", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xaea46A60368A7bD060eec7DF8CBa43b7EF41Ad85", "C", "Fetch AI", "FET", 1601931978, NULL, "fetch-ai", "FET", "0xaea46A60368A7bD060eec7DF8CBa43b7EF41Ad85");
*
UPDATE assets SET swapped_for="_ceth_0xaea46A60368A7bD060eec7DF8CBa43b7EF41Ad85" WHERE identifier="_ceth_0x1D287CC25dAD7cCaF76a26bc660c5F7C8E2a05BD";/*Introduce FET token swap*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x1D287CC25dAD7cCaF76a26bc660c5F7C8E2a05BD", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x1D287CC25dAD7cCaF76a26bc660c5F7C8E2a05BD", "C", "Fetch AI", "FET", 1538999375, "_ceth_0xaea46A60368A7bD060eec7DF8CBa43b7EF41Ad85", "fetch-ai", "FET", "0x1D287CC25dAD7cCaF76a26bc660c5F7C8E2a05BD");
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x767FE9EDC9E0dF98E07454847909b5E959D7ca0E", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x767FE9EDC9E0dF98E07454847909b5E959D7ca0E", "C", "Illuvium", "ILV", 1616355826, NULL, "illuvium", "ILV", "0x767FE9EDC9E0dF98E07454847909b5E959D7ca0E");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x7dE91B204C1C737bcEe6F000AAA6569Cf7061cb7", 9, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x7dE91B204C1C737bcEe6F000AAA6569Cf7061cb7", "C", "Robonomics Network", "XRT", 1555493324, NULL, "robonomics-network", "XRT", "0x7dE91B204C1C737bcEe6F000AAA6569Cf7061cb7");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x054D64b73d3D8A21Af3D764eFd76bCaA774f3Bb2", 18, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x054D64b73d3D8A21Af3D764eFd76bCaA774f3Bb2", "C", "Plasma Finance", "PPAY", 1604406754, NULL, "plasma-finance", "", "0x054D64b73d3D8A21Af3D764eFd76bCaA774f3Bb2");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xF94b5C5651c888d928439aB6514B93944eEE6F48", 18, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xF94b5C5651c888d928439aB6514B93944eEE6F48", "C", "YIELD App", "YLD", 1607697368, NULL, "yield-app", "YLD", "0xF94b5C5651c888d928439aB6514B93944eEE6F48");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x8a40c222996f9F3431f63Bf80244C36822060f12", 18, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x8a40c222996f9F3431f63Bf80244C36822060f12", "C", "Finxflo", "FXF", 1612679229, NULL, "finxflo", "FXF", "0x8a40c222996f9F3431f63Bf80244C36822060f12");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x661Ab0Ed68000491d98C796146bcF28c20d7c559", 18, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x661Ab0Ed68000491d98C796146bcF28c20d7c559", "C", "Shadows", "DOWS", 1614615544, NULL, "shadows", "DOWS", "0x661Ab0Ed68000491d98C796146bcF28c20d7c559");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xBBc2AE13b23d715c30720F079fcd9B4a74093505", 18, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xBBc2AE13b23d715c30720F079fcd9B4a74093505", "C", "Ethernity Chain", "ERN", 1611899325, NULL, "ethernity-chain", "ERN", "0xBBc2AE13b23d715c30720F079fcd9B4a74093505");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xD2dDa223b2617cB616c1580db421e4cFAe6a8a85", 18, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xD2dDa223b2617cB616c1580db421e4cFAe6a8a85", "C", "Bondly", "BONDLY", 1607343988, NULL, "bondly", "BONDLY", "0xD2dDa223b2617cB616c1580db421e4cFAe6a8a85");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xdBdb4d16EdA451D0503b854CF79D55697F90c8DF", 18, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xdBdb4d16EdA451D0503b854CF79D55697F90c8DF", "C", "Alchemix", "ALCX", 1614400082, NULL, "alchemix", "ALCX", "0xdBdb4d16EdA451D0503b854CF79D55697F90c8DF");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x420412E765BFa6d85aaaC94b4f7b708C89be2e2B", 4, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x420412E765BFa6d85aaaC94b4f7b708C89be2e2B", "C", "Brazilian Digital Token", "BRZ", 1552417004, NULL, "brazilian-digital-token", "BRZ", "0x420412E765BFa6d85aaaC94b4f7b708C89be2e2B");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xcca0c9c383076649604eE31b20248BC04FdF61cA", 18, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xcca0c9c383076649604eE31b20248BC04FdF61cA", "C", "Bitmax Token", "BTMX", 1590380637, NULL, "bmax", "BTMX", "0xcca0c9c383076649604eE31b20248BC04FdF61cA");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xc834Fa996fA3BeC7aAD3693af486ae53D8aA8B50", 18, NULL); INSERT INTO assets(identifier, type, name, symbol,started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xc834Fa996fA3BeC7aAD3693af486ae53D8aA8B50", "C", "Convergence", "CONV", 1616385987, NULL, "convergence", "CONV", "0xc834Fa996fA3BeC7aAD3693af486ae53D8aA8B50");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("COPE", "Y", "Cope", "COPE", 1617077337, NULL, "cope", "COPE", "COPE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("COPE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("CRON", "B", "Cryptocean", "CRON", 1557885600, NULL, "cryptocean", "CRON", "CRON"); INSERT INTO common_asset_details(asset_id, forked) VALUES("CRON", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("FIDA", "Y", "Bonfida", "FIDA", 1608598800, NULL, "bonfida", "FIDA", "FIDA"); INSERT INTO common_asset_details(asset_id, forked) VALUES("FIDA", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("HOLY", "Y", "Holy Trinity", "HOLY", 1609894800, NULL, "holy-trinity", "", "HOLY"); INSERT INTO common_asset_details(asset_id, forked) VALUES("HOLY", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x3E9BC21C9b189C09dF3eF1B824798658d5011937", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x3E9BC21C9b189C09dF3eF1B824798658d5011937", "C", "Linear", "LINA", 1600266838, NULL, "linear", "LINA", "0x3E9BC21C9b189C09dF3eF1B824798658d5011937");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xB1f66997A5760428D3a87D68b90BfE0aE64121cC", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xB1f66997A5760428D3a87D68b90BfE0aE64121cC", "C", "LuaToken", "LUA", 1601024188, NULL, "lua-token", "LUA", "0xB1f66997A5760428D3a87D68b90BfE0aE64121cC");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x08d967bb0134F2d07f7cfb6E246680c53927DD30", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x08d967bb0134F2d07f7cfb6E246680c53927DD30", "C", "MATH Token", "MATH", 1569577860, NULL, "math", "MATH", "0x08d967bb0134F2d07f7cfb6E246680c53927DD30");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x965697b4ef02F0DE01384D0d4F9F782B1670c163", 6, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x965697b4ef02F0DE01384D0d4F9F782B1670c163", "C", "Oxygen Ecosystem Token", "OXY", 1607784270, NULL, "oxygen", "OXY", "0x965697b4ef02F0DE01384D0d4F9F782B1670c163");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x0FD10b9899882a6f2fcb5c371E17e70FdEe00C38", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x0FD10b9899882a6f2fcb5c371E17e70FdEe00C38", "C", "Pundi X Token", "PUNDIX", 1615175880, NULL, "pundi-x-2", "PUNDIX", "0x0FD10b9899882a6f2fcb5c371E17e70FdEe00C38");
*
UPDATE assets SET swapped_for="_ceth_0x0FD10b9899882a6f2fcb5c371E17e70FdEe00C38" WHERE identifier="_ceth_0xA15C7Ebe1f07CaF6bFF097D8a589fb8AC49Ae5B3";/*Introduce NPXS token swap*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xA15C7Ebe1f07CaF6bFF097D8a589fb8AC49Ae5B3", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xA15C7Ebe1f07CaF6bFF097D8a589fb8AC49Ae5B3", "C", "Pundi X", "NPXS", 1506470400, "_ceth_0x0FD10b9899882a6f2fcb5c371E17e70FdEe00C38", "pundi-x", "NPXS", "0xA15C7Ebe1f07CaF6bFF097D8a589fb8AC49Ae5B3");
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x33D0568941C0C64ff7e0FB4fbA0B11BD37deEd9f", 6, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x33D0568941C0C64ff7e0FB4fbA0B11BD37deEd9f", "C", "RAMP DEFI", "RAMP", 1597966623, NULL, "ramp", "RAMP", "0x33D0568941C0C64ff7e0FB4fbA0B11BD37deEd9f");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("RAY", "Y", "Raydium", "RAY", 1613927088, NULL, "raydium", "RAY", "RAY"); INSERT INTO common_asset_details(asset_id, forked) VALUES("RAY", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xAC51066d7bEC65Dc4589368da368b212745d63E8", 6, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xAC51066d7bEC65Dc4589368da368b212745d63E8", "C", "ALICE", "ALICE", 1614689017, NULL, "my-neighbor-alice", "ALICE", "0xAC51066d7bEC65Dc4589368da368b212745d63E8");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("BIFI", "S", "Beefy.Finance", "BIFI", 1600620892, NULL, "beefy-finance", "BIFI", "BIFI"); INSERT INTO common_asset_details(asset_id, forked) VALUES("BIFI", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("CFX", "B", "Conflux Token", "CFX", 1604970000, NULL, "conflux-token", "CFX", "CFX"); INSERT INTO common_asset_details(asset_id, forked) VALUES("CFX", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("EPS", "S", "Ellipsis", "EPS", 1616517644, NULL, "ellipsis", "ELLIP", "EPS"); INSERT INTO common_asset_details(asset_id, forked) VALUES("EPS", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x57B946008913B82E4dF85f501cbAeD910e58D26C", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x57B946008913B82E4dF85f501cbAeD910e58D26C", "C", "Marlin POND", "POND", 1608108114, NULL, "marlin", "POND", "0x57B946008913B82E4dF85f501cbAeD910e58D26C");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xe53EC727dbDEB9E2d5456c3be40cFF031AB40A55", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xe53EC727dbDEB9E2d5456c3be40cFF031AB40A55", "C", "SuperFarm", "SUPER", 1613866257, NULL, "superfarm", "SUPER", "0xe53EC727dbDEB9E2d5456c3be40cFF031AB40A55");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("TKO", "S", "Tokocrypto Token", "TKO", 1617298253, NULL, "tokocrypto", "TKO", "TKO"); INSERT INTO common_asset_details(asset_id, forked) VALUES("TKO", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x888888848B652B3E3a0f34c96E00EEC0F3a23F72", 4, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x888888848B652B3E3a0f34c96E00EEC0F3a23F72", "C", "Alien Worlds Trilium", "TLM", 1613920019, NULL, "alien-worlds", "TLM", "0x888888848B652B3E3a0f34c96E00EEC0F3a23F72");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x725C263e32c72dDC3A19bEa12C5a0479a81eE688", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x725C263e32c72dDC3A19bEa12C5a0479a81eE688", "C", "Bridge Mutual", "BMI", 1611958204, NULL, "bridge-mutual", "BMI", "0x725C263e32c72dDC3A19bEa12C5a0479a81eE688");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x1B073382E63411E3BcfFE90aC1B9A43feFa1Ec6F", 8, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x1B073382E63411E3BcfFE90aC1B9A43feFa1Ec6F", "C", "Bitpanda Ecosystem Token", "BEST", 1564487711, NULL, "bitpanda-ecosystem-token", "BEST", "0x1B073382E63411E3BcfFE90aC1B9A43feFa1Ec6F");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x738865301A9b7Dd80Dc3666dD48cF034ec42bdDa", 8, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x738865301A9b7Dd80Dc3666dD48cF034ec42bdDa", "C", "Agoras Token", "AGRS", 1610671100, NULL, "agoras", "AGRS", "0x738865301A9b7Dd80Dc3666dD48cF034ec42bdDa");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x2001f2A0Cf801EcFda622f6C28fb6E10d803D969", 8, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x2001f2A0Cf801EcFda622f6C28fb6E10d803D969", "C", "CoinLoan", "CLT", 1518798365, NULL, "coinloan", "", "0x2001f2A0Cf801EcFda622f6C28fb6E10d803D969");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xe2DA716381d7E0032CECaA5046b34223fC3f218D", 5, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xe2DA716381d7E0032CECaA5046b34223fC3f218D", "C", "Carbon Utility Token", "CUT", 1615231734, NULL, "carbon-utility-token", "", "0xe2DA716381d7E0032CECaA5046b34223fC3f218D");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xb1f871Ae9462F1b2C6826E88A7827e76f86751d4", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xb1f871Ae9462F1b2C6826E88A7827e76f86751d4", "C", "GNYerc20", "GNYerc20", 1615231734, NULL, "gny", "GNY", "0xb1f871Ae9462F1b2C6826E88A7827e76f86751d4");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x68a9d92Fe19399FEEBEd6A9a0980a7ea7638074C", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x68a9d92Fe19399FEEBEd6A9a0980a7ea7638074C", "C", "Iqoniq", "IQQ", 1615386735, NULL, "iqoniq", "", "0x68a9d92Fe19399FEEBEd6A9a0980a7ea7638074C");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xdfbc9050F5B01DF53512DCC39B4f2B2BBaCD517A", 8, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xdfbc9050F5B01DF53512DCC39B4f2B2BBaCD517A", "C", "Jobchain", "JOB", 1579390502, NULL, "jobchain", "JOB", "0xdfbc9050F5B01DF53512DCC39B4f2B2BBaCD517A");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xF9e5aF7B42D31D51677c75bbBD37c1986eC79AEE", 8, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xF9e5aF7B42D31D51677c75bbBD37c1986eC79AEE", "C", "QuickX Protocol", "QCX", 1548185499, NULL, "quickx-protocol", "QCX", "0xF9e5aF7B42D31D51677c75bbBD37c1986eC79AEE");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xAd4f86a25bbc20FfB751f2FAC312A0B4d8F88c64", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xAd4f86a25bbc20FfB751f2FAC312A0B4d8F88c64", "C", "OptionRoom Token", "ROOM", 1611783103, NULL, "option-room", "", "0xAd4f86a25bbc20FfB751f2FAC312A0B4d8F88c64");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x0AeE8703D34DD9aE107386d3eFF22AE75Dd616D1", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x0AeE8703D34DD9aE107386d3eFF22AE75Dd616D1", "C", "Tranche Finance", "SLICE", 1609247971, NULL, "tranche-finance", "SLICE", "0x0AeE8703D34DD9aE107386d3eFF22AE75Dd616D1");
*
UPDATE assets SET swapped_for="_ceth_0x0AeE8703D34DD9aE107386d3eFF22AE75Dd616D1" WHERE identifier="_ceth_0xa5Fd1A791C4dfcaacC963D4F73c6Ae5824149eA7";/*Introduce Tranche Finance token swap*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xa5Fd1A791C4dfcaacC963D4F73c6Ae5824149eA7", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xa5Fd1A791C4dfcaacC963D4F73c6Ae5824149eA7", "C", "Jibrel Network Token", "JNT", 1552845272, "_ceth_0x0AeE8703D34DD9aE107386d3eFF22AE75Dd616D1", "jibrel", "JNT", "0xa5Fd1A791C4dfcaacC963D4F73c6Ae5824149eA7");
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x9B02dD390a603Add5c07f9fd9175b7DABE8D63B7", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x9B02dD390a603Add5c07f9fd9175b7DABE8D63B7", "C", "Shopping.io", "SPI", 1607010551, NULL, "shopping-io", "SPI", "0x9B02dD390a603Add5c07f9fd9175b7DABE8D63B7");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x74232704659ef37c08995e386A2E26cc27a8d7B1", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x74232704659ef37c08995e386A2E26cc27a8d7B1", "C", "Strike Token", "STRK", 1615435564, NULL, "strike", "STRK", "0x74232704659ef37c08995e386A2E26cc27a8d7B1");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xE748269494e76c1ceC3F627bb1e561E607dA9161", 8, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xE748269494e76c1ceC3F627bb1e561E607dA9161", "C", "Xels Token", "XELS", 1613731292, NULL, "xels", "XELS", "0xE748269494e76c1ceC3F627bb1e561E607dA9161");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("WAXP", "B", "WAX", "WAXP", 1528419600, NULL, "wax", "WAXP", "WAXP"); INSERT INTO common_asset_details(asset_id, forked) VALUES("WAXP", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("WIN", "P", "WINk", "WIN", 1562532570, NULL, "wink", "WIN", "WIN"); INSERT INTO common_asset_details(asset_id, forked) VALUES("WIN", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("DON", "B", "Donnie Finance", "DON", 1615954083, NULL, "donnie-finance", "", "DON"); INSERT INTO common_asset_details(asset_id, forked) VALUES("DON", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xD478161C952357F05f0292B56012Cd8457F1cfbF", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xD478161C952357F05f0292B56012Cd8457F1cfbF", "C", "Polkamarkets", "POLK", 1613820933, NULL, "polkamarkets", "POLK", "0xD478161C952357F05f0292B56012Cd8457F1cfbF");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xf1f955016EcbCd7321c7266BccFB96c68ea5E49b", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xf1f955016EcbCd7321c7266BccFB96c68ea5E49b", "C", "Rally", "RLY", 1601929393, NULL, "rally-2", "RLY", "0xf1f955016EcbCd7321c7266BccFB96c68ea5E49b");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x06A01a4d579479Dd5D884EBf61A31727A3d8D442", 8, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x06A01a4d579479Dd5D884EBf61A31727A3d8D442", "C", "SmartKey", "SKEY", 1598617685, NULL, "smartkey", "SKEY", "0x06A01a4d579479Dd5D884EBf61A31727A3d8D442");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x0fF6ffcFDa92c53F615a4A75D982f399C989366b", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x0fF6ffcFDa92c53F615a4A75D982f399C989366b", "C", "Unilayer", "LAYER", 1597515254, NULL, "unilayer", "LAYER", "0x0fF6ffcFDa92c53F615a4A75D982f399C989366b");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xF001937650bb4f62b57521824B2c20f5b91bEa05", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xF001937650bb4f62b57521824B2c20f5b91bEa05", "C", "Taraxa Coin", "TARA", 1616051569, NULL, "taraxa", "TARA", "0xF001937650bb4f62b57521824B2c20f5b91bEa05");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("XYM", "B", "Symbol", "XYM", 1616131249, NULL, "symbol", "XYM", "XYM"); INSERT INTO common_asset_details(asset_id, forked) VALUES("XYM", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x961C8c0B1aaD0c0b10a51FeF6a867E3091BCef17", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x961C8c0B1aaD0c0b10a51FeF6a867E3091BCef17", "C", "DeFiYieldProtocol", "DYP", 1601843568, NULL, "defi-yield-protocol", "DYP", "0x961C8c0B1aaD0c0b10a51FeF6a867E3091BCef17");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("PCX", "B", "ChainX", "PCX", 1564624800, NULL, "chainx", "PCX", "PCX"); INSERT INTO common_asset_details(asset_id, forked) VALUES("PCX", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x3aFfCCa64c2A6f4e3B6Bd9c64CD2C969EFd1ECBe", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x3aFfCCa64c2A6f4e3B6Bd9c64CD2C969EFd1ECBe", "C", "DSLA", "DSLA", 1601843568, NULL, "stacktical", "DSLA", "0x3aFfCCa64c2A6f4e3B6Bd9c64CD2C969EFd1ECBe");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("FLUX", "B", "Flux", "FLUX", 1564624800, NULL, "zelcash", "", "FLUX"); INSERT INTO common_asset_details(asset_id, forked) VALUES("FLUX", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("GSPI", "S", "SPI Governance", "GSPI", 1614967129, NULL, "gspi", "GSPI", "GSPI"); INSERT INTO common_asset_details(asset_id, forked) VALUES("GSPI", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xE1c7E30C42C24582888C758984f6e382096786bd", 8, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xE1c7E30C42C24582888C758984f6e382096786bd", "C", "Curate", "XCUR", 1587031895, NULL, "curate", "XCUR", "0xE1c7E30C42C24582888C758984f6e382096786bd");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x635d081fD8F6670135D8a3640E2cF78220787d56", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x635d081fD8F6670135D8a3640E2cF78220787d56", "C", "ADD", "ADD", 1615201125, NULL, "add-xyz-new", "ADD", "0x635d081fD8F6670135D8a3640E2cF78220787d56");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xf3dcbc6D72a4E1892f7917b7C43b74131Df8480e", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xf3dcbc6D72a4E1892f7917b7C43b74131Df8480e", "C", "BDPToken", "BDP", 1614842471, NULL, "big-data-protocol", "BDP", "0xf3dcbc6D72a4E1892f7917b7C43b74131Df8480e");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xb753428af26E81097e7fD17f40c88aaA3E04902c", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xb753428af26E81097e7fD17f40c88aaA3E04902c", "C", "Spice", "SFI", 1604135425, NULL, "saffron-finance", "SFI", "0xb753428af26E81097e7fD17f40c88aaA3E04902c");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("ADAHALF", "W", "0.5X Long Cardano Token", "ADAHALF", 1602986400, NULL, "0-5x-long-cardano-token", "ADAHALF", "ADAHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("ADAHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("ADAHEDGE", "W", "1X Short Cardano Token", "ADAHEDGE", 1596852000, NULL, "1x-short-cardano-token", "ADAHEDGE", "ADAHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("ADAHEDGE", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x057FB10e3fec001a40e6B75D3a30B99e23e54107", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x057FB10e3fec001a40e6B75D3a30B99e23e54107", "C", "3X Short Algorand Token", "ALGOBEAR", 1566118908, NULL, "3x-short-algorand-token", "ALGOBEAR", "0x057FB10e3fec001a40e6B75D3a30B99e23e54107");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x584936357D68f5143F12e2e64F0089dB93814dAd", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x584936357D68f5143F12e2e64F0089dB93814dAd", "C", "3X Long Algorand Token", "ALGOBULL", 1566117837, NULL, "3x-long-algorand-token", "ALGOBULL", "0x584936357D68f5143F12e2e64F0089dB93814dAd");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("ALGOHALF", "W", "0.5X Long Algorand Token", "ALGOHALF", 1597740237, NULL, "0-5x-long-algorand-token", "ALGOHALF", "ALGOHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("ALGOHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xfdc3D57eB7839ca68A2fAD7A93799c8e8aFA61B7", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xfdc3D57eB7839ca68A2fAD7A93799c8e8aFA61B7", "C", "1X Short Algorand Token", "ALGOHEDGE", 1566119012, NULL, "1x-short-algorand-token", "ALGOHEDGE", "0xfdc3D57eB7839ca68A2fAD7A93799c8e8aFA61B7");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x90B417Ab462440Cf59767BCf72D0d91CA42F21ED", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x90B417Ab462440Cf59767BCf72D0d91CA42F21ED", "C", "3X Short Altcoin Index Token", "ALTBEAR", 1566118892, NULL, "3x-short-altcoin-index-token", "ALTBEAR", "0x90B417Ab462440Cf59767BCf72D0d91CA42F21ED");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xd829664CDbF3195b2cE76047A65de29e7ED0a9A8", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xd829664CDbF3195b2cE76047A65de29e7ED0a9A8", "C", "3X Long Altcoin Index Token", "ALTBULL", 1566117832, NULL, "3x-long-altcoin-index-token", "ALTBULL", "0xd829664CDbF3195b2cE76047A65de29e7ED0a9A8");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("ALTHALF", "W", "0.5X Long Algorand Token", "ALTHALF", 1603332000, NULL, "0-5x-long-altcoin-index-token", "ALTHALF", "ALTHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("ALTHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x258FEc90B7788E60dA3bc6f81d5839Dc5B36a110", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x258FEc90B7788E60dA3bc6f81d5839Dc5B36a110", "C", "1X Short Altcoin Index Token", "ALTHEDGE", 1566118867, NULL, NULL, "ALTHEDGE", "0x258FEc90B7788E60dA3bc6f81d5839Dc5B36a110");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x3B834A620751A811f65D8f599b3b72617A4418d0", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x3B834A620751A811f65D8f599b3b72617A4418d0", "C", "3X Short Cosmos Token", "ATOMBEAR", 1580720206, NULL, "3x-short-cosmos-token", "ATOMBEAR", "0x3B834A620751A811f65D8f599b3b72617A4418d0");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x75F0038B8fbfCCAFe2aB9a51431658871bA5182C", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x75F0038B8fbfCCAFe2aB9a51431658871bA5182C", "C", "3X Long Cosmos Token", "ATOMBULL", 1580720064, NULL, "3x-long-cosmos-token", "ATOMBULL", "0x75F0038B8fbfCCAFe2aB9a51431658871bA5182C");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("ATOMHALF", "W", "0.5X Long Cosmos Token", "ATOMHALF", 1597024824, NULL, "0-5x-long-cosmos-token", "ATOMHALF", "ATOMHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("ATOMHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("ATOMHEDGE", "W", "1X Short Cosmos Token", "ATOMHEDGE", 1597024824, NULL, "1x-short-cosmos-token", "ATOMHEDGE", "ATOMHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("ATOMHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("BALBEAR", "W", "3X Short Balancer Token", "BALBEAR", 1618510059, NULL, "3x-short-balancer-token", "BALBEAR", "BALBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("BALBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("BALBULL", "W", "3X Long Balancer Token ", "BALBULL", 1596679200, NULL, "3x-long-balancer-token", "BALBULL", "BALBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("BALBULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("BALHALF", "W", "0.5X Long Balancer Token", "BALHALF", 1604451600, NULL, "0-5x-long-balancer-token", "BALHALF", "BALHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("BALHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("BALHEDGE", "W", "1X Short Balancer Token", "BALHEDGE", 1616000400, NULL, NULL, "BALHEDGE", "BALHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("BALHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("BCHHALF", "W", "0.5X Long Bitcoin Cash Token", "BCHHALF", 1596722400, NULL, "0-5x-long-bitcoin-cash-token", "BCHHALF", "BCHHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("BCHHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x02E88a689fdfB920e7Aa6174Fb7AB72add3C5694", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x02E88a689fdfB920e7Aa6174Fb7AB72add3C5694", "C", "1X Short Bitcoin Cash Token", "BCHHEDGE", 1566117917, NULL, "1x-short-bitcoin-cash-token", "BCHHEDGE", "0x02E88a689fdfB920e7Aa6174Fb7AB72add3C5694");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x48dEE19C81B89A9aB473361bAE7a19210f2DEaA4", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x48dEE19C81B89A9aB473361bAE7a19210f2DEaA4", "C", "3X Short Shitcoin Index Token", "BEARSHIT", 1566118923, NULL, "3x-short-shitcoin-index-token", "BEARSHIT", "0x48dEE19C81B89A9aB473361bAE7a19210f2DEaA4");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("BNBHALF", "W", "0.5X Long BNB Token", "BNBHALF", 1616000400, NULL, NULL, "BNBHALF", "BNBHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("BNBHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x2840aD41cf25Ad58303Ba24C416E79dCe4161b4F", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x2840aD41cf25Ad58303Ba24C416E79dCe4161b4F", "C", "1X Short BNB Token", "BNBHEDGE", 1558089174, NULL, "1x-short-bnb-token", "BNBHEDGE", "0x2840aD41cf25Ad58303Ba24C416E79dCe4161b4F");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("BSVHALF", "W", "0.5X Long Bitcoin SV Token", "BSVHALF", 1596679200, NULL, "0-5x-long-bitcoin-sv-token", "BSVHALF", "BSVHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("BSVHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("BSVHEDGE", "W", "1X Short Bitcoin SV Token", "BSVHEDGE", 1558089174, NULL, NULL, "BSVHEDGE", "BSVHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("BSVHEDGE", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x81824663353A9d29b01B2DE9dd9a2Bb271d298cD", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x81824663353A9d29b01B2DE9dd9a2Bb271d298cD", "C", "Bitcoin Volatility Token", "BVOL", 1587558092, NULL, "1x-long-btc-implied-volatility-token", "BVOL", "0x81824663353A9d29b01B2DE9dd9a2Bb271d298cD");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("COMPBEAR", "W", "3X Short Compound Token Token", "COMPBEAR", 1596679200, NULL, "3x-short-compound-token-token", "COMPBEAR", "COMPBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("COMPBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("COMPBULL", "W", "3X Long Compound Token Token", "COMPBULL", 1596679200, NULL, "3x-long-compound-token-token", "COMPBULL", "COMPBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("COMPBULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("COMPHALF", "W", "0.5X Long Compound Token Token", "COMPHALF", 1616997600, NULL, NULL, "COMPHALF", "COMPHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("COMPHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("COMPHEDGE", "W", "1X Short Compound Token Token", "COMPHEDGE", 1597111200, NULL, "1x-short-compound-token-token", "COMPHEDGE", "COMPHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("COMPHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("CUSDTBEAR", "W", "3X Short Compound USDT Token", "CUSDTBEAR", 1597370400, NULL, "3x-short-compound-usdt-token", "CUSDTBEAR", "CUSDTBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("CUSDTBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("CUSDTBULL", "W", "3X Long Compound USDT Token", "CUSDTBULL", 1596852000, NULL, "3x-long-compound-usdt-token", "CUSDTBULL", "CUSDTBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("CUSDTBULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("CUSDTHALF", "W", "0.5X Long Compound USDT Token", "CUSDTHALF", 1616000400, NULL, NULL, "CUSDTHALF", "CUSDTHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("CUSDTHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("CUSDTHEDGE", "W", "1X Short Compound USDT Token", "CUSDTHEDGE", 1604451600, NULL, "1x-short-compound-usdt-token", "CUSDTHEDGE", "CUSDTHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("CUSDTHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("DEFIBEAR", "W", "3X Short DeFi Index Token", "DEFIBEAR", 1596679200, NULL, "3x-short-defi-index-token", "DEFIBEAR", "DEFIBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("DEFIBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("DEFIBULL", "W", "3X Long DeFi Index Token", "DEFIBULL", 1596679200, NULL, "3x-long-defi-index-token", "DEFIBULL", "DEFIBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("DEFIBULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("DEFIHALF", "W", "0.5X Long DeFi Index Token", "DEFIHALF", 1597111200, NULL, "0-5x-long-defi-index-token", "DEFIHALF", "DEFIHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("DEFIHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("DEFIHEDGE", "W", "1X Short DeFi Index Token", "DEFIHEDGE", 1597111200, NULL, "1x-short-defi-index-token", "DEFIHEDGE", "DEFIHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("DEFIHEDGE", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xF1d32952E2fbB1a91e620b0FD7fBC8a8879A47f3", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xF1d32952E2fbB1a91e620b0FD7fBC8a8879A47f3", "C", "3X Short Dogecoin Token", "DOGEBEAR", 1580720370, NULL, "3x-short-dogecoin-token", "DOGEBEAR", "0xF1d32952E2fbB1a91e620b0FD7fBC8a8879A47f3");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x7AA6b33fB7F395DDBca7b7A33264A3c799Fa626f", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x7AA6b33fB7F395DDBca7b7A33264A3c799Fa626f", "C", "3X Long Dogecoin Token", "DOGEBULL", 1580719995, NULL, "3x-long-dogecoin-token", "DOGEBULL", "0x7AA6b33fB7F395DDBca7b7A33264A3c799Fa626f");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("DOGEHALF", "W", "0.5X Long Dogecoin Token", "DOGEHALF", 1604451600, NULL, "0-5x-long-dogecoin-token", "DOGEHALF", "DOGEHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("DOGEHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("DOGEHEDGE", "W", "1X Short Dogecoin Token", "DOGEHEDGE", 1597111200, NULL, "1x-short-dogecoin-token", "DOGEHEDGE", "DOGEHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("DOGEHEDGE", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x223FB5c14C00Cfb70cF56BB63c2EeF2d74fE1A78", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x223FB5c14C00Cfb70cF56BB63c2EeF2d74fE1A78", "C", "3X Short Dragon Index Token", "DRGNBEAR", 1580720232, NULL, "3x-short-dragon-index-token", "DRGNBEAR", "0x223FB5c14C00Cfb70cF56BB63c2EeF2d74fE1A78");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x3335f16AF9008bFd32f1eE6C2Be5d4f84FA0b9da", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x3335f16AF9008bFd32f1eE6C2Be5d4f84FA0b9da", "C", "3X Long Dragon Index Token", "DRGNBULL", 1580720553, NULL, "3x-long-dragon-index-token", "DRGNBULL", "0x3335f16AF9008bFd32f1eE6C2Be5d4f84FA0b9da");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("DRGNHALF", "W", "0.5X Long Dragon Index Token", "DRGNHALF", 1604451600, NULL, "0-5x-long-dragon-index-token", "DRGNHALF", "DRGNHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("DRGNHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("DRGNHEDGE", "W", "1X Short Dragon Index Token", "DRGNHEDGE", 1604451600, NULL, NULL, "DRGNHEDGE", "DRGNHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("DRGNHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("EOSHALF", "W", "0.5X Long EOS Token", "EOSHALF", 1597370400, NULL, "0-5x-long-eos-token", "EOSHALF", "EOSHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("EOSHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xA340f0937a8c00DB11C83Cc16CEC12310160F0b6", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xA340f0937a8c00DB11C83Cc16CEC12310160F0b6", "C", "3X Short Ethereum Classic Token", "ETCBEAR", 1570234070, NULL, "3x-short-ethereum-classic-token", "ETCBEAR", "0xA340f0937a8c00DB11C83Cc16CEC12310160F0b6");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x974c98Bc2e82FA18de92B7e697A1D9BD25682e80", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x974c98Bc2e82FA18de92B7e697A1D9BD25682e80", "C", "3X Long Ethereum Classic Token", "ETCBULL", 1570234100, NULL, "3x-long-ethereum-classic-token", "ETCBULL", "0x974c98Bc2e82FA18de92B7e697A1D9BD25682e80");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("ETCHALF", "W", "0.5X Long Ethereum Classic Token", "ETCHALF", 1596679200, NULL, "0-5x-long-ethereum-classic-token", "ETCHALF", "ETCHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("ETCHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("ETCHEDGE", "W", "1X Short Ethereum Classic Token", "ETCHEDGE", 1592787600, NULL, NULL, "ETCHEDGE", "ETCHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("ETCHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("ETHHALF", "W", "0.5X Long Ethereum Token", "ETHHALF", 1596765600, NULL, "0-5x-long-ethereum-token", "ETHHALF", "ETHHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("ETHHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x10e1E953DDBa597011f8bFA806aB0cC3415a622b", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x10e1E953DDBa597011f8bFA806aB0cC3415a622b", "C", "1X Short Ethereum Token", "ETHHEDGE", 1552911672, NULL, "1x-short-ethereum-token", "ETHHEDGE", "0x10e1E953DDBa597011f8bFA806aB0cC3415a622b");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x6baA91cd8AA07431760EF2eedFedCEF662A6B8B3", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x6baA91cd8AA07431760EF2eedFedCEF662A6B8B3", "C", "3X Short Exchange Token Index Token", "EXCHBEAR", 1570234197, NULL, "3x-short-exchange-token-index-token", "EXCHBEAR", "0x6baA91cd8AA07431760EF2eedFedCEF662A6B8B3");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x592ef68C18F05A22C5890263DEa5D952dd140d2A", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x592ef68C18F05A22C5890263DEa5D952dd140d2A", "C", "3X Long Exchange Token Index Token", "EXCHBULL", 1570234122, NULL, "3x-long-exchange-token-index-token", "EXCHBULL", "0x592ef68C18F05A22C5890263DEa5D952dd140d2A");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("EXCHHALF", "W", "0.5X Long Exchange Token Index Token", "EXCHHALF", 1596765600, NULL, "0-5x-long-echange-token-index-token", "EXCHHALF", "EXCHHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("EXCHHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xf8CC67e304f8e1A351ED83b4DBBe6B4076d51376", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xf8CC67e304f8e1A351ED83b4DBBe6B4076d51376", "C", "1X Short Exchange Token Index Token", "EXCHHEDGE", 1570234108, NULL, "1x-short-exchange-token-index-token", "EXCHHEDGE", "0xf8CC67e304f8e1A351ED83b4DBBe6B4076d51376");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("HALF", "W", "0.5X Long Bitcoin Token", "HALF", 1596765600, NULL, "0-5x-long-bitcoin-token", "HALF", "HALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("HALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("HALFSHIT", "W", "0.5X Long Shitcoin Index Token", "HALFSHIT", 1597975200, NULL, "0-5x-long-shitcoin-index-token", "HALFSHIT", "HALFSHIT"); INSERT INTO common_asset_details(asset_id, forked) VALUES("HALFSHIT", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x1FA3bc860bF823d792f04F662f3AA3a500a68814", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x1FA3bc860bF823d792f04F662f3AA3a500a68814", "C", "1X Short Bitcoin Token", "HEDGE", 1552911843, NULL, "1x-short-bitcoin-token", "", "0x1FA3bc860bF823d792f04F662f3AA3a500a68814");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x1d9cd2180Fd4E9771fCA28681034D02390B14e4c", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x1d9cd2180Fd4E9771fCA28681034D02390B14e4c", "C", "1X Short Shitcoin Index Token", "HEDGESHIT", 1566117877, NULL, "1x-short-shitcoin-index-token", "HEDGESHIT", "0x1d9cd2180Fd4E9771fCA28681034D02390B14e4c");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x86EB791495bE777db763142a2C547D1112554Fb8", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x86EB791495bE777db763142a2C547D1112554Fb8", "C", "3X Short Huobi Token Token", "HTBEAR", 1570234012, NULL, "3x-short-huobi-token-token", "HTBEAR", "0x86EB791495bE777db763142a2C547D1112554Fb8");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x0D5E2681D2AaDC91F7DA4146740180A2190f0c79", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x0D5E2681D2AaDC91F7DA4146740180A2190f0c79", "C", "3X Long Huobi Token Token", "HTBULL", 1570234070, NULL, "3x-long-huobi-token-token", "HTBULL", "0x0D5E2681D2AaDC91F7DA4146740180A2190f0c79");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("HTHALF", "W", "0.5X Long Huobi Token Token", "HTHALF", 1592791200, NULL, NULL, "HTHALF", "HTHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("HTHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x3008186FE6e3bCA6D1362105A48ec618672ce5b3", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x3008186FE6e3bCA6D1362105A48ec618672ce5b3", "C", "1X Short Huobi Token Token", "HTHEDGE", 1570233995, NULL, NULL, "HTHEDGE", "0x3008186FE6e3bCA6D1362105A48ec618672ce5b3");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x627e2Ee3dbDA546e168eaAFF25A2C5212E4A95a0", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x627e2Ee3dbDA546e168eaAFF25A2C5212E4A95a0", "C", "Inverse Bitcoin Volatility Token", "IBVOL", 1587558092, NULL, "1x-short-btc-implied-volatility", "IBVOL", "0x627e2Ee3dbDA546e168eaAFF25A2C5212E4A95a0");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("KNCBEAR", "W", "3X Short Kyber Network Token", "KNCBEAR", 1650062944, NULL, "3x-short-kyber-network-token", "KNCBEAR", "KNCBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("KNCBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("KNCBULL", "W", "3X Long Kyber Network Token", "KNCBULL", 1596722400, NULL, "3x-long-kyber-network-token", "KNCBULL", "KNCBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("KNCBULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("KNCHALF", "W", "0.5X Long Kyber Network Token", "KNCHALF", 1596722400, NULL, "0-5x-long-kyber-network-token", "KNCHALF", "KNCHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("KNCHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("KNCHEDGE", "W", "1X Short Kyber Network Token", "KNCHEDGE", 1592186400, NULL, NULL, "KNCHEDGE", "KNCHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("KNCHEDGE", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x3c955e35b6da1fF623D38D750c85b3Aed89A10c1", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x3c955e35b6da1fF623D38D750c85b3Aed89A10c1", "C", "3X Short LEO Token", "LEOBEAR", 1566119053, NULL, "3x-short-leo-token", "LEOBEAR", "0x3c955e35b6da1fF623D38D750c85b3Aed89A10c1");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xC2685307Ef2B8842fbf3DeF432408C46Bd0420fd", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xC2685307Ef2B8842fbf3DeF432408C46Bd0420fd", "C", "3X Long LEO Token", "LEOBULL", 1566118887, NULL, "3x-long-leo-token", "LEOBULL", "0xC2685307Ef2B8842fbf3DeF432408C46Bd0420fd");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("LEOHALF", "W", "0.5X Long LEO Token", "LEOHALF", 1590372000, NULL, NULL, "LEOHALF", "LEOHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("LEOHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("LINKHALF", "W", "0.5X Long Chainlink Token", "LINKHALF", 1598234400, NULL, "0-5x-long-chainlink-token", "LINKHALF", "LINKHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("LINKHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("LINKHEDGE", "W", "1X Short Chainlink Token", "LINKHEDGE", 1596852000, NULL, "1x-short-chainlink-token", "LINKHEDGE", "LINKHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("LINKHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("LTCHALF", "W", "0.5X Long Litecoin Token", "LTCHALF", 1589767200, NULL, NULL, "LTCHALF", "LTCHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("LTCHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xD0C64D6c0E9aA53fFFd8B80313e035f7B83083F3", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xD0C64D6c0E9aA53fFFd8B80313e035f7B83083F3", "C", "1X Short Litecoin Token", "LTCHEDGE", 1566116862, NULL, "1x-short-litecoin-token", "LTCHEDGE", "0xD0C64D6c0E9aA53fFFd8B80313e035f7B83083F3");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xbE893b4C214DBFfC17ef1E338fBDb7061FF09237", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xbE893b4C214DBFfC17ef1E338fBDb7061FF09237", "C", "3X Short Matic Token", "MATICBEAR", 1580720309, NULL, "3x-short-matic-token", "MATICBEAR", "0xbE893b4C214DBFfC17ef1E338fBDb7061FF09237");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x7e03521b9dA891Ca3F79A8728E2eaeb24886c5f9", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x7e03521b9dA891Ca3F79A8728E2eaeb24886c5f9", "C", "3X Long Matic Token", "MATICBULL", 1580720114, NULL, "3x-long-matic-token", "MATICBULL", "0x7e03521b9dA891Ca3F79A8728E2eaeb24886c5f9");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("MATICHALF", "W", "0.5X Long Matic Token", "MATICHALF", 1597716000, NULL, "0-5x-long-matic-token", "MATICHALF", "MATICHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("MATICHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("MATICHEDGE", "W", "1X Short Matic Token", "MATICHEDGE", 1597111200, NULL, "1x-short-matic-token", "MATICHEDGE", "MATICHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("MATICHEDGE", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xC82abB524257C8ee4790BFDefB452b2d6a395e21", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xC82abB524257C8ee4790BFDefB452b2d6a395e21", "C", "3X Short Midcap Index Token", "MIDBEAR", 1566118871, NULL, "3x-short-midcap-index-token", "MIDBEAR", "0xC82abB524257C8ee4790BFDefB452b2d6a395e21");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x59db60bD41bbC8cA4c1EfEE6Ea2A97EAe1E30cF5", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x59db60bD41bbC8cA4c1EfEE6Ea2A97EAe1E30cF5", "C", "3X Long Midcap Index Token", "MIDBULL", 1566117832, NULL, "3x-long-midcap-index-token", "MIDBULL", "0x59db60bD41bbC8cA4c1EfEE6Ea2A97EAe1E30cF5");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("MIDHALF", "W", "0.5X Long Midcap Index Token", "MIDHALF", 1597308232, NULL, "0-5x-long-midcap-index-token", "MIDHALF", "MIDHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("MIDHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("MIDHEDGE", "W", "1X Short Midcap Index Token", "MIDHEDGE", 1592791200, NULL, NULL, "MIDHEDGE", "MIDHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("MIDHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("MKRBEAR", "W", "3X Short Maker Token", "MKRBEAR", 1597024800, NULL, "3x-short-maker-token", "MKRBEAR", "MKRBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("MKRBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("MKRBULL", "W", "3X Long Maker Token", "MKRBULL", 1596765600, NULL, "3x-long-maker-token", "MKRBULL", "MKRBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("MKRBULL", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x053E5BA7Cb9669Dcc2fEb2D0E1d3d4a0AD6aaE39", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x053E5BA7Cb9669Dcc2fEb2D0E1d3d4a0AD6aaE39", "C", "3X Short OKB Token", "OKBBEAR", 1570234108, NULL, "3x-short-okb-token", "OKBBEAR", "0x053E5BA7Cb9669Dcc2fEb2D0E1d3d4a0AD6aaE39");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x8aF785687ee8D75114B028997c9ca36b5CC67Bc4", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x8aF785687ee8D75114B028997c9ca36b5CC67Bc4", "C", "3X Long OKB Token", "OKBBULL", 1570234051, NULL, "3x-long-okb-token", "OKBBULL", "0x8aF785687ee8D75114B028997c9ca36b5CC67Bc4");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("OKBHALF", "W", "0.5X Long OKB Token", "OKBHALF", 1596765600, NULL, "0-5x-long-okb-token", "OKBHALF", "OKBHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("OKBHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x889BC62E94bb6902D022bB82B38f7FCd637Df28C", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x889BC62E94bb6902D022bB82B38f7FCd637Df28C", "C", "1X Short OKB Token", "OKBHEDGE", 1570234092, NULL, "3x-short-okb-token", "OKBHEDGE", "0x889BC62E94bb6902D022bB82B38f7FCd637Df28C");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x3C4a46F0C075A7F191A7459bb51EB1f81ac36F8A", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x3C4a46F0C075A7F191A7459bb51EB1f81ac36F8A", "C", "3X Short PAX Gold Token", "PAXGBEAR", 1580719612, NULL, "3x-short-pax-gold-token", "PAXGBEAR", "0x3C4a46F0C075A7F191A7459bb51EB1f81ac36F8A");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x81f09eD4b98B1c8e99b1Fa838B72acB842AFE94c", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x81f09eD4b98B1c8e99b1Fa838B72acB842AFE94c", "C", "3X Long PAX Gold Token", "PAXGBULL", 1580719562, NULL, "3x-long-pax-gold-token", "PAXGBULL", "0x81f09eD4b98B1c8e99b1Fa838B72acB842AFE94c");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("PAXGHALF", "W", "0.5X Long PAX Gold Token", "PAXGHALF", 1599616800, NULL, "0-5x-long-pax-gold-token", "PAXGHALF", "PAXGHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("PAXGHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("PAXGHEDGE", "W", "1X Short PAX Gold Token", "PAXGHEDGE", 1589767200, NULL, NULL, "PAXGHEDGE", "PAXGHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("PAXGHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("PRIVBEAR", "W", "3X Short Privacy Index Token", "PRIVBEAR", 1596679200, NULL, "3x-short-privacy-index-token", "PRIVBEAR", "PRIVBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("PRIVBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("PRIVBULL", "W", "3X Short Privacy Index Token", "PRIVBULL", 1618536783, NULL, "3x-long-privacy-index-token", "PRIVBULL", "PRIVBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("PRIVBULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("PRIVHALF", "W", "0.5X Long Privacy Index Token", "PRIVHALF", 1603332000, NULL, "0-5x-long-privacy-index-token", "PRIVHALF", "PRIVHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("PRIVHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("PRIVHEDGE", "W", "1X Short Privacy Index Token", "PRIVHEDGE", 1603332000, NULL, "1x-short-privacy-index-token", "PRIVHEDGE", "PRIVHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("PRIVHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("SUSHIBEAR", "W", "3X Short Sushi Token", "SUSHIBEAR", 1600221600, NULL, "3x-short-sushi-token", "SUSHIBEAR", "SUSHIBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("SUSHIBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("SUSHIBULL", "W", "3X Long Sushi Token", "SUSHIBULL", 1600308000, NULL, "3x-long-sushi-token", "SUSHIBULL", "SUSHIBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("SUSHIBULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("SXPBEAR", "W", "3X Short Swipe Token", "SXPBEAR", 1596679200, NULL, "3x-short-swipe-token", "SXPBEAR", "SXPBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("SXPBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("SXPBULL", "W", "3X Long Swipe Token", "SXPBULL", 1596852000, NULL, "3x-long-swipe-token", "SXPBULL", "SXPBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("SXPBULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("SXPHALF", "W", "0.5X Long Swipe Token", "SXPHALF", 1596852000, NULL, "0-5x-long-swipe-token", "SXPHALF", "SXPHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("SXPHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("SXPHEDGE", "W", "1X Short Swipe Token", "SXPHEDGE", 1597111200, NULL, "1x-short-swipe-token", "SXPHEDGE", "SXPHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("SXPHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("THETABEAR", "W", "3X Short Theta Network Token", "THETABEAR", 1596679200, NULL, "3x-short-theta-network-token", "THETABEAR", "THETABEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("THETABEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("THETABULL", "W", "3X Long Theta Network Token", "THETABULL", 1596679200, NULL, "3x-long-theta-network-token", "THETABULL", "THETABULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("THETABULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("THETAHALF", "W", "0.5X Long Theta Network Token", "THETAHALF", 1596679200, NULL, "0-5x-long-theta-network-token", "THETAHALF", "THETAHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("THETAHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("THETAHEDGE", "W", "1X Short Theta Network Token", "THETAHEDGE", 1597024800, NULL, "1x-short-theta-network-token", "THETAHEDGE", "THETAHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("THETAHEDGE", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xA1653CB37852249e4f18dfBc473a5cE3F88Fa6aD", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xA1653CB37852249e4f18dfBc473a5cE3F88Fa6aD", "C", "3X Short TomoChain Token", "TOMOBEAR", 1580720348, NULL, "3x-short-tomochain-token", "TOMOBEAR", "0xA1653CB37852249e4f18dfBc473a5cE3F88Fa6aD");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xa38920C00D1a5303dB538A3Ea08da7a779e1F751", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xa38920C00D1a5303dB538A3Ea08da7a779e1F751", "C", "3X Long TomoChain Token", "TOMOBULL", 1580720053, NULL, "3x-long-tomochain-token", "TOMOBULL", "0xa38920C00D1a5303dB538A3Ea08da7a779e1F751");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("TOMOHALF", "W", "0.5X Long TomoChain Token", "TOMOHALF", 1597024800, NULL, NULL, "TOMOHALF", "TOMOHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("TOMOHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("TOMOHEDGE", "W", "1X Short TomoChain Token", "TOMOHEDGE", 1596765600, NULL, "1x-short-tomochain-token", "TOMOHEDGE", "TOMOHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("TOMOHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("TRXHALF", "W", "0.5X Long TRX Token", "TRXHALF", 1590372000, NULL, NULL, "TRXHALF", "TRXHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("TRXHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xe58C8dF0088Cf27b26C7D546A9835deAcC29496c", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xe58C8dF0088Cf27b26C7D546A9835deAcC29496c", "C", "1X Short TRX Token", "TRXHEDGE", 1558090503, NULL, "1x-short-trx-token", "TRXHEDGE", "0xe58C8dF0088Cf27b26C7D546A9835deAcC29496c");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xA5dDFCA8B837cCD0cf80fe6C24E2A9018FB50dbA", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xA5dDFCA8B837cCD0cf80fe6C24E2A9018FB50dbA", "C", "3X Short BiLira Token", "TRYBBEAR", 1580720179, NULL, "3x-short-bilira-token", "TRYBBEAR", "0xA5dDFCA8B837cCD0cf80fe6C24E2A9018FB50dbA");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xc7038cCf60E48C5b7119E55566A6aD9f2D66C7c2", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xc7038cCf60E48C5b7119E55566A6aD9f2D66C7c2", "C", "3X Long BiLira Token", "TRYBBULL", 1580720322, NULL, "3x-long-bilira-token", "TRYBBULL", "0xc7038cCf60E48C5b7119E55566A6aD9f2D66C7c2");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("TRYBHALF", "W", "0.5X Long BiLira Token", "TRYBHALF", 1592816322, NULL, NULL, "TRYBHALF", "TRYBHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("TRYBHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("TRYBHEDGE", "W", "1X Short BiLira Token", "TRYBHEDGE", 1592816322, NULL, NULL, "TRYBHEDGE", "TRYBHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("TRYBHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("UNISWAPBEAR", "W", "3X Short Uniswap Index Token", "UNISWAPBEAR", 1601888322, NULL, NULL, "UNISWAPBEAR", "UNISWAPBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("UNISWAPBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("UNISWAPBULL", "W", "3X Long Uniswap Index Token", "UNISWAPBULL", 1601888322, NULL, NULL, "UNISWAPBULL", "UNISWAPBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("UNISWAPBULL", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x0cd6c8161f1638485A1A2F5Bf1A0127E45913C2F", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x0cd6c8161f1638485A1A2F5Bf1A0127E45913C2F", "C", "3X Short Tether Token", "USDTBEAR", 1552910935, NULL, "3x-short-tether-token", "USDTBEAR", "0x0cd6c8161f1638485A1A2F5Bf1A0127E45913C2F");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x8Cce19943A01E78B7C277794fb081816F6151Bab", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x8Cce19943A01E78B7C277794fb081816F6151Bab", "C", "3X Long Tether Token", "USDTBULL", 1552911896, NULL, "3x-long-tether-token", "USDTBULL", "0x8Cce19943A01E78B7C277794fb081816F6151Bab");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("USDTHALF", "W", "0.5X Long Tether Token", "USDTHALF", 1591014296, NULL, NULL, "USDTHALF", "USDTHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("USDTHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("USDTHEDGE", "W", "1X Short Tether Token", "USDTHEDGE", 1606134296, NULL, NULL, "USDTHEDGE", "USDTHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("USDTHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("VETBEAR", "W", "3X Short VeChain Token", "VETBEAR", 1596679200, NULL, "3x-short-vechain-token", "VETBEAR", "VETBEAR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("VETBEAR", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("VETBULL", "W", "3X Long VeChain Token", "VETBULL", 1596679200, NULL, "3x-long-vechain-token", "VETBULL", "VETBULL"); INSERT INTO common_asset_details(asset_id, forked) VALUES("VETBULL", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("VETHEDGE", "W", "1X Short VeChain Token", "VETHEDGE", 1597148696, NULL, "1x-short-vechain-token", "VETHEDGE", "VETHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("VETHEDGE", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x31CbF205e26Ba63296FdBD254a6b1bE3ED28CE47", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x31CbF205e26Ba63296FdBD254a6b1bE3ED28CE47", "C", "3X Short Tether Gold Token", "XAUTBEAR", 1585498444, NULL, "3x-short-tether-gold-token", "XAUTBEAR", "0x31CbF205e26Ba63296FdBD254a6b1bE3ED28CE47");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xc9287623832668432099CEF2FfDEF3CeD14f4315", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xc9287623832668432099CEF2FfDEF3CeD14f4315", "C", "3X Long Tether Gold Token", "XAUTBULL", 1585498463, NULL, "3x-long-tether-gold-token", "XAUTBULL", "0xc9287623832668432099CEF2FfDEF3CeD14f4315");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("XAUTHALF", "W", "0.5X Long Tether Gold Token", "XAUTHALF", 1599660000, NULL, "0-5x-long-tether-gold-token", "XAUTHALF", "XAUTHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("XAUTHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("XAUTHEDGE", "W", "1X Short Tether Gold Token", "XAUTHEDGE", 1593439200, NULL, NULL, "XAUTHEDGE", "XAUTHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("XAUTHEDGE", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("XRPHALF", "W", "0.5X Long XRP Token", "XRPHALF", 1596679200, NULL, "0-5x-long-xrp-token", "XRPHALF", "XRPHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("XRPHALF", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x55b54D8fB1640d1321D5164590e7B020BA43def2", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x55b54D8fB1640d1321D5164590e7B020BA43def2", "C", "1X Short XRP Token", "XRPHEDGE", 1552911889, NULL, "1x-short-xrp-token", "XRPHEDGE", "0x55b54D8fB1640d1321D5164590e7B020BA43def2");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xbc41d05287498DEc58129560De6bd1b8d4E3aC1d", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xbc41d05287498DEc58129560De6bd1b8d4E3aC1d", "C", "3X Short Tezos Token", "XTZBEAR", 1580720246, NULL, "3x-short-tezos-token", "XTZBEAR", "0xbc41d05287498DEc58129560De6bd1b8d4E3aC1d");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x8AF17a6396c8f315f6b6DBC6AA686C85f9b3E554", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x8AF17a6396c8f315f6b6DBC6AA686C85f9b3E554", "C", "3X Long Tezos Token", "XTZBULL", 1580720015, NULL, "3x-long-tezos-token", "XTZBULL", "0x8AF17a6396c8f315f6b6DBC6AA686C85f9b3E554");
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("XTZHALF", "W", "0.5X Long Tezos Token", "XTZHALF", 1596679200, NULL, "0-5x-long-tezos-token", "XTZHALF", "XTZHALF"); INSERT INTO common_asset_details(asset_id, forked) VALUES("XTZHALF", NULL);
*
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("XTZHEDGE", "W", "1X Short Tezos Token", "XTZHEDGE", 1596679200, NULL, "1x-short-tezos-token", "XTZHEDGE", "XTZHEDGE"); INSERT INTO common_asset_details(asset_id, forked) VALUES("XTZHEDGE", NULL);
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x956F47F50A910163D8BF957Cf5846D573E7f87CA", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x956F47F50A910163D8BF957Cf5846D573E7f87CA", "C", "Fei USD", "FEI", 1616909037, NULL, "fei-protocol", "", "0x956F47F50A910163D8BF957Cf5846D573E7f87CA");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xc7283b66Eb1EB5FB86327f08e1B5816b0720212B", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xc7283b66Eb1EB5FB86327f08e1B5816b0720212B", "C", "Tribe", "TRIBE", 1616909037, NULL, "tribe-2", "", "0xc7283b66Eb1EB5FB86327f08e1B5816b0720212B");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xFd2a8fA60Abd58Efe3EeE34dd494cD491dC14900", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xFd2a8fA60Abd58Efe3EeE34dd494cD491dC14900", "C", "Curve.fi aDAI/aUSDC/aUSDT", "a3CRV", 1608558126, NULL, NULL, "", "0xFd2a8fA60Abd58Efe3EeE34dd494cD491dC14900");
*
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x51e00a95748DBd2a3F47bC5c3b3E7B3F0fea666c", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x51e00a95748DBd2a3F47bC5c3b3E7B3F0fea666c", "C", "DVGToken", "DVG", 1611997374, NULL, "daoventures", "DVG", "0x51e00a95748DBd2a3F47bC5c3b3E7B3F0fea666c");
*
UPDATE assets SET coingecko="3x-short-bitcoin-token" WHERE identifier="_ceth_0x016ee7373248a80BDe1fD6bAA001311d233b3CFa";/*Add a coingecko identifier to 3x short bitcoin token*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x016ee7373248a80BDe1fD6bAA001311d233b3CFa", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x016ee7373248a80BDe1fD6bAA001311d233b3CFa", "C", "3X Short Bitcoin Token", "BEAR", 1552867200, NULL, "3x-short-bitcoin-token", "BEAR", "0x016ee7373248a80BDe1fD6bAA001311d233b3CFa");
UPDATE assets SET coingecko="dao-casino" WHERE identifier="_ceth_0x8aA33A7899FCC8eA5fBe6A608A109c3893A1B8b2";/*Add a coingecko identifier to dao casino*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x8aA33A7899FCC8eA5fBe6A608A109c3893A1B8b2", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x8aA33A7899FCC8eA5fBe6A608A109c3893A1B8b2", "C", "DAO.Casino", "BET", 1490054400, NULL, "dao-casino", "BET", "0x8aA33A7899FCC8eA5fBe6A608A109c3893A1B8b2");
UPDATE assets SET coingecko="3x-long-bitcoin-token" WHERE identifier="_ceth_0x68eb95Dc9934E19B86687A10DF8e364423240E94";/*Add a coingecko identifier to 3x long bitcoin token*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x68eb95Dc9934E19B86687A10DF8e364423240E94", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x68eb95Dc9934E19B86687A10DF8e364423240E94", "C", "3X Long Bitcoin Token", "BULL", 1552867200, NULL, "3x-long-bitcoin-token", "BULL", "0x68eb95Dc9934E19B86687A10DF8e364423240E94");
UPDATE assets SET coingecko="pop-chest-token" WHERE identifier="_ceth_0x5D858bcd53E085920620549214a8b27CE2f04670";/*Add a coingecko identifier to pop chest token*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x5D858bcd53E085920620549214a8b27CE2f04670", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x5D858bcd53E085920620549214a8b27CE2f04670", "C", "Pop Chest Token", "POP", 1544486400, NULL, "pop-chest-token", "POPC", "0x5D858bcd53E085920620549214a8b27CE2f04670");
UPDATE assets SET coingecko=NULL WHERE identifier="_ceth_0x198A87b3114143913d4229Fb0f6D4BCb44aa8AFF";/*Remove coingecko identifier from Snowball. It's not just delisted -- but completely removed */
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x198A87b3114143913d4229Fb0f6D4BCb44aa8AFF", 8, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x198A87b3114143913d4229Fb0f6D4BCb44aa8AFF", "C", "Snowball", "SNBL", 1516941614, NULL, NULL, "", "0x198A87b3114143913d4229Fb0f6D4BCb44aa8AFF");
UPDATE assets SET coingecko="sp8de", cryptocompare="SPX" WHERE identifier="_ceth_0x05aAaA829Afa407D83315cDED1d45EB16025910c";/*Correct coingecko and cryptocompare identifier for sp8de*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x05aAaA829Afa407D83315cDED1d45EB16025910c", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x05aAaA829Afa407D83315cDED1d45EB16025910c", "C", "SP8DE Token", "SPX", 1515369600, NULL, "sp8de", "SPX", "0x05aAaA829Afa407D83315cDED1d45EB16025910c");
UPDATE assets SET coingecko="veritaseum" WHERE identifier="_ceth_0x8f3470A7388c05eE4e7AF3d01D8C722b0FF52374";/*Add a coingecko identifier for veritaseum*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x8f3470A7388c05eE4e7AF3d01D8C722b0FF52374", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x8f3470A7388c05eE4e7AF3d01D8C722b0FF52374", "C", "Veritaseum", "VERI", 1492951503, NULL, "veritaseum", "VERI", "0x8f3470A7388c05eE4e7AF3d01D8C722b0FF52374");
UPDATE assets SET coingecko="xsnx", cryptocompare="" WHERE identifier="_ceth_0x2367012aB9c3da91290F71590D5ce217721eEfE4";/*Update coingecko and cryptocompare identifier for xSNXa*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x2367012aB9c3da91290F71590D5ce217721eEfE4", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x2367012aB9c3da91290F71590D5ce217721eEfE4", "C", "xSNXa", "xSNXa", 1601566970, NULL, "xsnx", "", "0x2367012aB9c3da91290F71590D5ce217721eEfE4");
UPDATE assets SET coingecko="aave-eth-v1" WHERE identifier="_ceth_0x3a3A65aAb0dd2A17E3F1947bA16138cd37d08c04";/*Update coingecko identifier for aETH v1*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x3a3A65aAb0dd2A17E3F1947bA16138cd37d08c04", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x3a3A65aAb0dd2A17E3F1947bA16138cd37d08c04", "C", "Aave Interest bearing ETH"", "aETH", 1578501678, NULL, "aave-eth-v1", "ETH", "0x3a3A65aAb0dd2A17E3F1947bA16138cd37d08c04");
UPDATE assets SET coingecko="camp" WHERE identifier="_ceth_0xE9E73E1aE76D17A16cC53E3e87a9a7dA78834d37";/*Set a coingecko identifier for CAMP*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0xE9E73E1aE76D17A16cC53E3e87a9a7dA78834d37", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0xE9E73E1aE76D17A16cC53E3e87a9a7dA78834d37", "C", "Camp"", "CAMP", 1601535391, NULL, "camp", "CAMP", "0xE9E73E1aE76D17A16cC53E3e87a9a7dA78834d37");
UPDATE assets SET coingecko="celo-dollar" WHERE identifier="CUSD";/*Set a coingecko identifier for Celo Dollar*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("CUSD", "B", "Celo USD", "CUSD", 1601337600, NULL, "celo-dollar", "CELOUSD", "CUSD"); INSERT INTO common_asset_details(asset_id, forked) VALUES("CUSD", NULL);
UPDATE assets SET cryptocompare="" WHERE identifier="EDR-2";/*Remove cryptocompare identifier for E-Dinar coin. We have no data anymore for this*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("EDR-2", "B", "E-Dinar Coin", "EDR", 1472226274, NULL, NULL, "", "EDR-2"); INSERT INTO common_asset_details(asset_id, forked) VALUES("EDR-2", NULL);
UPDATE assets SET coingecko="faircoin" WHERE identifier="FAIR";/*Add a coingecko identifier for FairCoin*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("FAIR", "B", "FairCoin", "FAIR", 1393286400, NULL, "faircoin", "FAIR", "FAIR"); INSERT INTO common_asset_details(asset_id, forked) VALUES("FAIR", NULL);
UPDATE assets SET cryptocompare="SPAIN" WHERE identifier="SPA";/*Update cryptocompare identifier for SpainCoin.*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("SPA", "B", "SpainCoin", "SPA", 1394668800, NULL, NULL, "SPAIN", "SPA"); INSERT INTO common_asset_details(asset_id, forked) VALUES("SPA", NULL);
UPDATE assets SET coingecko="tokes", cryptocompare="TKS" WHERE identifier="TKS";/*Add a coingecko and cryptocompare identifier for Tokes*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("TKS", "M", "Tokes", "TKS", 1480723200, NULL, "tokes", "TKS", "TKS"); INSERT INTO common_asset_details(asset_id, forked) VALUES("TKS", NULL);
UPDATE assets SET coingecko="terrausd", cryptocompare="UST" WHERE identifier="UST";/*Add a coingecko and cryptocompare identifier for TerraUSD*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("UST", "B", "TerraUSD", "UST", 1599350400, NULL, "terrausd", "UST", "UST"); INSERT INTO common_asset_details(asset_id, forked) VALUES("UST", NULL);
UPDATE assets SET coingecko="milk-alliance", cryptocompare="MLK" WHERE identifier="MLK";/*Fix a coingecko and cryptocompare identifier for MiL.k*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("MLK", "V", "MiL.k", "MLK", 1595462400, NULL, "milk-alliance", "MLK", "MLK"); INSERT INTO common_asset_details(asset_id, forked) VALUES("MLK", NULL);
UPDATE assets SET cryptocompare="ALPA" WHERE identifier="_ceth_0x7cA4408137eb639570F8E647d9bD7B7E8717514A";/*Set a coingecko identifier for ALPA*/
INSERT INTO ethereum_tokens(address, decimals, protocol) VALUES("0x7cA4408137eb639570F8E647d9bD7B7E8717514A", 18, NULL); INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("_ceth_0x7cA4408137eb639570F8E647d9bD7B7E8717514A", "C", "AlpaToken"", "ALPA", 1603590090, NULL, "alpaca", "ALPA", "0x7cA4408137eb639570F8E647d9bD7B7E8717514A");
UPDATE assets SET cryptocompare="MOB" WHERE identifier="MOB";/*Add a cryptocompare identifier for mobilecoin*/
INSERT INTO assets(identifier, type, name, symbol, started, swapped_for, coingecko, cryptocompare, details_reference) VALUES("MOB", "B", "MobileCoin", "MOB", 1607212800, NULL, "mobilecoin", "MOB", "MOB"); INSERT INTO common_asset_details(asset_id, forked) VALUES("MOB", NULL);

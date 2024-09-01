import json

ERC20Json = open("src/dfk_commons/abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

ERC721Json = open("src/dfk_commons/abi/ERC721.json")
ERC721ABI = json.load(ERC721Json)

HeroCoreJson = open("src/dfk_commons/abi/HeroCoreDiamond.json")
HeroCoreABI = json.load(HeroCoreJson)

HeroSaleJson = open("src/dfk_commons/abi/HeroSale.json")
HeroSaleABI = json.load(HeroSaleJson)

HeroBridgeJson = open("src/dfk_commons/abi/HeroBridgeUpgradeable.json")
HeroBridgeABI = json.load(HeroBridgeJson)
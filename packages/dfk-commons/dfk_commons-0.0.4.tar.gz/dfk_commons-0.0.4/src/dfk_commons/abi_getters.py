import json

ERC20Json = open("abi/ERC20.json")
ERC20ABI = json.load(ERC20Json)

ERC721Json = open("abi/ERC721.json")
ERC721ABI = json.load(ERC721Json)

HeroCoreJson = open("abi/HeroCoreDiamond.json")
HeroCoreABI = json.load(HeroCoreJson)

HeroSaleJson = open("abi/HeroSale.json")
HeroSaleABI = json.load(HeroSaleJson)

HeroBridgeJson = open("abi/HeroBridgeUpgradeable.json")
HeroBridgeABI = json.load(HeroBridgeJson)
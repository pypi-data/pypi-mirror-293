from dfk_commons.classes.APIService import APIService
from dfk_commons.classes.Account import Account
from dfk_commons.classes.RPCProvider import RPCProvider
from dfk_commons.abi_getters import ERC20ABI, ERC721ABI

def getCrystalBalance(account: Account, apiService: APIService, RPCProvider: RPCProvider):
    contract = RPCProvider.w3.eth.contract(address= apiService.tokens["Crystal"].address, abi=ERC20ABI)
    return int(contract.functions.balanceOf(account.address).call())

def heroNumber(account: Account, apiService: APIService, rpcProvider: RPCProvider):
    contract = rpcProvider.w3.eth.contract(address= apiService.contracts["Heroes"]["address"], abi=ERC721ABI)
    return int(contract.functions.balanceOf(account.address).call())
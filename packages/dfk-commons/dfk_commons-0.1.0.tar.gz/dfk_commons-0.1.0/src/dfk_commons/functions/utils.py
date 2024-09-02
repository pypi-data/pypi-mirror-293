from dfk_commons.classes.APIService import APIService
from dfk_commons.classes.Account import Account
from dfk_commons.classes.RPCProvider import RPCProvider
from dfk_commons.abi_getters import ERC20ABI, ERC721ABI

def getJewelBalance(account: Account, rpcProvider: RPCProvider):
    return int(rpcProvider.w3.eth.get_balance(account.address))

def getCrystalBalance(account: Account, apiService: APIService, rpcProvider: RPCProvider):
    contract = rpcProvider.w3.eth.contract(address= apiService.tokens["Crystal"].address, abi=ERC20ABI)
    return int(contract.functions.balanceOf(account.address).call())

def heroNumber(account: Account, apiService: APIService, rpcProvider: RPCProvider):
    contract = rpcProvider.w3.eth.contract(address= apiService.contracts["Heroes"]["address"], abi=ERC721ABI)
    return int(contract.functions.balanceOf(account.address).call())

def sendJewel(account: Account, payout_address, amount, rpcProvider: RPCProvider):
    tx = {
        "from": account.address,
        "to": payout_address,
        "value": amount,
        "nonce": account.nonce,
        "chainId": rpcProvider.chainId
    }
    tx["gas"] = int(rpcProvider.w3.eth.estimate_gas(tx))
    tx["maxFeePerGas"] = rpcProvider.w3.to_wei(12, 'gwei')
    tx["maxPriorityFeePerGas"] = rpcProvider.w3.to_wei(1, "gwei")
    signed_tx = rpcProvider.w3.eth.account.sign_transaction(tx, account.key)
    hash = rpcProvider.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    hash = rpcProvider.w3.to_hex(hash)
    rpcProvider.w3.eth.wait_for_transaction_receipt(hash)
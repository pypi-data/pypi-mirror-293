from dfk_commons.classes.RPCProvider import RPCProvider

class Account:
    def __init__(self, account, rpcProvider: RPCProvider, account_data) -> None:
        self.account = account
        self.address = account.address
        self.key = account.key
        self.manager = account_data["pay_to"]
        self.profession = account_data["profession"] if "profession" in account_data else "mining"
        self.enabled_quester = account_data["enabled_quester"]
        self.enabled_manager = account_data["enabled_manager"]
        self.questing = account_data["questing"]
        self.rpcProvider = rpcProvider
    
    @property
    def nonce(self):
        return self.rpcProvider.w3.eth.get_transaction_count(self.address, "pending")
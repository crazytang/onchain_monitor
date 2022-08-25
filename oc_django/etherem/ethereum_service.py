from pprint import pprint

from web3 import Web3
from web3.providers import JSONBaseProvider

from oc_django.etherem.objects.block import Block
from oc_django.etherem.objects.contract_receipt import ContractReceipt
from oc_django.etherem.objects.contract_transaction import ContractTransaction
from oc_django.helpers.utils import bn_to_number

RPC_GATEWAY = 'https://kovan.infura.io/v3/b0ad1354b637443a871c602ec795fc71'
class EthereumService:
    def __init__(self):
        self.provider = Web3.HTTPProvider(RPC_GATEWAY)
        self.web3: Web3 = Web3(self.provider)
        self.eth = self.web3.eth

    def get_block_from_number(self, block_number: int) -> Block:
        data = self.eth.getBlock(block_number)
        return Block(data)

    def get_balance(self, user_address: str) -> float:
        return bn_to_number( self.eth.getBalance(user_address))

    def get_contract_receipt(self, tx_hash:str):
        return ContractReceipt(self.eth.get_transaction_receipt(tx_hash))

    def get_contract_transaction(self, tx_hash: str):
        return ContractTransaction(self.eth.get_transaction(tx_hash))

    def get_block_number(self)->int:
        return self.eth.get_block_number()
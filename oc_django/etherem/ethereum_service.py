import json

from django.conf import settings
from hexbytes import HexBytes
from web3 import Web3

from oc_django.etherem.objects.block import Block
from oc_django.etherem.objects.contract_receipt import ContractReceipt
from oc_django.etherem.objects.contract_transaction import ContractTransaction
from oc_django.helpers.utils import bn_to_number, to_hex


class EthereumService:
    def __init__(self, network_name='kovan'):
        self.gateway = settings.CHAIN_SETTING[network_name]['rpc']
        self.provider = Web3.HTTPProvider(self.gateway)
        self.web3: Web3 = Web3(self.provider)
        self.eth = self.web3.eth

    def get_block_from_number(self, block_number: int) -> Block:
        data = self.eth.getBlock(block_number)
        return Block(data)

    def get_balance(self, user_address: str) -> float:
        return bn_to_number(self.eth.getBalance(user_address))

    def get_contract_receipt(self, tx_hash: str) -> ContractReceipt:
        return ContractReceipt(self.eth.get_transaction_receipt(to_hex(tx_hash)))

    def get_raw_contract_receipt(self, tx_hash: str) -> (ContractReceipt, str):
        """
        the db need the raw transaction data
        """
        raw = self.eth.get_transaction_receipt(to_hex(tx_hash))
        return ContractReceipt(raw), self.raw_receipt_to_json(raw)

    def raw_receipt_to_json(self, raw_receipt) -> str:
        """
        handle some innormal attributes, like HexBytes
        """
        keys = raw_receipt.__dict__.keys()
        new_obj = {}
        for key in keys:
            if isinstance(raw_receipt[key], HexBytes):
                new_obj[key] = raw_receipt[key].hex()
            elif isinstance(raw_receipt[key], list) and len(raw_receipt[key]) > 0:
                new_obj[key] = []
                for i in range(0, len(raw_receipt[key])):
                    new_obj[key].append({})
                    keys2 = raw_receipt[key][i].__dict__.keys()
                    for key2 in keys2:
                        if isinstance(raw_receipt[key][i][key2], HexBytes):
                            new_obj[key][i][key2] = raw_receipt[key][i][key2].hex()
                        elif isinstance(raw_receipt[key][i][key2], list) and len(raw_receipt[key][i][key2]) > 0:
                            new_obj[key][i][key2] = []
                            for ii in range(0, len(raw_receipt[key][i][key2])):
                                if isinstance(raw_receipt[key][i][key2][ii], HexBytes):
                                    new_obj[key][i][key2].append(raw_receipt[key][i][key2][ii].hex())
                                else:
                                    new_obj[key][i][key2].append(raw_receipt[key][i][key2][ii])

                        else:
                            new_obj[key][i][key2] = raw_receipt[key][i][key2]
            else:
                new_obj[key] = raw_receipt[key]

        return json.dumps(new_obj)

    def get_contract_transaction(self, tx_hash: str):
        return ContractTransaction(self.eth.get_transaction(tx_hash))

    def get_block_number(self) -> int:
        return self.eth.get_block_number()

    def wait_transaction_receipt(self, tx_hash: str) -> ContractReceipt:
        """
        waiting for transaction fulfilled
        """
        raw = self.eth.wait_for_transaction_receipt(to_hex(tx_hash))
        return ContractReceipt(raw)

    def wait_raw_transaction_receipt(self, tx_hash: str) -> (ContractReceipt, str):
        """
        waiting for transaction fulfilled, and return raw data
        """
        raw = self.eth.wait_for_transaction_receipt(tx_hash)
        return ContractReceipt(raw), self.raw_receipt_to_json(raw)


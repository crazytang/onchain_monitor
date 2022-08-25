from pprint import pprint
from unittest import TestCase

from oc_django.etherem.ethereum_service import EthereumService
from oc_django.etherem.objects.block import Block


class TestEtheremService(TestCase):

    def setUp(self) -> None:
        self.eth = EthereumService()
        pass

    def test_user_balance(self):
        user_address = '0x90b30e8d7Eaf82039AD0cABC548B107663514871'
        balance = self.eth.get_balance(user_address)
        # print('user address %s balance is %f' % (user_address,balance))
        self.assertGreater(balance, 0)

    def test_get_block(self):
        block_number = 33441757
        block: Block = self.eth.get_block_from_number(block_number)

        # pprint(block)
        self.assertGreater(len(block.transactions), 0)
        self.assertEqual(block_number, block.number)

    def test_getContract_receipt(self):
        tx_hash = '0x23997910e25b3ac5ef4a115a092351549753705c9bf92853004bb6be20c5d80c'
        receipt = self.eth.get_contract_receipt(tx_hash)
        tx = self.eth.get_contract_transaction(tx_hash)

        # pprint(tx.transactionHash)
        self.assertEqual(tx.hash, receipt.transactionHash)


from django.utils.datetime_safe import datetime

from oc_django.etherem.ethereum_service import EthereumService
from oc_django.etherem.objects.block import Block
from oc_django.etherem.objects.contract_receipt import ContractReceipt
from oc_django.etherem.objects.contract_transaction import ContractTransaction
from oc_django.helpers.utils import bn_to_number, get_datetime_now
from onchain_monitor.models.contract_transaction_info import ContractTransactionInfo


class ContractTransactionService:
    @staticmethod
    def get_one_from_tx_hash(tx_hash: str) -> ContractTransactionInfo:
        return ContractTransactionInfo.objects.filter(tx_hash=tx_hash).first()

    @staticmethod
    def handleTx(block: Block, tx: ContractTransaction, receipt: ContractReceipt, raw_receipt:str,network='kovan') -> ContractTransactionInfo:
        """
        handle the transaction data, then save to db
        """
        # receipt.transactionHash = '0x3ec1053abafe387a7c062b773f4e80512adf22be311b769e45912f21c5521d'
        tx_info: ContractTransactionInfo = ContractTransactionService.get_one_from_tx_hash(receipt.transactionHash)

        if not tx_info:
            tx_info = ContractTransactionInfo()
            tx_info.tx_hash = receipt.transactionHash
            tx_info.tx_status = receipt.status
            tx_info.tx_from = receipt._from
            tx_info.tx_to = receipt.to
            tx_info.block_hash = receipt.blockHash
            tx_info.block_number = receipt.blockNumber
            tx_info.network = network
            tx_info.tx_nonce = tx.nonce
            tx_info.tx_data = tx.input
            tx_info.tx_value = tx.value
            tx_info.tx_receipt = raw_receipt
            tx_info.tx_gas_used = bn_to_number(receipt.gasUsed)
            tx_info.transacted_at = datetime.fromtimestamp(block.timestamp)
            tx_info.created_at = get_datetime_now()

        tx_info.save()

        # print('tx_info', tx_info)
        return tx_info

    @staticmethod
    def handle_tx_from_wss(block_number: int, contract_addresses: [str], network:str):
        """
        handle the transaction data from websocket subscribed
        """
        ethereum_service = EthereumService(network)
        block = ethereum_service.get_block_from_number(block_number)
        txs = block.transactions
        for tx_hash in txs:
            receipt, raw_receipt = ethereum_service.get_raw_contract_receipt(tx_hash)
            if receipt.transactionHash.lower() in contract_addresses:
                tx = ethereum_service.get_contract_transaction(tx_hash)
                ContractTransactionService.handleTx(block, tx, receipt, raw_receipt, network)

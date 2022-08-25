from django.utils.datetime_safe import datetime

from oc_django.etherem.objects.block import Block
from oc_django.etherem.objects.contract_receipt import ContractReceipt
from oc_django.etherem.objects.contract_transaction import ContractTransaction
from onchain_monitor.models.contract_transaction_info import ContractTransactionInfo


class ContractTransactionService:
    @staticmethod
    def get_one_from_tx_hash(tx_hash: str) -> ContractTransactionInfo:
        return ContractTransactionInfo.objects.filter(tx_hash=tx_hash).first()

    @staticmethod
    def handleTx(block: Block, tx: ContractTransaction, receipt: ContractReceipt):
        """
        处理交易数据，保存到数据库里面
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
            tx_info.network = 'kovan' # todo requiring from variant
            tx_info.tx_nonce = tx.nonce
            tx_info.tx_data = tx.input
            tx_info.tx_value = tx.value
            tx_info.tx_receipt = str(receipt)
            tx_info.tx_gas_used = receipt.gasUsed
            tx_info.transacted_at = datetime.fromtimestamp(block.timestamp)
            tx_info.created_at = datetime.now()

        tx_info.save()

        print('tx_info', tx_info)



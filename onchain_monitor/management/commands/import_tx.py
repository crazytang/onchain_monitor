from pprint import pprint
from django.core.management import BaseCommand

from oc_django.etherem.ethereum_service import EthereumService
from oc_django.etherem.objects.block import Block
from oc_django.etherem.objects.contract_receipt import ContractReceipt
from onchain_monitor.models.common_contract import CommonContract
from onchain_monitor.services.common_contract_service import CommonContractService
from onchain_monitor.services.contract_transaction_service import ContractTransactionService


class Command(BaseCommand):
    help = 'Import On Chain Transactions'

    addresses: [str] = []
    def add_arguments(self, parser):
        parser.add_argument('block_num', type=int, help='from block number')
        # pass

    def handle(self, *args, **options):
        start_block_num = int(options['block_num']) # 开始block number

        self.ethereum_service = EthereumService()
        latest_block_num = self.ethereum_service.get_block_number() # 结束block number

        for i in range(start_block_num, latest_block_num):
            block = self.ethereum_service.get_block_from_number(i)
            self.detect(block)
            return

    def get_contract_addresses(self)->[str]:
        """
        获取监控地址
        :return:
        """
        # if not hasattr(self, 'addresses'):
        #     self.addresses = []
        if len(self.addresses) > 0:
            return self.addresses

        rs = CommonContractService.get_all()

        for i in range(0, len(rs)):
            self.addresses.append(rs[i].contract_address)

        return self.addresses

    def detect(self, block: Block):
        """
        检测区块
        """

        addresses = self.get_contract_addresses()

        txs = block.transactions
        for i in range(0, len(txs)):
            print('block number %d' %i)
            receipt= self.ethereum_service.get_contract_receipt(txs[i])
            for ii in range(0, len(addresses)):
                if receipt.to.lower() == addresses[ii].lower():
                    print('hitted a tx %s' % receipt.transactionHash)
                    tx = self.ethereum_service.get_contract_transaction(receipt.transactionHash)
                    ContractTransactionService.handleTx(block, tx, receipt)
                    break
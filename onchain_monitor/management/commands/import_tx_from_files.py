import os
from django.core.management import BaseCommand
import csv
from oc_django.etherem.ethereum_service import EthereumService
from oc_django.etherem.objects.block import Block
from oc_django.etherem.objects.contract_receipt import ContractReceipt
from oc_django.etherem.objects.contract_transaction import ContractTransaction
from oc_django.helpers.utils import check_network_name
from onchain_monitor.models.common_contract import CommonContract
from onchain_monitor.services.common_contract_service import CommonContractService
from onchain_monitor.services.contract_transaction_service import ContractTransactionService


class Command(BaseCommand):
    help = 'Import On Chain Transactions'

    addresses: [str] = []

    def __init__(self, stdout=None, stderr=None, no_color=False, force_color=False):
        super().__init__(stdout, stderr, no_color, force_color)
        self.ethereum_service = None

    def add_arguments(self, parser):
        parser.add_argument('network', type=str, default='kovan', help='network name')
        parser.add_argument('path', type=str, help='import path')
        # pass

    def handle(self, *args, **options):
        path = options['path']
        network = options['network']
        rs, tips = check_network_name(network)
        if not rs:
            raise Exception(tips)

        if not os.path.exists(path):
            raise Exception(path, 'is not exists')

        files = os.listdir(path)

        new_files = []
        for i in range(0, len(files)):
            _file = path + '/' + files[i]
            _tmp = _file.split('.')

            if os.path.isfile(_file) and _tmp[len(_tmp)-1].lower() == 'csv':
                new_files[i] = path + '/' + files[i]

        if len(new_files) == 0:
            raise Exception(path, 'is empty or no csv file')

        contract_addresses = self.get_contract_addresses()

        txs = []
        for i in range(0, len(new_files)):
            print('reading file', new_files[i])
            with open(files[i], newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    if row[0] == 'Txhash':
                        continue

                    if row[5].lower() in contract_addresses:
                        txs.append(row[0])

        if len(txs) == 0:
            raise Exception('no any relevant tx can be found')

        print(len(txs),'txs found')

        self.ethereum_service = EthereumService(network)

        for tx_hash in txs:
            print('handling', tx_hash)
            receipt, raw_receipt = self.ethereum_service.get_raw_contract_receipt(tx_hash)
            block: Block = self.ethereum_service.get_block_from_number(receipt.blockNumber)
            tx: ContractTransaction = self.ethereum_service.get_contract_transaction(tx_hash)

            ContractTransactionService.handleTx(block, tx, receipt, raw_receipt)
            print('handled')

        for i in range(0, len(new_files)):
            self.file_done(new_files[i])

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
            self.addresses.append(rs[i].contract_address.lower())

        return self.addresses

    def file_done(self, file:str):
        new_file = file + '.done'
        os.rename(file, new_file)
        print(file,'has been renamed to ',new_file)
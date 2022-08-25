from web3.datastructures import AttributeDict

from oc_django.etherem.objects.transaction_log import TransactionLog
from oc_django.libs.dj_base_object import DjBaseObject


class ContractReceipt(DjBaseObject):
    def __init__(self, data:AttributeDict):
        self.blockHash = data['blockHash'].hex()
        self.blockNumber = data['blockNumber']
        self.contractAddress = data['contractAddress']
        self.cumulativeGasUsed = data['cumulativeGasUsed']
        self.effectiveGasPrice = data['effectiveGasPrice']
        self._from = data['from']
        self.to = data['to']
        self.gasUsed = data['gasUsed']

        self.logs = []
        for i in range(0, len(data['logs'])):
            self.logs.append(TransactionLog(data['logs'][i]))

        self.logsBloom = data['logsBloom'].hex()
        self.status = data['status']
        self.transactionHash = data['transactionHash'].hex()
        self.transactionIndex = data['transactionIndex']
        if 'type' not in data:
            self.type = 0
        else:
            self.type = int(data['type'], 16)
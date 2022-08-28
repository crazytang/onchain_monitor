from web3.datastructures import AttributeDict

from oc_django.helpers.utils import batch_hex_bytes_to_string
from oc_django.libs.dj_base_object import DjBaseObject


class TransactionLog(DjBaseObject):
    def __init__(self, data: AttributeDict):
        # print('data', data)
        self.address = data['address']
        self.blockHash = data['blockHash'].hex()
        self.blockNumber = data['blockNumber']
        self.data = data['data']
        self.logIndex = data['logIndex']
        self.removed = data['removed']
        self.topics = batch_hex_bytes_to_string(data['topics'])
        self.transactionHash = data['transactionHash'].hex()
        self.transactionIndex = data['transactionIndex']
        self.transactionLogIndex = 0 if 'transactionLogIndex' not in data else int(data['transactionLogIndex'], 16)
        self.type = 0 if 'type' not in data else data['type']
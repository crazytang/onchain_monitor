from web3.datastructures import AttributeDict

from oc_django.etherem.objects.transaction_log import TransactionLog
from oc_django.helpers.utils import batch_hex_bytes_to_string, hex_to_dec, bn_to_number
from oc_django.libs.dj_base_object import DjBaseObject


class ContractTransaction(DjBaseObject):
    def __init__(self, data:AttributeDict):
        self.accessList = batch_hex_bytes_to_string(data['accessList'])
        self.blockHash = data['blockHash'].hex()
        self.blockNumber = data['blockNumber']
        self.chainId = hex_to_dec(data['chainId'])
        self.condition = data['condition']
        self.creates = data['creates']
        self._from = data['from']
        self.gas = data['gas']
        self.gasPrice = data['gasPrice']
        self.hash = data['hash'].hex()
        self.input = data['input']
        self.maxFeePerGas = hex_to_dec(data['maxFeePerGas'])
        self.maxPriorityFeePerGas = hex_to_dec(data['maxPriorityFeePerGas'])
        self.nonce = data['nonce']
        self.publicKey = data['publicKey'].hex()
        self.r = data['r'].hex()
        self.raw = data['raw'].hex()
        self.s = data['s'].hex()
        self.to = data['to']
        self.transactionIndex = data['transactionIndex']
        if 'type' in data:
            self.type = hex_to_dec(data['type'])
        else:
            self.type = 0

        self.v = data['v']
        self.value = bn_to_number(data['value'])
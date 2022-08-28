from hexbytes import HexBytes
from web3.datastructures import AttributeDict

from oc_django.helpers.utils import batch_hex_bytes_to_string
from oc_django.libs.dj_base_object import DjBaseObject


class Block(DjBaseObject):
    def __init__(self, data:AttributeDict):
        # print('data', data)
        self.author = '' if 'author' not in data else data['author']
        self.baseFeePerGas = '' if 'baseFeePerGas' not in data else data['baseFeePerGas']
        self.receiptsRoot = '' if 'receiptsRoot' not in data else data['receiptsRoot']
        self.difficulty = data['difficulty']
        self.extraData = HexBytes(data['extraData']).hex()
        self.gasLimit = data['gasLimit']
        self.gasUsed = data['gasUsed']
        self.hash = HexBytes(data['hash']).hex()
        self.logsBloom = HexBytes(data['logsBloom']).hex()
        self.miner = data['miner']
        self.number = data['number']
        self.parentHash = HexBytes(data['parentHash']).hex()
        self.sealFields = '' if 'sealFields' not in data else data['sealFields']
        self.sha3Uncles = HexBytes(data['sha3Uncles']).hex()
        self.signature = '' if 'signature' not in data else data['signature']
        self.size = data['size']
        self.stateRoot = HexBytes(data['stateRoot']).hex()
        self.step = 0 if 'step' not in data else data['step']
        self.timestamp = data['timestamp']
        self.totalDifficulty = data['totalDifficulty']

        self.transactions = batch_hex_bytes_to_string(data['transactions'])
        # for i in range(0, len(data['transactions'])):
        #     self.transactions.append(HexBytes(data['transactions'][i]).hex())

        self.transactionsRoot = HexBytes(data['transactionsRoot']).hex()
        self.uncles = data['uncles']

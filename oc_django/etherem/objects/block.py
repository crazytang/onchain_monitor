from hexbytes import HexBytes
from web3.datastructures import AttributeDict

from oc_django.helpers.utils import batch_hex_bytes_to_string
from oc_django.libs.dj_base_object import DjBaseObject


class Block(DjBaseObject):
    def __init__(self, data:AttributeDict):
        self.author = data['author']
        self.baseFeePerGas = data['baseFeePerGas']
        self.difficulty = data['difficulty']
        self.extraData = HexBytes(data['extraData']).hex()
        self.gasLimit = data['gasLimit']
        self.gasUsed = data['gasUsed']
        self.hash = HexBytes(data['hash']).hex()
        self.logsBloom = HexBytes(data['logsBloom']).hex()
        self.miner = data['miner']
        self.number = data['number']
        self.parentHash = HexBytes(data['parentHash']).hex()
        self.sealFields = data['sealFields']
        self.sha3Uncles = HexBytes(data['sha3Uncles']).hex()
        self.signature = data['signature']
        self.size = data['size']
        self.stateRoot = HexBytes(data['stateRoot']).hex()
        self.step = data['step']
        self.timestamp = data['timestamp']
        self.totalDifficulty = data['totalDifficulty']

        self.transactions = batch_hex_bytes_to_string(data['transactions'])
        # for i in range(0, len(data['transactions'])):
        #     self.transactions.append(HexBytes(data['transactions'][i]).hex())

        self.transactionsRoot = HexBytes(data['transactionsRoot']).hex()
        self.uncles = data['uncles']

import json

import websockets
from django.conf import settings
from websockets import connect

from oc_django.etherem.ethereum_service import EthereumService
from oc_django.helpers.utils import check_network_name
from oc_django.libs.log_service import LogService
from onchain_monitor.services.contract_transaction_service import ContractTransactionService


class SocketClientService:
    """
    The socket client service
    Call Sample Codes:
        wss_uri = 'wss://kovan.infura.io/ws/v3/ebd7174b1e35424f9b5842a4f2f7cc4a'
        scb_str = '{"jsonrpc":"2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}'
        ws = SocketClientService(wss_uri).subscribe(scb_str)
        asyncio.run(ws.run())
    """
    def __init__(self, network='kovan'):
        self.__uri = settings.CHAIN_SETTING[network]['wss']
        self.__subscribe_str = ''
        self.__network = network
        self.__contract_addresses: [str] = []
        self.ethereum_service = EthereumService(network)

    def set_uri(self, uri):
        """
        set the websocket uri
        """
        self.__uri = uri
        return self

    def set_restric_addresses(self, contract_addresses: [str]):
        """
        set the addresses of restriction
        """
        self.__contract_addresses = contract_addresses
        return self

    def subscribe(self, scb_str):
        """
        set the subscribe json data
        """
        self.__subscribe_str = scb_str
        return self

    async def run(self):
        """
        run the websocket client
        """
        if len(self.__contract_addresses) == 0:
            raise Exception('contract_addresses can not be empty')
        rs, tip = check_network_name(self.__network)
        if not rs:
            raise Exception(tip)

        async with connect(self.__uri) as websocket:
            self.__log('connected to: %s' % self.__uri)
            try:
                await websocket.send(self.__subscribe_str)
                self.__log('sent: %s' % self.__subscribe_str)
                async for message in websocket:
                    # self.__log('received: %s' %message)
                    data = json.loads(message)
                    if 'params' in data and 'result' in data['params'] and 'number' in data['params']['result']:
                        block_number = int(data['params']['result']['number'], 16)
                        ContractTransactionService.handle_tx_from_wss(block_number, self.__contract_addresses, self.__network)
            except websockets.ConnectionClosed:
                self.__log('connection is lost, trying reconnection')
                await self.run()

    def __log(self, msg):
        log_file = 'wss.log'
        log_dir = ''
        LogService.write_to_log(log_dir, log_file, msg, output=True)
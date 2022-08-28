import asyncio
from unittest import TestCase

from onchain_monitor.ws.socket_client_service import SocketClientService


class TestSocketClientService(TestCase):

    def setUp(self) -> None:
        pass

    def test_wss_connect(self):
        wss_uri = 'wss://kovan.infura.io/ws/v3/ebd7174b1e35424f9b5842a4f2f7cc4a'
        scb_str = '{"jsonrpc":"2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}'
        ws = SocketClientService(wss_uri).subscribe(scb_str)
        asyncio.run(ws.run())

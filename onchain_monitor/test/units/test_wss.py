import asyncio
import json
from unittest import TestCase

from websockets import connect


class TestWss(TestCase):

    def setUp(self) -> None:
        pass

    def test_connect_infura_wss(self):
        data = asyncio.run(self.communiting("wss://kovan.infura.io/ws/v3/ebd7174b1e35424f9b5842a4f2f7cc4a"))
        self.assertIsNotNone(data['id'])
        self.assertEqual(data['id'], 1)

        self.assertIsNotNone(data['result'])
        result = int(data['result'], 16)
        # print('result', result)
        self.assertGreater(result, 33475368)

    def test_connect_alchemy_wss(self):
        wss_gateway = 'wss://eth-goerli.g.alchemy.com/v2/fZ4bHjl2AL7bfyIQf4h2EkGjPq0jzjU8'
        data = asyncio.run(self.communiting(wss_gateway))

        self.assertIsNotNone(data['id'])
        self.assertEqual(data['id'], 1)

        self.assertIsNotNone(data['result'])
        result = int(data['result'], 16)
        # print('result', result)
        self.assertGreater(result, 7474966)


    async def communiting(self, uri):
        # print('certifi.where()', certifi.where())
        # print('ssl.get_default_verify_paths()',ssl.get_default_verify_paths())
        async with connect(uri) as websocket:
            await websocket.send('{"jsonrpc": "2.0", "id": 1, "method": "eth_blockNumber", "params": []}')
            data = await websocket.recv()
            # print('data', data)
            data = json.loads(data)
            return data
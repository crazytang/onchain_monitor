import asyncio

from django.core.management import BaseCommand

from oc_django.helpers.utils import check_network_name
from onchain_monitor.models.common_contract import CommonContract
from onchain_monitor.services.common_contract_service import CommonContractService
from onchain_monitor.ws.socket_client_service import SocketClientService


class Command(BaseCommand):
    help = 'Connect to Websocket Node and import data as our requirement'

    def add_arguments(self, parser):
        parser.add_argument('network', type=str, default='kovan', help='network name')

    def handle(self, *args, **options):
        network = options.get('network')

        rs, tip = check_network_name(network)
        if not rs:
            print(tip)
            return
        contract_addresses = CommonContractService.get_contract_addresses()

        scb_str = '{"jsonrpc":"2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}'
        ws = SocketClientService(network).subscribe(scb_str).set_restric_addresses(contract_addresses)
        asyncio.run(ws.run())
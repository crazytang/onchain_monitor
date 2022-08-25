from pprint import pprint

from django.core.management import BaseCommand

from onchain_monitor.models.common_contract import CommonContract


class Command(BaseCommand):
    help = 'It is a test command'

    def add_arguments(self, parser):
        # parser.add_argument('poll_ids', nargs='+', type=int)
        pass

    def handle(self, *args, **options):
        print('in test_command')

        rs = CommonContract.objects.first()
        pprint(rs)


from onchain_monitor.queue.tx_data_job import TxDataService


class JobHandler:

    def dispatch(self, type, data):
        """
        dispatching handler job task
        you need to create a handler here before you want push a new task on queue
        """

        if type == 'tx_queue':
            self.handle_tx(data)

    def handle_tx(self, data):
        TxDataService.handle(data)
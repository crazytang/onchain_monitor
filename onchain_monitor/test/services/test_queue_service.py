
from unittest import TestCase
import django_rq

from onchain_monitor.queue.job_handler import JobHandler


class TestQueueService(TestCase):

    def setUp(self) -> None:
        pass

    def test_push_to_queue(self):
        queue = django_rq.get_queue()
        type = "tx_queue"
        data = {
            "tx_hash": "0x16b3a5ce4a6f8acc08b8f9113859b0c28f98b395c9a540a1721cc0ea78e4169f",
            "network": "kovan"
        }
        # handler_job = HandlerJob()
        queue.enqueue(JobHandler().dispatch, type, data)
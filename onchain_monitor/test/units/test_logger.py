import datetime
from django.core.files import File
from unittest import TestCase

from oc_django.libs.log_service import LogService


class TestLogger(TestCase):

    def setUp(self) -> None:
        pass

    def test_write_to_log(self):
        """
        测试日志
        :return:
        """
        test_str = '##test_str_log_%s##' % datetime.datetime.now()
        file = LogService.write_to_log('', 'test.log', test_str)

        f = open(file, 'r')
        myfile = File(f)
        file_content = myfile.read()
        myfile.close()

        self.assertTrue(test_str in file_content)
from pprint import pprint

from django.db import connection
from django.db.backends.utils import CursorWrapper
from django.test import TestCase


class TestDB(TestCase):
    def setUp(self) -> None:
        pass
        # pprint('this is setUp()')

    def test_connection(self):
        """
        测试数据库连接
        :return:
        """
        cursor: CursorWrapper = connection.cursor()
        # self.assertIsInstance(cursor)
        rows_num:int = cursor.execute('show databases')
        self.assertGreater(rows_num, 0)
        rs = cursor.fetchall()
        has = False
        for row in rs:
            if row[0] == 'onchain':
                has = True
                break

        self.assertTrue(has)
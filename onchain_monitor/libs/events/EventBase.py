import json
from abc import abstractmethod

from django.db.models.expressions import NoneType


class EventBase:
    @abstractmethod
    def fetchTo(self, data:[]):
        pass

    def __str__(self):
        # _dict = {}
        # keys = self.__dict__.keys()
        # for k in keys:
        #     if type(self.__dict__[k]) == NoneType:
        #         _dict[k] = ''
        #     else:
        #         _dict[k] = self.__dict__[k]
        _dict = self.__dict__
        return json.dumps(_dict)
        # str(self.__dict__)

    def toJson(self):
        _dict = self.__dict__
        return json.dumps(_dict)
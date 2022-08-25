class DjBaseObject(object):

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)

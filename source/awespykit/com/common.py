# coding: utf-8


class VerInfo:
    defver = "0.0.0"

    def __init__(self, ver=defver):
        assert isinstance(ver, str)
        self.__ver = ver

    def __repr__(self):
        if not self.__ver:
            return self.defver
        return self.__ver

    __str__ = __repr__

    def is_null(self):
        return self.__ver == self.defver

    def set(self, ver: str):
        assert isinstance(ver, str)
        if ver:
            self.__ver = ver
        else:
            self.__ver = self.defver
        return self.__ver

# coding: utf-8

from typing import Sequence

from fastpip import index_urls

from .abstract_config import AbstractConfig
from .package_manager import get_shared_pypaths


class IndexManagerConfig(AbstractConfig):
    _key_index_urls = "index_urls"
    _key_window_size = "window_size"

    CONFIGFILE = "indexurl_manager.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE)

    @property
    def index_urls(self):
        if self._key_index_urls not in self:
            self[self._key_index_urls] = index_urls.copy()
        return self[self._key_index_urls]

    @index_urls.setter
    def index_urls(self, value: dict):
        assert isinstance(value, dict)
        self[self._key_index_urls] = value

    @property
    def cur_pypaths(self):
        shared_pypaths = get_shared_pypaths()
        if shared_pypaths is None:
            return list()
        assert isinstance(shared_pypaths, list)
        return shared_pypaths

    @property
    def window_size(self):
        if self._key_window_size not in self:
            self[self._key_window_size] = 1000, 500
        return self[self._key_window_size]

    @window_size.setter
    def window_size(self, value):
        assert isinstance(value, Sequence)
        assert len(value) == 2
        assert isinstance(value[0], int) and isinstance(value[1], int)
        self[self._key_window_size] = value

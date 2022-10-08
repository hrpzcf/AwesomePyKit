# coding: utf-8

from fastpip import index_urls

from .abstract_settings import AbstractSettings
from .package_manager import get_global_pypaths


class IndexManagerSettings(AbstractSettings):
    key_index_urls = "index_urls"

    CONFIGFILE = "indexurl_manager.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE, dict)

    @property
    def index_urls(self):
        if self.key_index_urls not in self:
            self[self.key_index_urls] = index_urls.copy()
        return self[self.key_index_urls]

    @index_urls.setter
    def index_urls(self, value: dict):
        assert isinstance(value, dict)
        self[self.key_index_urls] = value

    @property
    def cur_pypaths(self):
        global_pypaths = get_global_pypaths()
        if global_pypaths is None:
            return list()
        assert isinstance(global_pypaths, list)
        return global_pypaths

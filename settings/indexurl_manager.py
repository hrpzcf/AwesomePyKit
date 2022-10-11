# coding: utf-8

from fastpip import index_urls

from .abstract_settings import AbstractSettings
from .package_manager import get_shared_pypaths


class IndexManagerSettings(AbstractSettings):
    key_index_urls = "index_urls"

    CONFIGFILE = "indexurl_manager.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE)

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
        shared_pypaths = get_shared_pypaths()
        if shared_pypaths is None:
            return list()
        assert isinstance(shared_pypaths, list)
        return shared_pypaths

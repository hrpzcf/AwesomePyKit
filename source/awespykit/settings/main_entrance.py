# coding: utf-8

from typing import Sequence

from com import *

from .abstract_config import AbstractConfig


class MainEntranceConfig(AbstractConfig):
    _key_app_style = "app_style"
    _key_window_size = "window_size"

    CONFIGFILE = "main_entrance.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE)

    @property
    def app_style(self):
        return self.setdefault(self._key_app_style, 2)

    @app_style.setter
    def app_style(self, value):
        assert isinstance(value, AppStyle)
        self[self._key_app_style] = value

    @property
    def window_size(self):
        if self._key_window_size not in self:
            self[self._key_window_size] = 260, 320
        return self[self._key_window_size]

    @window_size.setter
    def window_size(self, value):
        assert isinstance(value, Sequence)
        assert len(value) == 2
        assert isinstance(value[0], int) and isinstance(value[1], int)
        self[self._key_window_size] = value

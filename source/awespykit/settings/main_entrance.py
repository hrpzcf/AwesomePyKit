# coding: utf-8

from typing import Sequence

from .abstract_config import AbstractConfig


class MainEntranceConfig(AbstractConfig):
    _key_window_size = "window_size"

    CONFIGFILE = "main_entrance.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE)

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

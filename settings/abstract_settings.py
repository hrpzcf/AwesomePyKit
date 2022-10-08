# coding: utf-8

import json
from pathlib import Path

from . import config_root


class AbstractSettings(dict):
    ROOT = Path(config_root)

    def __init__(self, fname, default):
        super().__init__()
        self.__default = default
        self.__cfg = self.ROOT.joinpath(fname)
        self.load_config()

    def load_config(self):
        if not self.ROOT.exists():
            self.ROOT.mkdir(parents=True)
        self.update(self._load_json())

    def save_config(self):
        try:
            with open(self.__cfg, "wt", encoding="utf-8") as f:
                json.dump(self, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def _load_json(self):
        """__cfg 文件无法读取则调用 __default 取值并返回"""
        if not self.__cfg.exists():
            data = self.__default()
            try:
                with open(self.__cfg, "wt", encoding="utf-8") as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
            except Exception:
                pass
            return data
        try:
            with open(self.__cfg, "rt", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return self.__default()

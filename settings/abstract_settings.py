# coding: utf-8

import json
from pathlib import Path

from . import config_root


class AbstractSettings(dict):
    ROOT = Path(config_root)

    def __init__(self, fname):
        super().__init__()
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
            default_data = dict()
            try:
                with open(self.__cfg, "wt", encoding="utf-8") as f:
                    json.dump(default_data, f, indent=4, ensure_ascii=False)
            except Exception:
                pass
            return default_data
        try:
            with open(self.__cfg, "rt", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return dict()

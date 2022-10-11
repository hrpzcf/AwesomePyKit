# coding: utf-8

import json
from pathlib import Path

from . import config_root


class AbstractSettings(dict):
    root = Path(config_root)

    def __init__(self, fname):
        super().__init__()
        self.__cfg = self.root.joinpath(fname)
        self.__load_json()

    def save_config(self):
        try:
            with open(self.__cfg, "wt", encoding="utf-8") as f:
                json.dump(self, f, indent=4, ensure_ascii=False)
        except Exception:
            pass

    def __load_json(self):
        """如果 __cfg 文件无法读取则返回空字典"""
        try:
            if not self.root.exists():
                self.root.mkdir(parents=True)
        except Exception:
            return
        if not self.__cfg.exists():
            try:
                with open(self.__cfg, "wt", encoding="utf-8") as f:
                    json.dump(dict(), f)
            except Exception:
                return
        else:
            try:
                with open(self.__cfg, "rt", encoding="utf-8") as f:
                    self.update(json.load(f))
            except Exception:
                return

# coding: utf-8

import json
import os
import os.path as op
import sys
from pathlib import Path

_frozen_program = getattr(sys, "frozen", False)
if _frozen_program:
    # noinspection PyUnresolvedReferences
    _res_root = sys._MEIPASS
else:
    _res_root = op.dirname(op.dirname(op.abspath(__file__)))
_appdata_local_folder = os.getenv("LOCALAPPDATA")
if not _appdata_local_folder:
    if _frozen_program:
        _user_data_root = op.dirname(sys.executable)
    else:
        _user_data_root = _res_root
else:
    _user_data_root = op.join(_appdata_local_folder, "Awespykit")
config_root = op.join(_user_data_root, "config")
themes_root = op.join(_user_data_root, "themes")


def generate_respath(*p):
    """
    用于在不同运行环境之下获取正确的资源文件路径

    不同的运行环境：Python 源代码运行、Pyinstaller 打包为单文件运行/打包为单目录运行
    """
    return op.join(_res_root, *p)


class AbstractConfig(dict):
    root = Path(config_root)

    def __init__(self, fname):
        super().__init__()
        self.__cfg = self.root.joinpath(fname)
        self.__load_json()

    def save_config(self):
        try:
            with open(self.__cfg, "wt", encoding="utf-8") as f:
                json.dump(self, f, ensure_ascii=False)
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

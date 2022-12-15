# coding: utf-8

__doc__ = "主题相关工具"

import json
from pathlib import Path
from typing import *
import re
from com import *

from PyQt5.QtCore import QFile, QIODevice
from settings import themes_root


class ThemeData:
    def __init__(self, tid=-1, name=None, stylesheet=None):
        self.__index = tid
        self.__name = name
        self.__sheet = stylesheet

    def __repr__(self):
        return f"ThemeData(index={self.__index}, name={self.__name})"

    __str__ = __repr__

    @property
    def index(self):
        return self.__index

    @property
    def name(self):
        return self.__name

    @property
    def sheet(self):
        return self.__sheet


class Themes(list):
    __theme_dir = Path(themes_root)
    __key_theme_name = "name"
    __key_theme_sheet = "stylesheet"
    __theme_id = -1

    def __init__(self):
        super(Themes, self).__init__()
        self.__load_builtin_themes()
        self.__load_external_themes()

    @classmethod
    def __generate_theme_id(cls):
        cls.__theme_id += 1
        return cls.__theme_id

    def __load_builtin_themes(self):
        for theme in (
            QFile(":/themes/dark-theme.qss"),
            QFile(":/themes/light-theme.qss"),
        ):
            if not theme.open(QIODevice.ReadOnly):
                continue
            theme_name, stylesheet = self.__detach_text_content(
                theme.readAll().data().decode("utf-8")
            )
            theme.close()
            if not (theme_name and stylesheet):
                continue
            self.append(
                ThemeData(self.__generate_theme_id(), theme_name, stylesheet)
            )

    def __load_external_themes(self):
        for theme in self.__theme_dir.glob("*.qss"):
            try:
                with open(theme, "rt", encoding="utf-8") as fobj:
                    theme_name, stylesheet = self.__detach_text_content(
                        fobj.read()
                    )
                if not (theme_name and stylesheet):
                    continue
                self.append(
                    ThemeData(
                        self.__generate_theme_id(), theme_name, stylesheet
                    )
                )
            except Exception:
                continue

    @staticmethod
    def __detach_text_content(string: str) -> Tuple[str, str]:
        lines = string.split("\n", 2)
        if len(lines) < 3:
            return EMPTY_STR, EMPTY_STR
        _, name_line, stylesheet = lines
        theme_name = re.match(r"/\*\sTheme Name:\s?(.*)\s\*/", name_line)
        if not theme_name:
            return EMPTY_STR, EMPTY_STR
        return theme_name.group(1), stylesheet

# coding: utf-8

__doc__ = "主题相关工具"

__all__ = ["_App", "PreThemeList", "ThemeData", "Themes"]

import re
import sys
from os import path
from pathlib import Path
from typing import *

from com import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from res.res import *
from settings import themes_root

_App = QApplication(sys.argv)
try:
    from qdarkstyle import load_stylesheet_pyqt5
except ImportError:
    load_stylesheet_pyqt5 = None
try:
    from qt_material import apply_stylesheet, list_themes
except ImportError:
    list_themes = None
    apply_stylesheet = None


class ThemeData:
    def __init__(self, index, name, data, dtype=DataType.Sheet):
        self.__index = index
        self.__name = name
        self.__data = data
        self.__type = dtype
        self.__place_holder = None
        self.__itembg_normal = None
        self.__itembg_selected = None

    def __repr__(self):
        return f"ThemeData(index={self.__index}, name={self.__name})"

    __str__ = __repr__

    @property
    def index(self) -> int:
        return self.__index

    @property
    def name(self) -> str:
        return self.__name

    @property
    def data(self) -> str:
        return self.__data

    @property
    def type(self) -> DataType:
        return self.__type

    @property
    def place_holder(self) -> str:
        return self.__place_holder

    @place_holder.setter
    def place_holder(self, value):
        assert isinstance(value, str)
        self.__place_holder = value

    @property
    def itembg_normal(self) -> str:
        return self.__itembg_normal

    @itembg_normal.setter
    def itembg_normal(self, value):
        assert isinstance(value, str)
        self.__itembg_normal = value

    @property
    def itembg_selected(self) -> str:
        return self.__itembg_selected

    @itembg_selected.setter
    def itembg_selected(self, value):
        assert isinstance(value, str)
        self.__itembg_selected = value

    def getColors(self):
        return self.__place_holder, self.__itembg_normal, self.__itembg_selected


class Themes(list):
    __theme_dir = Path(themes_root)
    __theme_id = -1
    __id_increment = 1
    __pat_pht = re.compile(
        r"QPlaceHolderText\s*{\s*color\s*:\s*([#\da-zA-Z]+)\s*;\s*}", re.S
    )
    __pat_tibgn = re.compile(
        r"QTable(?:View|Widget)::item\s*{.*?background-color\s*:\s*([#\da-zA-Z]+)\s*;\s*}",
        re.S,
    )
    __pat_tibgs = re.compile(
        r"QTable(?:View|Widget)::item:selected\s*{.*?background-color\s*:\s*([#\da-zA-Z]+)\s*;\s*}",
        re.S,
    )
    __extra = {
        "warning": "#ffc107",
        "success": "#17a2b8",
        "danger": "#dc3545",
        "font_family": "Microsoft YaHei UI",
    }

    def __load_resetstyle_and_extra(self):
        qt_material_dark = QFile(":/themes/qt_material_dark.qss")
        if qt_material_dark.open(QIODevice.ReadOnly):
            self.__qt_material_dark = (
                qt_material_dark.readAll().data().decode("utf-8")
            )
        qt_material_all = QFile(":/themes/qt_material_all.qss")
        if qt_material_all.open(QIODevice.ReadOnly):
            self.__qt_material_all = (
                qt_material_all.readAll().data().decode("utf-8")
            )
        reset_style = QFile(":/themes/reset-style.qss")
        if reset_style.open(QIODevice.ReadOnly):
            self.__resetsheet = reset_style.readAll().data().decode("utf-8")

    def __init__(self):
        super(Themes, self).__init__()
        self.__resetsheet = EMPTY_STR
        self.__qt_material_all = EMPTY_STR
        self.__qt_material_dark = EMPTY_STR
        self.__load_resetstyle_and_extra()
        self.__current = 0
        self.__load_builtin_themes()
        self.__load_external_themes()

    def apply_theme(self, index: int):
        assert isinstance(index, int)
        assert isinstance(_App, QApplication)
        if index < 0 or index >= len(self):
            index = 0
        self.__current = index
        theme_data: ThemeData = self[index]
        if (
            theme_data.type == DataType.Sheet
            or theme_data.type == DataType.Style
        ):
            palette = QApplication.palette()
            if theme_data.place_holder is None:
                theme_data.place_holder = "#ADB4B4"
            palette.setColor(
                QPalette.PlaceholderText, QColor(theme_data.place_holder)
            )
            QApplication.setPalette(palette)
        if theme_data.type == DataType.Sheet:
            _App.setStyle(AppStyle.WindowsVista.name)
            _App.setStyleSheet(theme_data.data)
        elif theme_data.type == DataType.Style:
            _App.setStyle(theme_data.data)
            _App.setStyleSheet(self.__resetsheet)
        elif theme_data.type == DataType.XmlName:
            if apply_stylesheet is not None:
                _App.setStyle(AppStyle.WindowsVista.name)
                if theme_data.data.startswith("light_"):
                    apply_stylesheet(
                        _App,
                        theme_data.data,
                        invert_secondary=True,
                        extra=self.__extra,
                    )
                else:
                    apply_stylesheet(_App, theme_data.data, extra=self.__extra)
                current_style_sheet = _App.styleSheet()
                current_style_sheet = (
                    self.__resetsheet
                    + current_style_sheet
                    + self.__qt_material_all
                )
                if theme_data.data.startswith("dark_"):
                    current_style_sheet += self.__qt_material_dark
                _App.setStyleSheet(current_style_sheet)
        return index

    @property
    def current(self) -> ThemeData:
        return self[self.__current]

    @classmethod
    def __get_themeid(cls):
        cls.__theme_id += cls.__id_increment
        return cls.__theme_id

    @classmethod
    def __det_extra(cls, string: str):
        pht, tibgn, tibgs = None, None, None
        sch_pht = cls.__pat_pht.search(string)
        if sch_pht:
            pht = sch_pht.group(1)
        sch_tibgn = cls.__pat_tibgn.search(string)
        if sch_tibgn:
            tibgn = sch_tibgn.group(1)
        sch_tibgs = cls.__pat_tibgs.search(string)
        if sch_tibgs:
            tibgs = sch_tibgs.group(1)
        return pht, tibgn, tibgs

    def __load_builtin_themes(self):
        # 本工具箱内置的 Qt 样式表，有浅灰和暗色两套
        for theme in (
            QFile(":/themes/gray-theme.qss"),
            QFile(":/themes/dark-theme.qss"),
        ):
            if not theme.open(QIODevice.ReadOnly):
                continue
            theme_name, stylesheet = self.__detach_text_content(
                theme.readAll().data().decode("utf-8")
            )
            theme.close()
            if not (theme_name and stylesheet):
                continue
            phtc, tibgn, tibgs = self.__det_extra(stylesheet)
            theme_data = ThemeData(
                self.__get_themeid(), theme_name, stylesheet, DataType.Sheet
            )
            theme_data.place_holder = phtc
            theme_data.itembg_normal = tibgn
            theme_data.itembg_selected = tibgs
            self.append(theme_data)
        # Qt 内置的 2 种界面风格：系统原生风格、Fusion 风格
        self.append(
            ThemeData(
                self.__get_themeid(),
                "Fusion",
                AppStyle.Fusion.name,
                DataType.Style,
            )
        )
        self.append(
            ThemeData(
                self.__get_themeid(),
                "原生风格",
                AppStyle.WindowsVista.name,
                DataType.Style,
            )
        )
        # 开源的第三方样式表：qdarkstyle
        if load_stylesheet_pyqt5 is not None:
            self.append(
                ThemeData(
                    self.__get_themeid(),
                    "QDarkStyle",
                    load_stylesheet_pyqt5(),
                    DataType.Sheet,
                )
            )
        # 开源的第三方样式表：qt-material
        if list_themes is not None and apply_stylesheet is not None:
            for xml_name in list_themes():
                self.append(
                    ThemeData(
                        self.__get_themeid(),
                        path.splitext(xml_name)[0],
                        xml_name,
                        DataType.XmlName,
                    )
                )

    def __load_external_themes(self):
        if not self.__theme_dir.exists():
            self.__theme_dir.mkdir(exist_ok=True)
            return
        elif not self.__theme_dir.is_dir():
            return
        for theme in self.__theme_dir.glob("*.qss"):
            try:
                with open(theme, "rt", encoding="utf-8") as fobj:
                    theme_name, stylesheet = self.__detach_text_content(
                        fobj.read()
                    )
                if not (theme_name and stylesheet):
                    continue
                phtc, tibgn, tibgs = self.__det_extra(stylesheet)
                theme_data = ThemeData(
                    self.__get_themeid(), theme_name, stylesheet, DataType.Sheet
                )
                theme_data.place_holder = phtc
                theme_data.itembg_normal = tibgn
                theme_data.itembg_selected = tibgs
                self.append(theme_data)
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


PreThemeList = Themes()

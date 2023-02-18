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
    Transparent = "transparent"
    PlaceHolderLight = "#ADB4B4"
    PlaceHolderDark = "#4F535B"

    def __init__(self, index, name, data, dtype=DataType.StyleSheet):
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

    @staticmethod
    def __read_builtin_file(builtin_qfile_path: str):
        qfile_obj = QFile(builtin_qfile_path)
        result = qfile_obj.open(QIODevice.ReadOnly)
        assert result, f"Failed to open file: {builtin_qfile_path}"
        return qfile_obj.readAll().data().decode("utf-8")

    def __load_extra_stylesheets(self):
        self.__qt_material_dark = self.__read_builtin_file(
            ":/themes/qt_material_dark.qss"
        )
        self.__qt_material_all = self.__read_builtin_file(
            ":/themes/qt_material_all.qss"
        )
        self.__base_stylesheet = self.__read_builtin_file(
            ":/themes/base-stylesheet.qss"
        )
        self.__qdarkstyle_extra = self.__read_builtin_file(
            ":/themes/qdarkstyle-extra.qss"
        )

    def __init__(self):
        super(Themes, self).__init__()
        self.__base_stylesheet = EMPTY_STR
        self.__qt_material_all = EMPTY_STR
        self.__qt_material_dark = EMPTY_STR
        self.__qdarkstyle_extra = EMPTY_STR
        self.__load_extra_stylesheets()
        self.__current_index = 0
        self.__load_builtin_themes()
        self.__load_external_themes()

    def apply_theme(self, index: int):
        assert isinstance(_App, QApplication)
        assert isinstance(index, int)
        if index < 0 or index >= len(self):
            index = 0
        self.__current_index = index
        theme_data: ThemeData = self[index]
        if not theme_data.type & DataType.QtMaterial and (
            theme_data.type & DataType.QtPreStyle
            or theme_data.type & DataType.StyleSheet
        ):
            palette = QApplication.palette()
            if theme_data.place_holder is None:
                if theme_data.type & DataType.DarkTheme:
                    theme_data.place_holder = theme_data.PlaceHolderDark
                elif theme_data.type & DataType.LightTheme:
                    theme_data.place_holder = theme_data.PlaceHolderLight
                else:
                    theme_data.place_holder = theme_data.Transparent
            palette.setColor(
                QPalette.PlaceholderText, QColor(theme_data.place_holder)
            )
            QApplication.setPalette(palette)
        # ResetStyle 优先级比 QtPreStyle 优先级高
        if theme_data.type & DataType.ResetStyle:
            _App.setStyle(AppStyle.WindowsVista.name)
        elif theme_data.type & DataType.QtPreStyle:
            _App.setStyle(theme_data.data)
        # ResetSheet 优先级比 StyleSheet 优先级高
        if theme_data.type & DataType.ResetSheet:
            _App.setStyleSheet(self.__base_stylesheet)
        elif theme_data.type & DataType.StyleSheet:
            final_stylesheet = theme_data.data
            if theme_data.type & DataType.QDarkStyle:
                final_stylesheet += self.__qdarkstyle_extra
            _App.setStyleSheet(final_stylesheet)
        if theme_data.type & DataType.QtMaterial and isinstance(
            apply_stylesheet, Callable
        ):
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
                self.__base_stylesheet
                + current_style_sheet
                + self.__qt_material_all
            )
            if theme_data.data.startswith("dark_"):
                current_style_sheet += self.__qt_material_dark
            _App.setStyleSheet(current_style_sheet)
        return index

    @property
    def current(self) -> ThemeData:
        return self[self.__current_index]

    @classmethod
    def __get_themeid(cls):
        cls.__theme_id += cls.__id_increment
        return cls.__theme_id

    @classmethod
    def __detect_extra(cls, string: str):
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
            theme_name, stylesheet = self.__detach(
                theme.readAll().data().decode("utf-8")
            )
            theme.close()
            if not (theme_name and stylesheet):
                continue
            phtc, tibgn, tibgs = self.__detect_extra(stylesheet)
            theme_data = ThemeData(
                self.__get_themeid(),
                theme_name,
                stylesheet,
                DataType.ResetStyle | DataType.StyleSheet,
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
                DataType.QtPreStyle | DataType.ResetSheet | DataType.LightTheme,
            )
        )
        self.append(
            ThemeData(
                self.__get_themeid(),
                "原生风格",
                AppStyle.WindowsVista.name,
                DataType.QtPreStyle | DataType.ResetSheet | DataType.LightTheme,
            )
        )
        # 开源的第三方样式表：QDarkStyle
        if isinstance(load_stylesheet_pyqt5, Callable):
            self.append(
                ThemeData(
                    self.__get_themeid(),
                    "QDarkStyle",
                    load_stylesheet_pyqt5(),
                    DataType.ResetStyle
                    | DataType.StyleSheet
                    | DataType.QDarkStyle
                    | DataType.DarkTheme,
                )
            )
        # 开源的第三方样式表：qt-material
        if isinstance(list_themes, Callable) and isinstance(
            apply_stylesheet, Callable
        ):
            for xml_name in list_themes():
                self.append(
                    ThemeData(
                        self.__get_themeid(),
                        path.splitext(xml_name)[0],
                        xml_name,
                        DataType.ResetStyle | DataType.QtMaterial,
                    )
                )

    def __load_external_themes(self):
        if not self.__theme_dir.exists():
            self.__theme_dir.mkdir(parents=True, exist_ok=True)
            return
        elif not self.__theme_dir.is_dir():
            return
        for theme in self.__theme_dir.glob("*.qss"):
            try:
                with open(theme, "rt", encoding="utf-8") as fobj:
                    theme_name, sheet = self.__detach(fobj.read())
                if not (theme_name and sheet):
                    continue
                (
                    placeholder_color,
                    tabitembg_normal,
                    tabitembg_selected,
                ) = self.__detect_extra(sheet)
                theme_data = ThemeData(
                    self.__get_themeid(),
                    theme_name,
                    sheet,
                    DataType.ResetStyle | DataType.StyleSheet,
                )
                theme_data.place_holder = placeholder_color
                theme_data.itembg_normal = tabitembg_normal
                theme_data.itembg_selected = tabitembg_selected
                self.append(theme_data)
            except Exception:
                continue

    @staticmethod
    def __detach(string: str) -> Tuple[str, str]:
        lines = string.split("\n", 2)
        if len(lines) < 3:
            return EMPTY_STR, EMPTY_STR
        _, name_line, stylesheet = lines
        theme_name = re.match(r"/\*\sTheme Name:\s?(.*)\s\*/", name_line)
        if not theme_name:
            return EMPTY_STR, EMPTY_STR
        return theme_name.group(1), stylesheet


PreThemeList = Themes()

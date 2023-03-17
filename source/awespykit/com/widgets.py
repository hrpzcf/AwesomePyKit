# coding: utf-8

__doc__ = """包含一些继承自默认Qt控件的自定义行为控件。"""

import os
from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from utils.thmt import PreThemeList

from .enums import Accept, RoleData


class LineEdit(QLineEdit):
    def __init__(self, accept=None, ext_filter=None):
        super().__init__()
        if accept is None:
            self.__accept = Accept.Dir
        else:
            self.__accept = accept
        if ext_filter is None:
            self.__filter = set()
        else:
            self.__filter = ext_filter
            assert isinstance(ext_filter, set)
        self.__drag_temp = ""

    @property
    def local_path(self):
        return self.text().strip()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            if self.__accept == Accept.Dir:
                event.accept()
            elif self.__accept == Accept.File:
                self.__drag_temp = os.path.realpath(
                    event.mimeData().urls()[0].toLocalFile()
                )
                if (
                    not self.__filter
                    or os.path.splitext(self.__drag_temp)[1] in self.__filter
                ):
                    event.accept()
                else:
                    event.ignore()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if not self.__drag_temp:
            self.__drag_temp = os.path.realpath(
                event.mimeData().urls()[0].toLocalFile()
            )
        if self.__accept == Accept.File and os.path.isfile(self.__drag_temp):
            self.setText(self.__drag_temp)
        elif self.__accept == Accept.Dir and os.path.isdir(self.__drag_temp):
            self.setText(self.__drag_temp)


class TextEdit(QTextEdit):
    def __init__(self, accept=None, ext_filter=None):
        super().__init__()
        self.setLineWrapMode(QTextEdit.NoWrap)
        if accept is None:
            self.__accept = Accept.File
        else:
            self.__accept = accept
        if ext_filter is None:
            self.__filter = set()
        else:
            self.__filter = ext_filter
            assert isinstance(ext_filter, set)
        self.__drag_temp = list()

    @property
    def local_paths(self):
        file_dir_paths = self.toPlainText().split("\n")
        if self.__accept == Accept.Dir:
            return [p for p in file_dir_paths if os.path.isdir(p)]
        if self.__accept == Accept.File:
            return [p for p in file_dir_paths if os.path.isfile(p)]
        return list()

    def __stash_from_urls(self, urls: List[QUrl]):
        self.__drag_temp.clear()
        for file_or_dir in (path.toLocalFile() for path in urls):
            file_or_dir = os.path.realpath(file_or_dir)
            if os.path.isfile(file_or_dir):
                self.__drag_temp.append(file_or_dir)
                continue
            self.__drag_temp.append(file_or_dir)
            for root, _, files in os.walk(file_or_dir):
                self.__drag_temp.extend(
                    os.path.join(root, filename) for filename in files
                )

    def dragEnterEvent(self, event: QDragEnterEvent):
        self.__drag_temp.clear()
        if event.mimeData().hasUrls():
            if self.__accept == Accept.File:
                self.__stash_from_urls(event.mimeData().urls())
                if not self.__filter or set(
                    os.path.splitext(fp)[1]
                    for fp in self.__drag_temp
                    if os.path.isfile(fp)
                ).issubset(self.__filter):
                    event.accept()
                else:
                    event.ignore()
            elif self.__accept == Accept.Dir:
                event.accept()
            else:
                event.ignore()
            if not self.toPlainText().endswith("\n"):
                self.append("")
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        cur_text = self.toPlainText()
        super().dropEvent(event)
        if not self.__drag_temp:
            self.__stash_from_urls(event.mimeData().urls())
        if self.__accept == Accept.File:
            self.setText(
                cur_text
                + "\n".join(p for p in self.__drag_temp if os.path.isfile(p))
            )
        elif self.__accept == Accept.Dir:
            self.setText(
                cur_text
                + "\n".join(p for p in self.__drag_temp if os.path.isdir(p))
            )
        else:
            self.setText("")
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximumHeight()
        )


class PlainTextEdit(QPlainTextEdit):
    def __init__(self, accept=None, ext_filter=None):
        super().__init__()
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        if accept is None:
            self.__accept = Accept.File
        else:
            self.__accept = accept
        if ext_filter is None:
            self.__filter = set()
        else:
            self.__filter = ext_filter
            assert isinstance(ext_filter, set)
        self.__drag_temp = list()

    @property
    def local_paths(self):
        file_dir_paths = self.toPlainText().split("\n")
        if self.__accept == Accept.Dir:
            return [p for p in file_dir_paths if os.path.isdir(p)]
        if self.__accept == Accept.File:
            return [p for p in file_dir_paths if os.path.isfile(p)]
        return list()

    def __stash_from_urls(self, urls: List[QUrl]):
        self.__drag_temp.clear()
        for file_or_dir in (path.toLocalFile() for path in urls):
            file_or_dir = os.path.realpath(file_or_dir)
            if os.path.isfile(file_or_dir):
                self.__drag_temp.append(file_or_dir)
                continue
            self.__drag_temp.append(file_or_dir)
            for root, _, files in os.walk(file_or_dir):
                self.__drag_temp.extend(
                    os.path.join(root, filename) for filename in files
                )

    def dragEnterEvent(self, event: QDragEnterEvent):
        self.__drag_temp.clear()
        if event.mimeData().hasUrls():
            if self.__accept == Accept.File:
                self.__stash_from_urls(event.mimeData().urls())
                if not self.__filter or set(
                    os.path.splitext(fp)[1]
                    for fp in self.__drag_temp
                    if os.path.isfile(fp)
                ).issubset(self.__filter):
                    event.accept()
                else:
                    event.ignore()
            elif self.__accept == Accept.Dir:
                event.accept()
            else:
                event.ignore()
            if not self.toPlainText().endswith("\n"):
                self.appendPlainText("")
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        cur_text = self.toPlainText()
        super().dropEvent(event)
        if not self.__drag_temp:
            self.__stash_from_urls(event.mimeData().urls())
        if self.__accept == Accept.File:
            self.setPlainText(
                cur_text
                + "\n".join(p for p in self.__drag_temp if os.path.isfile(p))
            )
        elif self.__accept == Accept.Dir:
            self.setPlainText(
                cur_text
                + "\n".join(p for p in self.__drag_temp if os.path.isdir(p))
            )
        else:
            self.setPlainText("")
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximumHeight()
        )


class ItemDelegate(QItemDelegate):
    """表格 QTableWidget 的 item 委托"""

    def __init__(self, parent: QTableWidget, editable: bool = True):
        self.__parent = parent
        super(ItemDelegate, self).__init__()
        self.__editable = editable

    @property
    def Editable(self):
        return self.__editable

    @Editable.setter
    def Editable(self, value):
        assert isinstance(value, bool)
        self.__editable = value

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:
        if self.__editable:
            return super().createEditor(parent, option, index)
        return None

    def paint(
        self,
        painter: QPainter,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> None:
        phtc, tibgn, tibgs = PreThemeList.current.getColors()
        if phtc and tibgn and tibgs:
            if option.state & QStyle.State_Selected:
                background_color = QColor(tibgs)
            else:
                background_color = QColor(tibgn)
        else:
            if option.state & QStyle.State_Selected:
                if option.state & QStyle.State_Active:
                    color_group = QPalette.Active
                else:
                    color_group = QPalette.Inactive
                background_color = self.__parent.palette().color(
                    color_group, QPalette.Highlight
                )
            else:
                background_color = QColor("transparent")
        painter.fillRect(option.rect, background_color)
        text_data = index.data(Qt.DisplayRole)
        if not text_data:
            return
        execution_results = index.data(Qt.UserRole)
        if execution_results is None:
            execution_results = RoleData.Unknown
        if execution_results == RoleData.Success:
            foreground_color = QColor("green")
        elif execution_results == RoleData.Failed:
            foreground_color = QColor("red")
        elif execution_results == RoleData.Warning:
            foreground_color = QColor("orange")
        else:
            foreground_color = QColor("black")
        painter.setPen(foreground_color)
        alignment = index.data(Qt.TextAlignmentRole)
        if alignment is None:
            alignment = Qt.AlignCenter
        painter.drawText(option.rect, alignment, text_data)

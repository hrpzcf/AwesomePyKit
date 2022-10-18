# coding: utf-8

__doc__ = """包含一些继承自默认Qt控件的自定义行为控件。"""

import os
from typing import List

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class QLineEditMod(QLineEdit):
    def __init__(self, accept="dir", file_filter=None):
        super().__init__()
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.__accept = accept
        if file_filter is None:
            self.__filter = set()
        else:
            self.__filter = file_filter
        self.__drag_temp = ""

    @property
    def local_path(self):
        return self.text().strip()

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            if self.__accept == "file":
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
            elif self.__accept == "dir":
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if not self.__drag_temp:
            self.__drag_temp = os.path.realpath(
                event.mimeData().urls()[0].toLocalFile()
            )
        if self.__accept == "file" and os.path.isfile(self.__drag_temp):
            self.setText(self.__drag_temp)
        elif self.__accept == "dir" and os.path.isdir(self.__drag_temp):
            self.setText(self.__drag_temp)


class QTextEditMod(QTextEdit):
    def __init__(self, accept="file", file_filter=None):
        super().__init__()
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self.__accept = accept
        if file_filter is None:
            self.__filter = set()
        else:
            self.__filter = file_filter
        self.__drag_temp = list()

    @property
    def local_paths(self):
        file_dir_paths = self.toPlainText().split("\n")
        if self.__accept == "dir":
            return [path for path in file_dir_paths if os.path.isdir(path)]
        if self.__accept == "file":
            return [path for path in file_dir_paths if os.path.isfile(path)]
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
            if self.__accept == "file":
                self.__stash_from_urls(event.mimeData().urls())
                if not self.__filter or set(
                    os.path.splitext(fp)[1]
                    for fp in self.__drag_temp
                    if os.path.isfile(fp)
                ).issubset(self.__filter):
                    event.accept()
                else:
                    event.ignore()
            elif self.__accept == "dir":
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
        if self.__accept == "file":
            self.setText(
                cur_text
                + "\n".join(path for path in self.__drag_temp if os.path.isfile(path))
            )
        elif self.__accept == "dir":
            self.setText(
                cur_text
                + "\n".join(path for path in self.__drag_temp if os.path.isdir(path))
            )
        else:
            self.setText("")
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximumHeight())

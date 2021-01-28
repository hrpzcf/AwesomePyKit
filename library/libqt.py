# coding: utf-8

__doc__ = '''包含一些继承自默认Qt控件的自定义行为控件。'''

import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QTextEdit


class QLineEditMod(QLineEdit):
    def __init__(self, accept='dir', file_filter=set()):
        super().__init__()
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self._accept = accept
        self._filter = file_filter
        self._drag_temp = ''

    @property
    def local_path(self):
        return self.text().strip()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if self._accept == 'file':
                self._drag_temp = os.path.realpath(
                    event.mimeData().urls()[0].toLocalFile()
                )
                if (
                    not self._filter
                    or os.path.splitext(self._drag_temp)[1] in self._filter
                ):
                    event.accept()
                else:
                    event.ignore()
            elif self._accept == 'dir':
                event.accept()
            else:
                event.ignore()
        else:
            event.ignore()

    def dropEvent(self, event):
        if not self._drag_temp:
            self._drag_temp = os.path.realpath(
                event.mimeData().urls()[0].toLocalFile()
            )
        if self._accept == 'file' and os.path.isfile(self._drag_temp):
            self.setText(self._drag_temp)
        elif self._accept == 'dir' and os.path.isdir(self._drag_temp):
            self.setText(self._drag_temp)


class QTextEditMod(QTextEdit):
    def __init__(self, accept='file', file_filter=set()):
        super().__init__()
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self._accept = accept
        self._filter = file_filter
        self._drag_temp = list()

    @property
    def local_paths(self):
        file_dir_paths = self.toPlainText().split('\n')
        if self._accept == 'dir':
            return [path for path in file_dir_paths if os.path.isdir(path)]
        if self._accept == 'file':
            return [path for path in file_dir_paths if os.path.isfile(path)]
        return []

    def _stash_from_urls(self, urls):
        self._drag_temp.clear()
        for file_or_dir in (path.toLocalFile() for path in urls):
            file_or_dir = os.path.realpath(file_or_dir)
            if os.path.isfile(file_or_dir):
                self._drag_temp.append(file_or_dir)
                continue
            self._drag_temp.append(file_or_dir)
            for root, _, files in os.walk(file_or_dir):
                self._drag_temp.extend(
                    os.path.join(root, filename) for filename in files
                )

    def dragEnterEvent(self, event):
        self._drag_temp.clear()
        if event.mimeData().hasUrls():
            if self._accept == 'file':
                self._stash_from_urls(event.mimeData().urls())
                if not self._filter or set(
                    os.path.splitext(fp)[1]
                    for fp in self._drag_temp
                    if os.path.isfile(fp)
                ).issubset(self._filter):
                    event.accept()
                else:
                    event.ignore()
            elif self._accept == 'dir':
                event.accept()
            else:
                event.ignore()
            if not self.toPlainText().endswith('\n'):
                self.append('')
        else:
            event.ignore()

    def dropEvent(self, event):
        cur_text = self.toPlainText()
        super().dropEvent(event)
        if not self._drag_temp:
            self._stash_from_urls(event.mimeData().urls())
        if self._accept == 'file':
            self.setText(
                cur_text
                + '\n'.join(
                    path for path in self._drag_temp if os.path.isfile(path)
                )
            )
        elif self._accept == 'dir':
            self.setText(
                cur_text
                + '\n'.join(
                    path for path in self._drag_temp if os.path.isdir(path)
                )
            )
        else:
            self.setText('')
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximumHeight()
        )

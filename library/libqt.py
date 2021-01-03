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
        self._file_filter = file_filter

    @property
    def local_path(self):
        return self.text().strip()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if self._accept == 'file':
                path = event.mimeData().urls()[0].toLocalFile()
                if (
                    not self._file_filter
                    or os.path.splitext(path)[1] in self._file_filter
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
        path = event.mimeData().urls()[0].toLocalFile()
        if self._accept == 'file' and os.path.isfile(path):
            self.setText(path)
        elif self._accept == 'dir' and os.path.isdir(path):
            self.setText(path)


class QTextEditMod(QTextEdit):
    def __init__(self, accept='file', file_filter=set()):
        super().__init__()
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self._accept = accept
        self._file_filter = file_filter

    @property
    def local_paths(self):
        file_dir_paths = self.toPlainText().split('\n')
        if self._accept == 'dir':
            return [path for path in file_dir_paths if os.path.isdir(path)]
        if self._accept == 'file':
            return [path for path in file_dir_paths if os.path.isfile(path)]
        return []

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if self._accept == 'file':
                if not self._file_filter or set(
                    os.path.splitext(path.toLocalFile())[1]
                    for path in event.mimeData().urls()
                ).issubset(self._file_filter):
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
        files_dirs = (path.toLocalFile() for path in event.mimeData().urls())
        if self._accept == 'file':
            self.setText(
                cur_text
                + '\n'.join(
                    path for path in files_dirs if os.path.isfile(path)
                )
            )
        elif self._accept == 'dir':
            self.setText(
                cur_text
                + '\n'.join(path for path in files_dirs if os.path.isdir(path))
            )
        else:
            self.setText('')
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().maximumHeight()
        )


class TextStream(QTextEdit):
    _DEF_MAX_LINES = 300

    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self._string_list = []
        self._max_lines = self._DEF_MAX_LINES

    def clear(self):
        self.clear()
        self._string_list.clear()

    def write(self, string):
        while len(self._string_list) > self._max_lines:
            del self._string_list[0]
        self._string_list.append(string)
        self.setText('\n'.join(self._string_list))

    @property
    def max_lines(self):
        return self._max_lines

    @max_lines.setter
    def max_lines(self, value):
        if not isinstance(value, int) or value > self._DEF_MAX_LINES:
            value = self._DEF_MAX_LINES
        self._max_lines = value

    @max_lines.deleter
    def max_lines(self):
        self._max_lines = self._DEF_MAX_LINES


# coding: utf-8

__doc__ = '''包含一些继承自默认Qt控件的自定义行为控件。'''

import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QTextEdit


class QLineEditMod(QLineEdit):
    def __init__(self, accept='dir'):
        super().__init__()
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self._accept = accept

    @property
    def local_path(self):
        return self.text().strip()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        path = event.mimeData().urls()[0].toLocalFile()
        if self._accept == 'file' and os.path.isfile(path):
            self.setText(path)
        elif self._accept == 'dir' and os.path.isdir(path):
            self.setText(path)


class QTextEditMod(QTextEdit):
    def __init__(self, accept='file'):
        super().__init__()
        self.setContextMenuPolicy(Qt.NoContextMenu)
        self._accept = accept

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
            event.accept()
            plain_text = self.toPlainText()
            if plain_text and not plain_text.endswith('\n'):
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


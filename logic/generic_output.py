# coding: utf-8

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import *


class GenericOutputWindow(Ui_generic_output, QMainWindow):
    signal_clear_content = pyqtSignal()
    signal_append_line = pyqtSignal(str)

    def __init__(self, parent, title=None, titlebar=False):
        super().__init__(parent)
        self.setupUi(self)
        if title is not None:
            self.setWindowTitle(title)
        if not titlebar:
            self.setWindowFlags(Qt.CustomizeWindowHint | Qt.Window)
        self.signal_slot_connection()
        self.__width = self.width()
        self.__height = self.height()

    def signal_slot_connection(self):
        self.uiPushButton_close_window.clicked.connect(self.hide)
        self.signal_append_line.connect(self.uiPlainTextEdit_output.appendPlainText)
        self.uiPushButton_clear_content.clicked.connect(
            self.uiPlainTextEdit_output.clear
        )
        self.signal_clear_content.connect(self.uiPlainTextEdit_output.clear)

    def resizeEvent(self, event: QResizeEvent):
        self.__width = self.width()
        self.__height = self.height()
        super().resizeEvent(event)

    def set_pos(self, x, y, w, h):
        if w is None:
            w = self.__width
        if h is None:
            h = self.__height
        self.setGeometry(x, y + self.geometry().y() - self.y(), w, h)

    def clear_content(self):
        self.signal_clear_content.emit()

    def add_line(self, string):
        self.signal_append_line.emit(string)

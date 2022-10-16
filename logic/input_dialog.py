# coding: utf-8

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import *


class InputDialog(Ui_input_dialog, QMainWindow):
    def __init__(self, parent, back, title="", w=None, h=None):
        super().__init__(parent)
        self.setupUi(self)
        self.initialize()
        self.__callback = back
        if title:
            self.setWindowTitle(title)
        self.show()
        width = self.width() if w is None else w
        height = self.height() if h is None else h
        self.resize(width, height)

    def initialize(self):
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.uiPushButton_confirm.clicked.connect(self.text_back)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.text_back()

    def text_back(self):
        self.close()
        self.__callback(self.uiLineEdit_input_content.text())

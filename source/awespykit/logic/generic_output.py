# coding: utf-8

from com import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import *


class GenericOutputWindow(Ui_generic_output, QMainWindow):
    signal_clear_content = pyqtSignal()
    signal_append_line = pyqtSignal(str)

    def __init__(self, parent: QMainWindow, title=None, titlebar=True):
        self.__parent = parent
        super().__init__(parent)
        self.setupUi(self)
        if title is not None:
            self.setWindowTitle(title)
        if not titlebar:
            self.setWindowFlags(Qt.Window | Qt.CustomizeWindowHint)
        self.signal_slot_connection()
        self.__pressed = False
        self.__linkage = Linkage.NoLink
        self.__x = self.x()
        self.__y = self.y()
        self.__w = self.width()
        self.__h = self.height()
        self.installEventFilter(self)
        self.__not_shown_yet = True

    def not_shown_yet(self):
        return self.__not_shown_yet

    @property
    def linkage(self):
        return self.__linkage

    @linkage.setter
    def linkage(self, side: Linkage):
        assert isinstance(side, Linkage)
        self.__linkage = side

    def signal_slot_connection(self):
        self.uiPushButton_close_window.clicked.connect(self.hide)
        self.signal_append_line.connect(
            self.uiPlainTextEdit_output.appendPlainText
        )
        self.uiPushButton_clear_content.clicked.connect(
            self.uiPlainTextEdit_output.clear
        )
        self.signal_clear_content.connect(self.uiPlainTextEdit_output.clear)

    def showEvent(self, event: QShowEvent):
        self.__not_shown_yet = False

    def __test_geo(self):
        cur, curf = self.geometry(), self.frameGeometry()
        par, parf = self.__parent.geometry(), self.__parent.frameGeometry()
        if parf.bottom() - 20 <= curf.top() <= parf.bottom() + 20:
            if parf.left() - 20 <= curf.left() <= parf.left() + 20:
                self.__x = parf.left()
                self.__y = parf.bottom() + 1
                self.__w = par.width()
                self.__h = cur.height()
                self.__linkage = Linkage.Top
                return True
        elif parf.top() - 20 < curf.top() < parf.top() + 20:
            if parf.right() - 20 <= curf.left() <= parf.right() + 20:
                self.__x = parf.right() + 1
                self.__y = parf.top()
                self.__w = cur.width()
                self.__h = par.height()
                self.__linkage = Linkage.Left
                return True
            elif parf.left() - 20 <= curf.right() <= parf.left() + 20:
                self.__x = parf.left() - curf.width()
                self.__y = parf.top()
                self.__w = cur.width()
                self.__h = par.height()
                self.__linkage = Linkage.Right
                return True
        self.__linkage = Linkage.NoLink
        return False

    def __make_adsorb(self):
        if not self.__pressed:
            return
        if not self.__test_geo():
            return
        self.move(self.__x, self.__y)
        self.resize(self.__w, self.__h)

    def moveEvent(self, event: QMoveEvent):
        cur_point = event.pos()
        self.__x = cur_point.x()
        self.__y = cur_point.y()

    def resizeEvent(self, event: QResizeEvent):
        cur_size = event.size()
        self.__w = cur_size.width()
        self.__h = cur_size.height()

    def eventFilter(self, sender: QObject, event: QEvent) -> bool:
        if sender == self:
            if event.type() == QEvent.NonClientAreaMouseButtonPress:
                self.__pressed = True
            elif event.type() == QEvent.NonClientAreaMouseButtonRelease:
                self.__pressed = False
            elif event.type() == QEvent.Move or event.type() == QEvent.Resize:
                self.__make_adsorb()
        return super().eventFilter(sender, event)

    def closeEvent(self, event: QCloseEvent):
        self.hide()
        event.ignore()

    def set_geometry(self, point: QPoint, w, h):
        if self.__linkage == Linkage.Left:
            self.__x = point.x() + 1
            self.__y = point.y()
        elif self.__linkage == Linkage.Right:
            self.__x = point.x() - self.frameGeometry().width()
            self.__y = point.y()
        elif self.__linkage == Linkage.Top:
            self.__x = point.x()
            self.__y = point.y() + 1
        else:
            return
        if w is not None:
            self.__w = w
        if h is not None:
            self.__h = h
        self.move(self.__x, self.__y)
        self.resize(self.__w, self.__h)

    def clear_content(self):
        self.signal_clear_content.emit()

    def add_line(self, string):
        self.signal_append_line.emit(string)

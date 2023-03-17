# coding: utf-8

from PyQt5.QtWidgets import *


class MessageBox(QMessageBox):
    """
    点击按钮后返回该按钮在参数中的次序值

    多按钮：关闭窗口返回值跟随'reject'按钮次序值

    只有一个按钮：直接关闭窗口返回 0

    多按钮的情况下，'reject'按钮在最右侧

    有'destructive'按钮，无'reject'按钮，窗口不可关闭
    """

    def __init__(
        self,
        title,
        message,
        icon=None,
        buttons=(("accept", "确定"),),
        parent=None,
    ):
        if icon is None:
            icon = QMessageBox.Information
        super().__init__(icon, title, message, parent=parent)
        self._buttons = buttons
        self.__set_push_buttons()

    def __set_push_buttons(self):
        for btn in self._buttons:
            role, text = btn
            if role == "accept":
                self.addButton(text, QMessageBox.AcceptRole)
            elif role == "destructive":
                self.addButton(text, QMessageBox.DestructiveRole)
            elif role == "reject":
                self.setDefaultButton(
                    self.addButton(text, QMessageBox.RejectRole)
                )

    def get_role(self):
        return self.exec_()

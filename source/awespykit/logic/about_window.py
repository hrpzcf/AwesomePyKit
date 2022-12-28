# coding: utf-8

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui import *

from logic.messagebox import MessageBox


class AboutWindow(Ui_about_window, QMainWindow):
    def __init__(self, parent, appversion: str):
        self.__parent = parent
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.__v = appversion
        self.uiLabel_app_version.installEventFilter(self)
        self.uiLabel_app_version.setText(f"Awespykit - {self.__v}")
        self.uiLabel_license.installEventFilter(self)
        self.uiLabel_issue_github.installEventFilter(self)
        self.uiLabel_issue_gitee.installEventFilter(self)
        self.uiLabel_source_github.installEventFilter(self)
        self.uiLabel_source_gitee.installEventFilter(self)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.MouseButtonRelease:
            hyperlink = None
            if obj == self.uiLabel_app_version:
                hyperlink = "https://gitee.com/hrpzcf/AwesomePyKit/releases"
            elif obj == self.uiLabel_issue_gitee:
                hyperlink = "https://gitee.com/hrpzcf/AwesomePyKit/issues"
            elif obj == self.uiLabel_issue_github:
                hyperlink = "https://github.com/hrpzcf/AwesomePyKit/issues"
            elif obj == self.uiLabel_source_gitee:
                hyperlink = "https://gitee.com/hrpzcf/AwesomePyKit"
            elif obj == self.uiLabel_source_github:
                hyperlink = "https://github.com/hrpzcf/AwesomePyKit"
            elif obj == self.uiLabel_license:
                hyperlink = (
                    "https://gitee.com/hrpzcf/AwesomePyKit/blob/main/LICENSE"
                )
            if hyperlink is not None and not QDesktopServices.openUrl(
                QUrl(hyperlink)
            ):
                MessageBox("提示", "链接打开失败！", QMessageBox.Warning).exec_()
        return super(AboutWindow, self).eventFilter(obj, event)

    def display(self):
        self.showNormal()

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'addenv_dialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_input_dialog(object):
    def setupUi(self, input_dialog):
        if not input_dialog.objectName():
            input_dialog.setObjectName(u"input_dialog")
        input_dialog.setWindowModality(Qt.WindowModal)
        input_dialog.resize(580, 74)
        font = QFont()
        font.setFamily(u"Microsoft YaHei UI")
        input_dialog.setFont(font)
        self.centralwidget = QWidget(input_dialog)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 16, 8, 8)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.uiLineEdit_input_content = QLineEdit(self.centralwidget)
        self.uiLineEdit_input_content.setObjectName(u"uiLineEdit_input_content")

        self.horizontalLayout.addWidget(self.uiLineEdit_input_content)

        self.uiPushButton_select_envdir = QPushButton(self.centralwidget)
        self.uiPushButton_select_envdir.setObjectName(u"uiPushButton_select_envdir")

        self.horizontalLayout.addWidget(self.uiPushButton_select_envdir)

        self.uiPushButton_confirm = QPushButton(self.centralwidget)
        self.uiPushButton_confirm.setObjectName(u"uiPushButton_confirm")

        self.horizontalLayout.addWidget(self.uiPushButton_confirm)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        palette = QPalette()
        brush = QBrush(QColor(100, 100, 100, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        self.label.setPalette(palette)
        font1 = QFont()
        font1.setFamily(u"Microsoft YaHei UI")
        font1.setPointSize(9)
        self.label.setFont(font1)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.verticalLayout.setStretch(1, 1)
        input_dialog.setCentralWidget(self.centralwidget)

        self.retranslateUi(input_dialog)

        QMetaObject.connectSlotsByName(input_dialog)
    # setupUi

    def retranslateUi(self, input_dialog):
        input_dialog.setWindowTitle(QCoreApplication.translate("input_dialog", u"\u8f93\u5165\u5185\u5bb9", None))
#if QT_CONFIG(tooltip)
        self.uiPushButton_select_envdir.setToolTip(QCoreApplication.translate("input_dialog", u"\u6253\u5f00\u76ee\u5f55\u9009\u62e9\u7a97\u53e3\uff0c\u9009\u62e9 python.exe \u6587\u4ef6\u6240\u5728\u7684\u76ee\u5f55\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.uiPushButton_select_envdir.setText(QCoreApplication.translate("input_dialog", u"\u9009\u62e9", None))
        self.uiPushButton_confirm.setText(QCoreApplication.translate("input_dialog", u"\u786e\u5b9a", None))
        self.label.setText(QCoreApplication.translate("input_dialog", u"\u7c98\u8d34 \u201cpython.exe\u201d \u6587\u4ef6\u6240\u5728\u76ee\u5f55\u8def\u5f84\u6216\u70b9\u51fb\u201c\u9009\u62e9\u201d\u6309\u94ae\u9009\u62e9 \u201cpython.exe\u201d \u6587\u4ef6\u6240\u5728\u76ee\u5f55\u7136\u540e\u70b9\u51fb\u786e\u5b9a\u3002", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'generic_output.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_generic_output(object):
    def setupUi(self, generic_output):
        if not generic_output.objectName():
            generic_output.setObjectName("generic_output")
        generic_output.resize(350, 500)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        generic_output.setFont(font)
        self.action123 = QAction(generic_output)
        self.action123.setObjectName("action123")
        self.action123.setFont(font)
        self.uiAction_bg_white = QAction(generic_output)
        self.uiAction_bg_white.setObjectName("uiAction_bg_white")
        self.uiAction_bg_black = QAction(generic_output)
        self.uiAction_bg_black.setObjectName("uiAction_bg_black")
        self.centralwidget = QWidget(generic_output)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.uiPlainTextEdit_output = QPlainTextEdit(self.centralwidget)
        self.uiPlainTextEdit_output.setObjectName("uiPlainTextEdit_output")
        font1 = QFont()
        font1.setFamily("Consolas")
        font1.setPointSize(10)
        self.uiPlainTextEdit_output.setFont(font1)
        self.uiPlainTextEdit_output.setReadOnly(True)

        self.verticalLayout.addWidget(self.uiPlainTextEdit_output)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.uiPushButton_close_window = QPushButton(self.centralwidget)
        self.uiPushButton_close_window.setObjectName("uiPushButton_close_window")

        self.horizontalLayout.addWidget(self.uiPushButton_close_window)

        self.uiPushButton_clear_content = QPushButton(self.centralwidget)
        self.uiPushButton_clear_content.setObjectName("uiPushButton_clear_content")

        self.horizontalLayout.addWidget(self.uiPushButton_clear_content)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout.setStretch(0, 1)
        generic_output.setCentralWidget(self.centralwidget)

        self.retranslateUi(generic_output)

        QMetaObject.connectSlotsByName(generic_output)

    # setupUi

    def retranslateUi(self, generic_output):
        generic_output.setWindowTitle(
            QCoreApplication.translate(
                "generic_output", "\u63a7\u5236\u53f0\u8f93\u51fa\u5185\u5bb9", None
            )
        )
        self.action123.setText(
            QCoreApplication.translate(
                "generic_output", "\u5b57\u4f53\u989c\u8272", None
            )
        )
        self.uiAction_bg_white.setText(
            QCoreApplication.translate("generic_output", "\u767d\u8272", None)
        )
        self.uiAction_bg_black.setText(
            QCoreApplication.translate("generic_output", "\u9ed1\u8272", None)
        )
        self.uiPlainTextEdit_output.setPlainText("")
        self.uiPushButton_close_window.setText(
            QCoreApplication.translate(
                "generic_output", "\u5173\u95ed\u7a97\u53e3", None
            )
        )
        self.uiPushButton_clear_content.setText(
            QCoreApplication.translate(
                "generic_output", "\u6e05\u7a7a\u5185\u5bb9", None
            )
        )

    # retranslateUi

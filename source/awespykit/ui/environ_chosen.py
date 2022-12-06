# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'environ_chosen.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_environ_chosen(object):
    def setupUi(self, environ_chosen):
        if not environ_chosen.objectName():
            environ_chosen.setObjectName("environ_chosen")
        environ_chosen.setWindowModality(Qt.WindowModal)
        environ_chosen.resize(420, 200)
        environ_chosen.setContextMenuPolicy(Qt.NoContextMenu)
        self.centralwidget = QWidget(environ_chosen)
        self.centralwidget.setObjectName("centralwidget")
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        self.centralwidget.setFont(font)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.lw_environ_list = QListWidget(self.centralwidget)
        self.lw_environ_list.setObjectName("lw_environ_list")

        self.verticalLayout.addWidget(self.lw_environ_list)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        palette = QPalette()
        brush = QBrush(QColor(91, 91, 91, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        self.label.setPalette(palette)
        font1 = QFont()
        font1.setFamily("Microsoft YaHei UI")
        font1.setPointSize(9)
        self.label.setFont(font1)

        self.verticalLayout.addWidget(self.label)

        environ_chosen.setCentralWidget(self.centralwidget)

        self.retranslateUi(environ_chosen)

        QMetaObject.connectSlotsByName(environ_chosen)

    # setupUi

    def retranslateUi(self, environ_chosen):
        environ_chosen.setWindowTitle(
            QCoreApplication.translate(
                "environ_chosen", "\u9009\u62e9 Python \u73af\u5883", None
            )
        )
        self.label.setText(
            QCoreApplication.translate(
                "environ_chosen",
                "\u9700\u8981\u5148\u5728\u5305\u7ba1\u7406\u5668\u4e2d\u6dfb\u52a0\u73af\u5883\uff0c\u8fd9\u91cc\u624d\u4f1a\u663e\u793a\u53ef\u4f9b\u9009\u62e9\u7684\u9879~",
                None,
            )
        )

    # retranslateUi

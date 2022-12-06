# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'index_manager.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_index_manager(object):
    def setupUi(self, index_manager):
        if not index_manager.objectName():
            index_manager.setObjectName("index_manager")
        index_manager.setWindowModality(Qt.WindowModal)
        index_manager.resize(480, 520)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        index_manager.setFont(font)
        self.centralwidget = QWidget(index_manager)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.li_indexurls = QListWidget(self.centralwidget)
        self.li_indexurls.setObjectName("li_indexurls")
        palette = QPalette()
        brush = QBrush(QColor(155, 222, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush)
        brush1 = QBrush(QColor(190, 190, 190, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush1)
        self.li_indexurls.setPalette(palette)

        self.verticalLayout_4.addWidget(self.li_indexurls)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.btn_delurl = QPushButton(self.centralwidget)
        self.btn_delurl.setObjectName("btn_delurl")

        self.horizontalLayout_4.addWidget(self.btn_delurl)

        self.horizontalLayout_4.setStretch(0, 9)
        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")

        self.verticalLayout.addWidget(self.label)

        self.le_urlname = QLineEdit(self.centralwidget)
        self.le_urlname.setObjectName("le_urlname")

        self.verticalLayout.addWidget(self.le_urlname)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.le_indexurl = QLineEdit(self.centralwidget)
        self.le_indexurl.setObjectName("le_indexurl")

        self.verticalLayout_2.addWidget(self.le_indexurl)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 9)

        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.btn_clearle = QPushButton(self.centralwidget)
        self.btn_clearle.setObjectName("btn_clearle")

        self.horizontalLayout.addWidget(self.btn_clearle)

        self.btn_saveurl = QPushButton(self.centralwidget)
        self.btn_saveurl.setObjectName("btn_saveurl")

        self.horizontalLayout.addWidget(self.btn_saveurl)

        self.btn_setindex = QPushButton(self.centralwidget)
        self.btn_setindex.setObjectName("btn_setindex")
        palette1 = QPalette()
        brush2 = QBrush(QColor(0, 0, 255, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush2)
        brush3 = QBrush(QColor(120, 120, 120, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush3)
        self.btn_setindex.setPalette(palette1)

        self.horizontalLayout.addWidget(self.btn_setindex)

        self.horizontalLayout.setStretch(0, 9)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(3, 2)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.btn_refresh_effective = QPushButton(self.centralwidget)
        self.btn_refresh_effective.setObjectName("btn_refresh_effective")

        self.horizontalLayout_3.addWidget(self.btn_refresh_effective)

        self.horizontalLayout_3.setStretch(0, 9)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.le_effectiveurl = QLineEdit(self.centralwidget)
        self.le_effectiveurl.setObjectName("le_effectiveurl")
        self.le_effectiveurl.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.le_effectiveurl)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.verticalLayout_4.setStretch(0, 9)
        self.verticalLayout_4.setStretch(1, 1)
        self.verticalLayout_4.setStretch(2, 1)
        self.verticalLayout_4.setStretch(3, 1)
        self.verticalLayout_4.setStretch(4, 1)
        self.verticalLayout_4.setStretch(5, 1)
        self.verticalLayout_4.setStretch(6, 1)

        self.verticalLayout_5.addLayout(self.verticalLayout_4)

        index_manager.setCentralWidget(self.centralwidget)

        self.retranslateUi(index_manager)

        QMetaObject.connectSlotsByName(index_manager)

    # setupUi

    def retranslateUi(self, index_manager):
        index_manager.setWindowTitle(
            QCoreApplication.translate(
                "index_manager", "\u955c\u50cf\u6e90\u8bbe\u7f6e", None
            )
        )
        self.label_4.setText("")
        # if QT_CONFIG(tooltip)
        self.btn_delurl.setToolTip(
            QCoreApplication.translate(
                "index_manager",
                "\u5220\u9664\u5217\u8868\u4e2d\u9009\u4e2d\u7684\u955c\u50cf\u6e90\u5730\u5740\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_delurl.setText(
            QCoreApplication.translate("index_manager", "\u5220\u9664", None)
        )
        self.label.setText(
            QCoreApplication.translate(
                "index_manager", "\u7f16\u8f91\u540d\u79f0\uff1a", None
            )
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "index_manager", "\u7f16\u8f91\u5730\u5740\uff1a", None
            )
        )
        self.label_5.setText("")
        # if QT_CONFIG(tooltip)
        self.btn_clearle.setToolTip(
            QCoreApplication.translate(
                "index_manager",
                "\u6e05\u7a7a\u6b63\u5728\u7f16\u8f91\u7684\u540d\u79f0\u548c\u5730\u5740\u8f93\u5165\u6846\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_clearle.setText(
            QCoreApplication.translate(
                "index_manager", "\u6e05\u7a7a\u7f16\u8f91", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.btn_saveurl.setToolTip(
            QCoreApplication.translate(
                "index_manager",
                "\u5c06\u8f93\u5165\u6846\u5185\u7684\u540d\u79f0\u548c\u5730\u5740\u4fdd\u5b58\u5230\u5217\u8868\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_saveurl.setText(
            QCoreApplication.translate(
                "index_manager", "\u4fdd\u5b58\u81f3\u5217\u8868", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.btn_setindex.setToolTip(
            QCoreApplication.translate(
                "index_manager",
                "\u5c06\u8f93\u5165\u6846\u5185\u7684\u955c\u50cf\u6e90\u5730\u5740\u8bbe\u7f6e\u4e3a\u5168\u5c40\u955c\u50cf\u6e90\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_setindex.setText(
            QCoreApplication.translate(
                "index_manager", "\u542f\u7528\u955c\u50cf\u6e90", None
            )
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "index_manager",
                "\u5f53\u524d\u751f\u6548\u7684\u5168\u5c40\u955c\u50cf\u6e90\u5730\u5740\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.btn_refresh_effective.setToolTip(
            QCoreApplication.translate(
                "index_manager",
                "\u83b7\u53d6\u5f53\u524d\u751f\u6548\u7684\u5168\u5c40\u955c\u50cf\u6e90\u5730\u5740\u5e76\u663e\u793a\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_refresh_effective.setText(
            QCoreApplication.translate("index_manager", "\u5237\u65b0", None)
        )

    # retranslateUi

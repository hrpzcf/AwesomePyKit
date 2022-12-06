# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'show_download.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_show_download(object):
    def setupUi(self, show_download):
        if not show_download.objectName():
            show_download.setObjectName("show_download")
        show_download.setWindowModality(Qt.WindowModal)
        show_download.resize(260, 500)
        self.centralwidget = QWidget(show_download)
        self.centralwidget.setObjectName("centralwidget")
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        self.centralwidget.setFont(font)
        self.centralwidget.setContextMenuPolicy(Qt.NoContextMenu)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.tw_downloading = QTableWidget(self.centralwidget)
        if self.tw_downloading.columnCount() < 2:
            self.tw_downloading.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tw_downloading.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tw_downloading.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tw_downloading.setObjectName("tw_downloading")
        self.tw_downloading.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_downloading.setSelectionMode(QAbstractItemView.NoSelection)
        self.tw_downloading.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_downloading.setCornerButtonEnabled(False)
        self.tw_downloading.horizontalHeader().setHighlightSections(False)
        self.tw_downloading.horizontalHeader().setStretchLastSection(True)
        self.tw_downloading.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.tw_downloading)

        show_download.setCentralWidget(self.centralwidget)

        self.retranslateUi(show_download)

        QMetaObject.connectSlotsByName(show_download)

    # setupUi

    def retranslateUi(self, show_download):
        show_download.setWindowTitle(
            QCoreApplication.translate(
                "show_download", "\u4e0b\u8f7d\u5217\u8868", None
            )
        )
        ___qtablewidgetitem = self.tw_downloading.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("show_download", "\u4e0b\u8f7d\u9879", None)
        )
        ___qtablewidgetitem1 = self.tw_downloading.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate(
                "show_download", "\u4e0b\u8f7d\u72b6\u6001", None
            )
        )

    # retranslateUi

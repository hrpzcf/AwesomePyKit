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
            show_download.setObjectName(u"show_download")
        show_download.setWindowModality(Qt.WindowModal)
        show_download.resize(260, 500)
        self.centralwidget = QWidget(show_download)
        self.centralwidget.setObjectName(u"centralwidget")
        font = QFont()
        font.setFamily(u"Microsoft YaHei UI")
        self.centralwidget.setFont(font)
        self.centralwidget.setContextMenuPolicy(Qt.NoContextMenu)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.uiTableWidget_downloading = QTableWidget(self.centralwidget)
        if (self.uiTableWidget_downloading.columnCount() < 2):
            self.uiTableWidget_downloading.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.uiTableWidget_downloading.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.uiTableWidget_downloading.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.uiTableWidget_downloading.setObjectName(u"uiTableWidget_downloading")
        self.uiTableWidget_downloading.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.uiTableWidget_downloading.setSelectionMode(QAbstractItemView.NoSelection)
        self.uiTableWidget_downloading.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.uiTableWidget_downloading.setCornerButtonEnabled(False)
        self.uiTableWidget_downloading.horizontalHeader().setHighlightSections(False)
        self.uiTableWidget_downloading.horizontalHeader().setStretchLastSection(True)
        self.uiTableWidget_downloading.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.uiTableWidget_downloading)

        show_download.setCentralWidget(self.centralwidget)

        self.retranslateUi(show_download)

        QMetaObject.connectSlotsByName(show_download)
    # setupUi

    def retranslateUi(self, show_download):
        show_download.setWindowTitle(QCoreApplication.translate("show_download", u"\u4e0b\u8f7d\u5217\u8868", None))
        ___qtablewidgetitem = self.uiTableWidget_downloading.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("show_download", u"\u4e0b\u8f7d\u9879", None));
        ___qtablewidgetitem1 = self.uiTableWidget_downloading.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("show_download", u"\u4e0b\u8f7d\u72b6\u6001", None));
    # retranslateUi


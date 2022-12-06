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
            index_manager.setObjectName(u"index_manager")
        index_manager.setWindowModality(Qt.WindowModal)
        index_manager.resize(480, 520)
        font = QFont()
        font.setFamily(u"Microsoft YaHei UI")
        index_manager.setFont(font)
        self.centralwidget = QWidget(index_manager)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.uiListWidget_indexurls = QListWidget(self.centralwidget)
        self.uiListWidget_indexurls.setObjectName(u"uiListWidget_indexurls")
        palette = QPalette()
        brush = QBrush(QColor(155, 222, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush)
        brush1 = QBrush(QColor(190, 190, 190, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush1)
        self.uiListWidget_indexurls.setPalette(palette)

        self.verticalLayout_4.addWidget(self.uiListWidget_indexurls)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_4.addWidget(self.label_4)

        self.uiPushButton_delete_url = QPushButton(self.centralwidget)
        self.uiPushButton_delete_url.setObjectName(u"uiPushButton_delete_url")

        self.horizontalLayout_4.addWidget(self.uiPushButton_delete_url)

        self.horizontalLayout_4.setStretch(0, 9)
        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_4)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.uiLineEdit_url_name = QLineEdit(self.centralwidget)
        self.uiLineEdit_url_name.setObjectName(u"uiLineEdit_url_name")

        self.verticalLayout.addWidget(self.uiLineEdit_url_name)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_2.addWidget(self.label_2)

        self.uiLineEdit_index_url = QLineEdit(self.centralwidget)
        self.uiLineEdit_index_url.setObjectName(u"uiLineEdit_index_url")

        self.verticalLayout_2.addWidget(self.uiLineEdit_index_url)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.horizontalLayout_2.setStretch(0, 2)
        self.horizontalLayout_2.setStretch(1, 9)

        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.uiPushButton_clear_edit = QPushButton(self.centralwidget)
        self.uiPushButton_clear_edit.setObjectName(u"uiPushButton_clear_edit")

        self.horizontalLayout.addWidget(self.uiPushButton_clear_edit)

        self.uiPushButton_save_url = QPushButton(self.centralwidget)
        self.uiPushButton_save_url.setObjectName(u"uiPushButton_save_url")

        self.horizontalLayout.addWidget(self.uiPushButton_save_url)

        self.uiPushButton_set_index = QPushButton(self.centralwidget)
        self.uiPushButton_set_index.setObjectName(u"uiPushButton_set_index")
        palette1 = QPalette()
        brush2 = QBrush(QColor(0, 0, 255, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush2)
        brush3 = QBrush(QColor(120, 120, 120, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush3)
        self.uiPushButton_set_index.setPalette(palette1)

        self.horizontalLayout.addWidget(self.uiPushButton_set_index)

        self.horizontalLayout.setStretch(0, 9)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 2)
        self.horizontalLayout.setStretch(3, 2)

        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.uiPushButton_refresh_effective = QPushButton(self.centralwidget)
        self.uiPushButton_refresh_effective.setObjectName(u"uiPushButton_refresh_effective")

        self.horizontalLayout_3.addWidget(self.uiPushButton_refresh_effective)

        self.horizontalLayout_3.setStretch(0, 9)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.uiLineEdit_effective_url = QLineEdit(self.centralwidget)
        self.uiLineEdit_effective_url.setObjectName(u"uiLineEdit_effective_url")
        self.uiLineEdit_effective_url.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.uiLineEdit_effective_url)


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
        index_manager.setWindowTitle(QCoreApplication.translate("index_manager", u"\u955c\u50cf\u6e90\u8bbe\u7f6e", None))
        self.label_4.setText("")
#if QT_CONFIG(tooltip)
        self.uiPushButton_delete_url.setToolTip(QCoreApplication.translate("index_manager", u"\u5220\u9664\u5217\u8868\u4e2d\u9009\u4e2d\u7684\u955c\u50cf\u6e90\u5730\u5740\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.uiPushButton_delete_url.setText(QCoreApplication.translate("index_manager", u"\u5220\u9664", None))
        self.label.setText(QCoreApplication.translate("index_manager", u"\u7f16\u8f91\u540d\u79f0\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("index_manager", u"\u7f16\u8f91\u5730\u5740\uff1a", None))
        self.label_5.setText("")
#if QT_CONFIG(tooltip)
        self.uiPushButton_clear_edit.setToolTip(QCoreApplication.translate("index_manager", u"\u6e05\u7a7a\u6b63\u5728\u7f16\u8f91\u7684\u540d\u79f0\u548c\u5730\u5740\u8f93\u5165\u6846\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.uiPushButton_clear_edit.setText(QCoreApplication.translate("index_manager", u"\u6e05\u7a7a\u7f16\u8f91", None))
#if QT_CONFIG(tooltip)
        self.uiPushButton_save_url.setToolTip(QCoreApplication.translate("index_manager", u"\u5c06\u8f93\u5165\u6846\u5185\u7684\u540d\u79f0\u548c\u5730\u5740\u4fdd\u5b58\u5230\u5217\u8868\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.uiPushButton_save_url.setText(QCoreApplication.translate("index_manager", u"\u4fdd\u5b58\u81f3\u5217\u8868", None))
#if QT_CONFIG(tooltip)
        self.uiPushButton_set_index.setToolTip(QCoreApplication.translate("index_manager", u"\u5c06\u8f93\u5165\u6846\u5185\u7684\u955c\u50cf\u6e90\u5730\u5740\u8bbe\u7f6e\u4e3a\u5168\u5c40\u955c\u50cf\u6e90\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.uiPushButton_set_index.setText(QCoreApplication.translate("index_manager", u"\u542f\u7528\u955c\u50cf\u6e90", None))
        self.label_3.setText(QCoreApplication.translate("index_manager", u"\u5f53\u524d\u751f\u6548\u7684\u5168\u5c40\u955c\u50cf\u6e90\u5730\u5740\uff1a", None))
#if QT_CONFIG(tooltip)
        self.uiPushButton_refresh_effective.setToolTip(QCoreApplication.translate("index_manager", u"\u83b7\u53d6\u5f53\u524d\u751f\u6548\u7684\u5168\u5c40\u955c\u50cf\u6e90\u5730\u5740\u5e76\u663e\u793a\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.uiPushButton_refresh_effective.setText(QCoreApplication.translate("index_manager", u"\u5237\u65b0", None))
    # retranslateUi


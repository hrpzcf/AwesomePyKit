# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'query_panel.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_query_panel(object):
    def setupUi(self, query_panel):
        if not query_panel.objectName():
            query_panel.setObjectName(u"query_panel")
        query_panel.setWindowModality(Qt.WindowModal)
        query_panel.resize(330, 330)
        font = QFont()
        font.setFamily(u"Microsoft YaHei UI")
        query_panel.setFont(font)
        self.centralwidget = QWidget(query_panel)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.uiLineEdit_input_name = QLineEdit(self.centralwidget)
        self.uiLineEdit_input_name.setObjectName(u"uiLineEdit_input_name")

        self.horizontalLayout.addWidget(self.uiLineEdit_input_name)

        self.uiPushButton_query = QPushButton(self.centralwidget)
        self.uiPushButton_query.setObjectName(u"uiPushButton_query")

        self.horizontalLayout.addWidget(self.uiPushButton_query)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.uiRadioButton_pkg2import = QRadioButton(self.centralwidget)
        self.uiRadioButton_pkg2import.setObjectName(u"uiRadioButton_pkg2import")
        self.uiRadioButton_pkg2import.setChecked(True)

        self.horizontalLayout_2.addWidget(self.uiRadioButton_pkg2import)

        self.uiRadioButton_import2pkg = QRadioButton(self.centralwidget)
        self.uiRadioButton_import2pkg.setObjectName(u"uiRadioButton_import2pkg")

        self.horizontalLayout_2.addWidget(self.uiRadioButton_import2pkg)

        self.uiCheckBox_case_sensitive = QCheckBox(self.centralwidget)
        self.uiCheckBox_case_sensitive.setObjectName(u"uiCheckBox_case_sensitive")

        self.horizontalLayout_2.addWidget(self.uiCheckBox_case_sensitive)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.uiLabel_query_environ = QLabel(self.centralwidget)
        self.uiLabel_query_environ.setObjectName(u"uiLabel_query_environ")
        self.uiLabel_query_environ.setFrameShape(QFrame.Box)

        self.verticalLayout_2.addWidget(self.uiLabel_query_environ)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.uiLabel_query_result = QLabel(self.centralwidget)
        self.uiLabel_query_result.setObjectName(u"uiLabel_query_result")

        self.verticalLayout.addWidget(self.uiLabel_query_result)

        self.uiPlainTextEdit_query_result = QPlainTextEdit(self.centralwidget)
        self.uiPlainTextEdit_query_result.setObjectName(u"uiPlainTextEdit_query_result")

        self.verticalLayout.addWidget(self.uiPlainTextEdit_query_result)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        query_panel.setCentralWidget(self.centralwidget)

        self.retranslateUi(query_panel)

        QMetaObject.connectSlotsByName(query_panel)
    # setupUi

    def retranslateUi(self, query_panel):
        query_panel.setWindowTitle(QCoreApplication.translate("query_panel", u"\u67e5\u8be2\u9762\u677f", None))
        self.uiPushButton_query.setText(QCoreApplication.translate("query_panel", u"\u67e5\u8be2", None))
        self.uiRadioButton_pkg2import.setText(QCoreApplication.translate("query_panel", u"\u4ee5\u5305\u540d\u67e5\u5bfc\u5165\u540d", None))
        self.uiRadioButton_import2pkg.setText(QCoreApplication.translate("query_panel", u"\u4ee5\u5bfc\u5165\u540d\u67e5\u5305\u540d", None))
        self.uiCheckBox_case_sensitive.setText(QCoreApplication.translate("query_panel", u"\u533a\u5206\u5927\u5c0f\u5199", None))
        self.label.setText(QCoreApplication.translate("query_panel", u"\u67e5\u8be2\u73af\u5883\uff1a", None))
        self.uiLabel_query_environ.setText(QCoreApplication.translate("query_panel", u"\u672a\u8bbe\u7f6e\u4efb\u4f55\u73af\u5883\uff01", None))
        self.uiLabel_query_result.setText(QCoreApplication.translate("query_panel", u"\u67e5\u8be2\u7ed3\u679c\uff1a", None))
    # retranslateUi


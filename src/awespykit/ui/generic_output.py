# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'generic_output.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_generic_output(object):
    def setupUi(self, generic_output):
        generic_output.setObjectName("generic_output")
        generic_output.resize(350, 500)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        generic_output.setFont(font)
        self.centralwidget = QtWidgets.QWidget(generic_output)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(4, 4, 4, 4)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.uiPlainTextEdit_output = QtWidgets.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(10)
        self.uiPlainTextEdit_output.setFont(font)
        self.uiPlainTextEdit_output.setReadOnly(True)
        self.uiPlainTextEdit_output.setPlainText("")
        self.uiPlainTextEdit_output.setObjectName("uiPlainTextEdit_output")
        self.verticalLayout.addWidget(self.uiPlainTextEdit_output)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.uiPushButton_close_window = QtWidgets.QPushButton(self.centralwidget)
        self.uiPushButton_close_window.setObjectName("uiPushButton_close_window")
        self.horizontalLayout.addWidget(self.uiPushButton_close_window)
        self.uiPushButton_clear_content = QtWidgets.QPushButton(self.centralwidget)
        self.uiPushButton_clear_content.setObjectName("uiPushButton_clear_content")
        self.horizontalLayout.addWidget(self.uiPushButton_clear_content)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        generic_output.setCentralWidget(self.centralwidget)
        self.action123 = QtWidgets.QAction(generic_output)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        self.action123.setFont(font)
        self.action123.setObjectName("action123")
        self.uiAction_bg_white = QtWidgets.QAction(generic_output)
        self.uiAction_bg_white.setObjectName("uiAction_bg_white")
        self.uiAction_bg_black = QtWidgets.QAction(generic_output)
        self.uiAction_bg_black.setObjectName("uiAction_bg_black")

        self.retranslateUi(generic_output)
        QtCore.QMetaObject.connectSlotsByName(generic_output)

    def retranslateUi(self, generic_output):
        _translate = QtCore.QCoreApplication.translate
        generic_output.setWindowTitle(_translate("generic_output", "控制台输出内容"))
        self.uiPushButton_close_window.setText(_translate("generic_output", "关闭窗口"))
        self.uiPushButton_clear_content.setText(_translate("generic_output", "清空内容"))
        self.action123.setText(_translate("generic_output", "字体颜色"))
        self.uiAction_bg_white.setText(_translate("generic_output", "白色"))
        self.uiAction_bg_black.setText(_translate("generic_output", "黑色"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_entrance.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_main_entrance(object):
    def setupUi(self, main_entrance):
        main_entrance.setObjectName("main_entrance")
        main_entrance.resize(260, 320)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(10)
        main_entrance.setFont(font)
        self.centralwidget = QtWidgets.QWidget(main_entrance)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pb_pkg_mgr = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_pkg_mgr.sizePolicy().hasHeightForWidth())
        self.pb_pkg_mgr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.pb_pkg_mgr.setFont(font)
        self.pb_pkg_mgr.setObjectName("pb_pkg_mgr")
        self.verticalLayout.addWidget(self.pb_pkg_mgr)
        self.pb_pyi_tool = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_pyi_tool.sizePolicy().hasHeightForWidth())
        self.pb_pyi_tool.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.pb_pyi_tool.setFont(font)
        self.pb_pyi_tool.setObjectName("pb_pyi_tool")
        self.verticalLayout.addWidget(self.pb_pyi_tool)
        self.pb_index_mgr = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_index_mgr.sizePolicy().hasHeightForWidth())
        self.pb_index_mgr.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.pb_index_mgr.setFont(font)
        self.pb_index_mgr.setObjectName("pb_index_mgr")
        self.verticalLayout.addWidget(self.pb_index_mgr)
        self.pb_pkg_dload = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pb_pkg_dload.sizePolicy().hasHeightForWidth())
        self.pb_pkg_dload.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei UI")
        font.setPointSize(11)
        self.pb_pkg_dload.setFont(font)
        self.pb_pkg_dload.setObjectName("pb_pkg_dload")
        self.verticalLayout.addWidget(self.pb_pkg_dload)
        main_entrance.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_entrance)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 260, 25))
        self.menubar.setObjectName("menubar")
        self.menu_help = QtWidgets.QMenu(self.menubar)
        self.menu_help.setObjectName("menu_help")
        self.menu_settings = QtWidgets.QMenu(self.menubar)
        self.menu_settings.setObjectName("menu_settings")
        self.menu_style = QtWidgets.QMenu(self.menu_settings)
        self.menu_style.setObjectName("menu_style")
        main_entrance.setMenuBar(self.menubar)
        self.description = QtWidgets.QAction(main_entrance)
        font = QtGui.QFont()
        self.description.setFont(font)
        self.description.setObjectName("description")
        self.action_about = QtWidgets.QAction(main_entrance)
        font = QtGui.QFont()
        self.action_about.setFont(font)
        self.action_about.setObjectName("action_about")
        self.contribution = QtWidgets.QAction(main_entrance)
        self.contribution.setObjectName("contribution")
        self.action_fusion = QtWidgets.QAction(main_entrance)
        self.action_fusion.setCheckable(True)
        self.action_fusion.setObjectName("action_fusion")
        self.action_windows = QtWidgets.QAction(main_entrance)
        self.action_windows.setCheckable(True)
        self.action_windows.setObjectName("action_windows")
        self.action_default = QtWidgets.QAction(main_entrance)
        self.action_default.setCheckable(True)
        self.action_default.setObjectName("action_default")
        self.menu_help.addAction(self.action_about)
        self.menu_style.addAction(self.action_default)
        self.menu_style.addAction(self.action_fusion)
        self.menu_style.addAction(self.action_windows)
        self.menu_settings.addAction(self.menu_style.menuAction())
        self.menubar.addAction(self.menu_settings.menuAction())
        self.menubar.addAction(self.menu_help.menuAction())

        self.retranslateUi(main_entrance)
        QtCore.QMetaObject.connectSlotsByName(main_entrance)

    def retranslateUi(self, main_entrance):
        _translate = QtCore.QCoreApplication.translate
        main_entrance.setWindowTitle(_translate("main_entrance", "AwesomePyKit"))
        self.pb_pkg_mgr.setToolTip(_translate("main_entrance", "管理不同 Python 环境中的第三方模块。"))
        self.pb_pkg_mgr.setText(_translate("main_entrance", "包管理器"))
        self.pb_pyi_tool.setToolTip(_translate("main_entrance", "使用 Pyinstaller 将 Python 程序打包成 exe 可执行文件。"))
        self.pb_pyi_tool.setText(_translate("main_entrance", "程序打包工具"))
        self.pb_index_mgr.setToolTip(_translate("main_entrance", "设置pip全局镜像源地址。"))
        self.pb_index_mgr.setText(_translate("main_entrance", "镜像源设置"))
        self.pb_pkg_dload.setToolTip(_translate("main_entrance", "Python 的模块、包下载工具，可批量下载。"))
        self.pb_pkg_dload.setText(_translate("main_entrance", "模块安装包下载"))
        self.menu_help.setTitle(_translate("main_entrance", "关于"))
        self.menu_settings.setTitle(_translate("main_entrance", "设置"))
        self.menu_style.setTitle(_translate("main_entrance", "界面风格"))
        self.description.setText(_translate("main_entrance", "功能说明"))
        self.action_about.setText(_translate("main_entrance", "关于软件"))
        self.contribution.setText(_translate("main_entrance", "参与贡献"))
        self.action_fusion.setText(_translate("main_entrance", "Fusion 风格"))
        self.action_windows.setText(_translate("main_entrance", "经典风格"))
        self.action_default.setText(_translate("main_entrance", "原生风格"))

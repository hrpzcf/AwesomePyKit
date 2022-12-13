# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_entrance.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_main_entrance(object):
    def setupUi(self, main_entrance):
        if not main_entrance.objectName():
            main_entrance.setObjectName(u"main_entrance")
        main_entrance.resize(202, 41)
        self.action_fusion = QAction(main_entrance)
        self.action_fusion.setObjectName(u"action_fusion")
        self.action_windows = QAction(main_entrance)
        self.action_windows.setObjectName(u"action_windows")
        self.action_native = QAction(main_entrance)
        self.action_native.setObjectName(u"action_native")
        self.centralwidget = QWidget(main_entrance)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.uiPushButton_pkg_mgr = QPushButton(self.centralwidget)
        self.uiPushButton_pkg_mgr.setObjectName(u"uiPushButton_pkg_mgr")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uiPushButton_pkg_mgr.sizePolicy().hasHeightForWidth())
        self.uiPushButton_pkg_mgr.setSizePolicy(sizePolicy)
        self.uiPushButton_pkg_mgr.setStyleSheet(u"QPushButton:hover{border-radius:4px;background-color:rgba(190, 190, 190, 160);}\n"
"QPushButton:pressed{border-radius:4px;background-color:rgba(150, 150, 150, 160);}\n"
"QPushButton::menu-indicator{image:none}")
        self.uiPushButton_pkg_mgr.setIconSize(QSize(32, 32))
        self.uiPushButton_pkg_mgr.setFlat(True)

        self.horizontalLayout.addWidget(self.uiPushButton_pkg_mgr)

        self.uiPushButton_pyi_tool = QPushButton(self.centralwidget)
        self.uiPushButton_pyi_tool.setObjectName(u"uiPushButton_pyi_tool")
        sizePolicy.setHeightForWidth(self.uiPushButton_pyi_tool.sizePolicy().hasHeightForWidth())
        self.uiPushButton_pyi_tool.setSizePolicy(sizePolicy)
        self.uiPushButton_pyi_tool.setStyleSheet(u"QPushButton:hover{border-radius:4px;background-color:rgba(190, 190, 190, 160);}\n"
"QPushButton:pressed{border-radius:4px;background-color:rgba(150, 150, 150, 160);}\n"
"QPushButton::menu-indicator{image:none}")
        self.uiPushButton_pyi_tool.setIconSize(QSize(32, 32))
        self.uiPushButton_pyi_tool.setFlat(True)

        self.horizontalLayout.addWidget(self.uiPushButton_pyi_tool)

        self.uiPushButton_index_mgr = QPushButton(self.centralwidget)
        self.uiPushButton_index_mgr.setObjectName(u"uiPushButton_index_mgr")
        sizePolicy.setHeightForWidth(self.uiPushButton_index_mgr.sizePolicy().hasHeightForWidth())
        self.uiPushButton_index_mgr.setSizePolicy(sizePolicy)
        self.uiPushButton_index_mgr.setStyleSheet(u"QPushButton:hover{border-radius:4px;background-color:rgba(190, 190, 190, 160);}\n"
"QPushButton:pressed{border-radius:4px;background-color:rgba(150, 150, 150, 160);}\n"
"QPushButton::menu-indicator{image:none}")
        self.uiPushButton_index_mgr.setIconSize(QSize(32, 32))
        self.uiPushButton_index_mgr.setFlat(True)

        self.horizontalLayout.addWidget(self.uiPushButton_index_mgr)

        self.uiPushButton_pkg_dload = QPushButton(self.centralwidget)
        self.uiPushButton_pkg_dload.setObjectName(u"uiPushButton_pkg_dload")
        sizePolicy.setHeightForWidth(self.uiPushButton_pkg_dload.sizePolicy().hasHeightForWidth())
        self.uiPushButton_pkg_dload.setSizePolicy(sizePolicy)
        self.uiPushButton_pkg_dload.setStyleSheet(u"QPushButton:hover{border-radius:4px;background-color:rgba(190, 190, 190, 160);}\n"
"QPushButton:pressed{border-radius:4px;background-color:rgba(150, 150, 150, 160);}\n"
"QPushButton::menu-indicator{image:none}")
        self.uiPushButton_pkg_dload.setIconSize(QSize(32, 32))
        self.uiPushButton_pkg_dload.setFlat(True)

        self.horizontalLayout.addWidget(self.uiPushButton_pkg_dload)

        self.uiPushButton_settings = QPushButton(self.centralwidget)
        self.uiPushButton_settings.setObjectName(u"uiPushButton_settings")
        sizePolicy.setHeightForWidth(self.uiPushButton_settings.sizePolicy().hasHeightForWidth())
        self.uiPushButton_settings.setSizePolicy(sizePolicy)
        self.uiPushButton_settings.setStyleSheet(u"QPushButton:hover{border-radius:4px;background-color:rgba(190, 190, 190, 160);}\n"
"QPushButton:pressed{border-radius:4px;background-color:rgba(150, 150, 150, 160);}\n"
"QPushButton::menu-indicator{image:none}")
        self.uiPushButton_settings.setIconSize(QSize(32, 32))
        self.uiPushButton_settings.setFlat(True)

        self.horizontalLayout.addWidget(self.uiPushButton_settings)

        main_entrance.setCentralWidget(self.centralwidget)

        self.retranslateUi(main_entrance)

        QMetaObject.connectSlotsByName(main_entrance)
    # setupUi

    def retranslateUi(self, main_entrance):
        main_entrance.setWindowTitle(QCoreApplication.translate("main_entrance", u"Awespykit", None))
        self.action_fusion.setText(QCoreApplication.translate("main_entrance", u"Fusion", None))
        self.action_windows.setText(QCoreApplication.translate("main_entrance", u"\u7ecf\u5178\u98ce\u683c", None))
        self.action_native.setText(QCoreApplication.translate("main_entrance", u"\u539f\u751f\u98ce\u683c", None))
#if QT_CONFIG(tooltip)
        self.uiPushButton_pkg_mgr.setToolTip(QCoreApplication.translate("main_entrance", u"\u5305\u7ba1\u7406\u5668\n"
"\u7528\u4e8e\u7ba1\u7406\u4e0d\u540c Python \u73af\u5883\u4e2d\u7684\u5305/\u5e93/\u6a21\u5757", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.uiPushButton_pyi_tool.setToolTip(QCoreApplication.translate("main_entrance", u"\u7a0b\u5e8f\u6253\u5305\u5de5\u5177\n"
"\u4f7f\u7528 Pyinstaller \u5c06 Python \u7a0b\u5e8f\u6253\u5305\u6210 exe \u6587\u4ef6", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.uiPushButton_index_mgr.setToolTip(QCoreApplication.translate("main_entrance", u"Pip \u6e90\u8bbe\u7f6e\u5de5\u5177\n"
"\u8bbe\u7f6e\u4e0d\u540c\u7684\u955c\u50cf\u6e90\u4e3a pip \u5168\u5c40\u7d22\u5f15\u6e90\uff0c\u52a0\u5feb pip \u4e0b\u8f7d\u901f\u5ea6", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.uiPushButton_pkg_dload.setToolTip(QCoreApplication.translate("main_entrance", u"\u6a21\u5757\u5b89\u88c5\u5305\u4e0b\u8f7d\u5668\n"
"\u7528\u4e8e\u4e0b\u8f7d Python \u5404\u79cd\u7b2c\u4e09\u65b9\u5305/\u5e93/\u6a21\u5757\u7684\u79bb\u7ebf\u5b89\u88c5\u5305", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.uiPushButton_settings.setToolTip(QCoreApplication.translate("main_entrance", u"\u5de5\u5177\u7bb1\u7684\u8bbe\u7f6e\u83dc\u5355\n"
"\u5305\u542b\u754c\u9762\u98ce\u683c\u8bbe\u7f6e\u3001\u5173\u4e8e\u83dc\u5355", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi


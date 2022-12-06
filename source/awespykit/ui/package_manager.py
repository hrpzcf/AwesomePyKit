# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'package_manager.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_package_manager(object):
    def setupUi(self, package_manager):
        if not package_manager.objectName():
            package_manager.setObjectName("package_manager")
        package_manager.setWindowModality(Qt.WindowModal)
        package_manager.resize(900, 620)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        package_manager.setFont(font)
        self.centralwidget = QWidget(package_manager)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_6 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setHandleWidth(6)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lb_python_dir = QLabel(self.layoutWidget)
        self.lb_python_dir.setObjectName("lb_python_dir")
        self.lb_python_dir.setMinimumSize(QSize(0, 25))

        self.verticalLayout.addWidget(self.lb_python_dir)

        self.lw_env_list = QListWidget(self.layoutWidget)
        self.lw_env_list.setObjectName("lw_env_list")
        palette = QPalette()
        brush = QBrush(QColor(0, 120, 215, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.Highlight, brush)
        brush1 = QBrush(QColor(255, 255, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.HighlightedText, brush1)
        brush2 = QBrush(QColor(155, 222, 255, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.Highlight, brush2)
        brush3 = QBrush(QColor(0, 0, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush3)
        brush4 = QBrush(QColor(190, 190, 190, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.Highlight, brush4)
        palette.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush1)
        self.lw_env_list.setPalette(palette)
        self.lw_env_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lw_env_list.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.verticalLayout.addWidget(self.lw_env_list)

        self.verticalLayout.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btn_autosearch = QPushButton(self.layoutWidget)
        self.btn_autosearch.setObjectName("btn_autosearch")

        self.horizontalLayout.addWidget(self.btn_autosearch)

        self.btn_addmanully = QPushButton(self.layoutWidget)
        self.btn_addmanully.setObjectName("btn_addmanully")

        self.horizontalLayout.addWidget(self.btn_addmanully)

        self.btn_delselected = QPushButton(self.layoutWidget)
        self.btn_delselected.setObjectName("btn_delselected")

        self.horizontalLayout.addWidget(self.btn_delselected)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.verticalLayout_3.setStretch(0, 1)
        self.splitter.addWidget(self.layoutWidget)
        self.layoutWidget1 = QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_4 = QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lb_installed_pkgs_info = QLabel(self.layoutWidget1)
        self.lb_installed_pkgs_info.setObjectName("lb_installed_pkgs_info")

        self.horizontalLayout_4.addWidget(self.lb_installed_pkgs_info)

        self.horizontalSpacer = QSpacerItem(
            0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.le_search_pkgs_kwd = QLineEdit(self.layoutWidget1)
        self.le_search_pkgs_kwd.setObjectName("le_search_pkgs_kwd")
        self.le_search_pkgs_kwd.setClearButtonEnabled(True)

        self.horizontalLayout_4.addWidget(self.le_search_pkgs_kwd)

        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.tw_installed_info = QTableWidget(self.layoutWidget1)
        if self.tw_installed_info.columnCount() < 4:
            self.tw_installed_info.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.tw_installed_info.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tw_installed_info.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tw_installed_info.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tw_installed_info.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.tw_installed_info.setObjectName("tw_installed_info")
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.Highlight, brush)
        palette1.setBrush(QPalette.Active, QPalette.HighlightedText, brush1)
        palette1.setBrush(QPalette.Inactive, QPalette.Highlight, brush2)
        palette1.setBrush(QPalette.Inactive, QPalette.HighlightedText, brush3)
        palette1.setBrush(QPalette.Disabled, QPalette.Highlight, brush4)
        palette1.setBrush(QPalette.Disabled, QPalette.HighlightedText, brush1)
        self.tw_installed_info.setPalette(palette1)
        self.tw_installed_info.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tw_installed_info.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tw_installed_info.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tw_installed_info.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tw_installed_info.setCornerButtonEnabled(False)
        self.tw_installed_info.setColumnCount(4)
        self.tw_installed_info.horizontalHeader().setHighlightSections(False)
        self.tw_installed_info.verticalHeader().setHighlightSections(False)

        self.verticalLayout_2.addWidget(self.tw_installed_info)

        self.verticalLayout_2.setStretch(1, 1)

        self.verticalLayout_4.addLayout(self.verticalLayout_2)

        self.glo_table_btns = QGridLayout()
        self.glo_table_btns.setObjectName("glo_table_btns")
        self.btn_upgrade_package = QPushButton(self.layoutWidget1)
        self.btn_upgrade_package.setObjectName("btn_upgrade_package")

        self.glo_table_btns.addWidget(self.btn_upgrade_package, 1, 2, 1, 1)

        self.btn_check_for_updates = QPushButton(self.layoutWidget1)
        self.btn_check_for_updates.setObjectName("btn_check_for_updates")

        self.glo_table_btns.addWidget(self.btn_check_for_updates, 0, 3, 1, 1)

        self.btn_install_package = QPushButton(self.layoutWidget1)
        self.btn_install_package.setObjectName("btn_install_package")

        self.glo_table_btns.addWidget(self.btn_install_package, 1, 0, 1, 1)

        self.lb_num_selected_items = QLabel(self.layoutWidget1)
        self.lb_num_selected_items.setObjectName("lb_num_selected_items")
        font1 = QFont()
        font1.setFamily("Microsoft YaHei UI")
        font1.setPointSize(8)
        self.lb_num_selected_items.setFont(font1)

        self.glo_table_btns.addWidget(self.lb_num_selected_items, 0, 0, 1, 1)

        self.btn_uninstall_package = QPushButton(self.layoutWidget1)
        self.btn_uninstall_package.setObjectName("btn_uninstall_package")

        self.glo_table_btns.addWidget(self.btn_uninstall_package, 1, 1, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_2.addWidget(self.label_2)

        self.cb_check_uncheck_all = QCheckBox(self.layoutWidget1)
        self.cb_check_uncheck_all.setObjectName("cb_check_uncheck_all")

        self.horizontalLayout_2.addWidget(self.cb_check_uncheck_all)

        self.glo_table_btns.addLayout(self.horizontalLayout_2, 0, 1, 1, 1)

        self.uiPushButton_show_output = QPushButton(self.layoutWidget1)
        self.uiPushButton_show_output.setObjectName("uiPushButton_show_output")

        self.glo_table_btns.addWidget(self.uiPushButton_show_output, 0, 2, 1, 1)

        self.btn_upgrade_all = QPushButton(self.layoutWidget1)
        self.btn_upgrade_all.setObjectName("btn_upgrade_all")

        self.glo_table_btns.addWidget(self.btn_upgrade_all, 1, 3, 1, 1)

        self.verticalLayout_4.addLayout(self.glo_table_btns)

        self.verticalLayout_4.setStretch(0, 1)
        self.splitter.addWidget(self.layoutWidget1)

        self.verticalLayout_5.addWidget(self.splitter)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(-1, -1, 4, -1)
        self.lb_loading_gif = QLabel(self.centralwidget)
        self.lb_loading_gif.setObjectName("lb_loading_gif")
        self.lb_loading_gif.setFont(font1)
        self.lb_loading_gif.setAlignment(
            Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter
        )

        self.horizontalLayout_3.addWidget(self.lb_loading_gif)

        self.lb_loading_tip = QLabel(self.centralwidget)
        self.lb_loading_tip.setObjectName("lb_loading_tip")
        self.lb_loading_tip.setFont(font1)
        self.lb_loading_tip.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.horizontalLayout_3.addWidget(self.lb_loading_tip)

        self.horizontalLayout_3.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_3)

        self.verticalLayout_5.setStretch(0, 1)

        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        package_manager.setCentralWidget(self.centralwidget)

        self.retranslateUi(package_manager)

        QMetaObject.connectSlotsByName(package_manager)

    # setupUi

    def retranslateUi(self, package_manager):
        package_manager.setWindowTitle(
            QCoreApplication.translate(
                "package_manager", "\u5305\u7ba1\u7406\u5668", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.lb_python_dir.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u663e\u793a\u5f53\u524d\u641c\u7d22\u5230\u7684/\u7528\u6237\u6dfb\u52a0\u7684 Python \u76ee\u5f55\u8def\u5f84\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lb_python_dir.setText(
            QCoreApplication.translate(
                "package_manager", "Python \u73af\u5883\uff1a", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.lw_env_list.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u4f7f\u7528\u9f20\u6807\u5de6\u952e\u70b9\u51fb\u52a0\u8f7d\u9009\u4e2d\u7684 Python \u73af\u5883\u5df2\u5b89\u88c5\u7684\u5305\u4fe1\u606f\u5217\u8868\uff0c\u4f7f\u7528\u9f20\u6807\u53f3\u952e\u70b9\u51fb\u6216\u4f7f\u7528\u4e0a\u4e0b\u65b9\u5411\u952e\u9009\u62e9\u5219\u4e0d\u52a0\u8f7d\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.btn_autosearch.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u81ea\u52a8\u641c\u7d22\u5e38\u7528\u5b89\u88c5\u4f4d\u7f6e\u4e2d\u7684 Python \u76ee\u5f55\u5e76\u5c06\u8def\u5f84\u6dfb\u52a0\u5230 Python \u73af\u5883\u5217\u8868\u4fdd\u5b58\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_autosearch.setText(
            QCoreApplication.translate(
                "package_manager", "\u81ea\u52a8\u641c\u7d22", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.btn_addmanully.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u624b\u52a8\u5c06 Python \u76ee\u5f55\u8def\u5f84\u6dfb\u52a0\u5230\u672c Python \u73af\u5883\u5217\u8868\u4ee5\u4fbf\u4e0b\u6b21\u4f7f\u7528\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_addmanully.setText(
            QCoreApplication.translate(
                "package_manager", "\u624b\u52a8\u6dfb\u52a0", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.btn_delselected.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u5c06 Python \u73af\u5883\u5217\u8868\u4e2d\u7684\u9009\u4e2d\u9879\u79fb\u9664(\u4e0d\u4f1a\u5220\u9664\u672c\u673a Python \u76ee\u5f55)\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_delselected.setText(
            QCoreApplication.translate(
                "package_manager", "\u79fb\u9664\u9009\u4e2d\u9879", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.lb_installed_pkgs_info.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u9009\u4e2d\u7684 Python \u73af\u5883\u4e2d\u5df2\u5b89\u88c5\u7684\u5305\u540d\u3001\u5f53\u524d\u7248\u672c\u3001\u6700\u65b0\u7248\u672c\u3001\u5b89\u88c5\u72b6\u6001\u4fe1\u606f\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.lb_installed_pkgs_info.setText(
            QCoreApplication.translate(
                "package_manager",
                "\u5df2\u5b89\u88c5\u7684\u5305\u4fe1\u606f\uff1a",
                None,
            )
        )
        self.le_search_pkgs_kwd.setPlaceholderText(
            QCoreApplication.translate("package_manager", "\u641c\u7d22", None)
        )
        ___qtablewidgetitem = self.tw_installed_info.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(
            QCoreApplication.translate("package_manager", "\u540d\u79f0", None)
        )
        ___qtablewidgetitem1 = self.tw_installed_info.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate(
                "package_manager", "\u5f53\u524d\u7248\u672c", None
            )
        )
        ___qtablewidgetitem2 = self.tw_installed_info.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate(
                "package_manager", "\u6700\u65b0\u7248\u672c", None
            )
        )
        ___qtablewidgetitem3 = self.tw_installed_info.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("package_manager", "\u72b6\u6001", None)
        )
        # if QT_CONFIG(tooltip)
        self.btn_upgrade_package.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u5347\u7ea7\u8868\u683c\u4e2d\u88ab\u9009\u4e2d\u7684\u5305\u3002\n"
                "\u6ce8\u610f\uff0c\u88ab\u9009\u4e2d\u7684\u5305\u5982\u679c\u6ca1\u6709\u65b0\u7248\u672c\u5219\u4e0d\u5347\u7ea7\uff0c\u652f\u6301\u591a\u9009\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_upgrade_package.setText(
            QCoreApplication.translate("package_manager", "\u5347\u7ea7", None)
        )
        # if QT_CONFIG(tooltip)
        self.btn_check_for_updates.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                '\u68c0\u67e5\u9009\u4e2d\u7684 Python \u73af\u5883\u4e2d\u7684\u6240\u6709\u6a21\u5757\u7684\u6700\u65b0\u7248\u672c\uff0c\u6709\u65b0\u7248\u672c\u5219\u5728"\u6700\u65b0\u7248\u672c"\u5217\u4e2d\u663e\u793a\u7248\u672c\u53f7\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_check_for_updates.setText(
            QCoreApplication.translate(
                "package_manager", "\u68c0\u67e5\u66f4\u65b0", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.btn_install_package.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u5c06\u8f93\u5165\u7684\u5305\u540d\u5b89\u88c5\u5230\u9009\u4e2d\u7684 Python \u73af\u5883\u4e2d\u3002\n"
                "\u591a\u4e2a\u5305\u540d\u8bf7\u7528\u7a7a\u683c\u9694\u5f00\uff0c\u652f\u6301\u8f93\u5165\u4e0e pip \u547d\u4ee4 install \u9009\u9879\u76f8\u540c\u7684\u53c2\u6570\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_install_package.setText(
            QCoreApplication.translate("package_manager", "\u5b89\u88c5", None)
        )
        # if QT_CONFIG(tooltip)
        self.btn_uninstall_package.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u5c06\u8868\u683c\u4e2d\u9009\u4e2d\u7684\u5305\u5378\u8f7d(\u4ec5\u4ece\u9009\u4e2d\u7684 Python \u73af\u5883\u4e2d\u5378\u8f7d)\u3002\n"
                "\u6ce8\u610f\uff0c\u5378\u8f7d\u65f6\u8868\u683c\u4e2d\u7684\u6761\u76ee\u652f\u6301\u591a\u9009\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_uninstall_package.setText(
            QCoreApplication.translate("package_manager", "\u5378\u8f7d", None)
        )
        self.label_2.setText("")
        self.cb_check_uncheck_all.setText(
            QCoreApplication.translate("package_manager", "\u5168\u9009", None)
        )
        self.uiPushButton_show_output.setText(
            QCoreApplication.translate(
                "package_manager", "\u8f93\u51fa\u7a97\u53e3", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.btn_upgrade_all.setToolTip(
            QCoreApplication.translate(
                "package_manager",
                "\u5347\u7ea7\u8868\u683c\u4e2d\u5217\u51fa\u7684\u6240\u6709\u663e\u793a\u6709\u65b0\u7248\u672c\u7684\u5305\u3002\n"
                '\u4f7f\u7528\u6b64\u529f\u80fd\u524d\u8bf7\u5148\u70b9\u51fb"\u68c0\u67e5\u66f4\u65b0"\u6309\u94ae\u4ee5\u68c0\u67e5\u662f\u5426\u6709\u65b0\u7248\u672c\uff0c\u518d\u70b9\u51fb\u6b64\u6309\u94ae\u5347\u7ea7\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.btn_upgrade_all.setText(
            QCoreApplication.translate(
                "package_manager", "\u5347\u7ea7\u5168\u90e8", None
            )
        )

    # retranslateUi

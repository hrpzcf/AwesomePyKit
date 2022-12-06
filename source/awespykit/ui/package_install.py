# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'package_install.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_package_install(object):
    def setupUi(self, package_install):
        if not package_install.objectName():
            package_install.setObjectName("package_install")
        package_install.setWindowModality(Qt.WindowModal)
        package_install.resize(395, 438)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        package_install.setFont(font)
        package_install.setContextMenuPolicy(Qt.NoContextMenu)
        self.centralwidget = QWidget(package_install)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.uiLabel_target_environment = QLabel(self.centralwidget)
        self.uiLabel_target_environment.setObjectName("uiLabel_target_environment")
        self.uiLabel_target_environment.setFrameShape(QFrame.Box)

        self.horizontalLayout.addWidget(self.uiLabel_target_environment)

        self.horizontalLayout.setStretch(1, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")

        self.verticalLayout_3.addWidget(self.label)

        self.uiHorizontalLayout_package_name = QHBoxLayout()
        self.uiHorizontalLayout_package_name.setObjectName(
            "uiHorizontalLayout_package_name"
        )
        self.pte_package_names_old = QPlainTextEdit(self.centralwidget)
        self.pte_package_names_old.setObjectName("pte_package_names_old")

        self.uiHorizontalLayout_package_name.addWidget(self.pte_package_names_old)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.cb_including_pre = QCheckBox(self.centralwidget)
        self.cb_including_pre.setObjectName("cb_including_pre")

        self.verticalLayout_2.addWidget(self.cb_including_pre)

        self.cb_install_for_user = QCheckBox(self.centralwidget)
        self.cb_install_for_user.setObjectName("cb_install_for_user")

        self.verticalLayout_2.addWidget(self.cb_install_for_user)

        self.uiCheckBox_force_reinstall = QCheckBox(self.centralwidget)
        self.uiCheckBox_force_reinstall.setObjectName("uiCheckBox_force_reinstall")

        self.verticalLayout_2.addWidget(self.uiCheckBox_force_reinstall)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_2.addWidget(self.line_2)

        self.pb_load_from_text = QPushButton(self.centralwidget)
        self.pb_load_from_text.setObjectName("pb_load_from_text")

        self.verticalLayout_2.addWidget(self.pb_load_from_text)

        self.pb_save_as_text = QPushButton(self.centralwidget)
        self.pb_save_as_text.setObjectName("pb_save_as_text")

        self.verticalLayout_2.addWidget(self.pb_save_as_text)

        self.pb_do_install = QPushButton(self.centralwidget)
        self.pb_do_install.setObjectName("pb_do_install")
        self.pb_do_install.setMinimumSize(QSize(0, 50))
        palette = QPalette()
        brush = QBrush(QColor(0, 0, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush1 = QBrush(QColor(0, 0, 0, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush1)
        brush2 = QBrush(QColor(120, 120, 120, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush2)
        self.pb_do_install.setPalette(palette)
        font1 = QFont()
        font1.setFamily("Microsoft YaHei UI")
        font1.setPointSize(12)
        self.pb_do_install.setFont(font1)

        self.verticalLayout_2.addWidget(self.pb_do_install)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.uiHorizontalLayout_package_name.addLayout(self.verticalLayout_2)

        self.verticalLayout_3.addLayout(self.uiHorizontalLayout_package_name)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cb_use_index_url = QCheckBox(self.centralwidget)
        self.cb_use_index_url.setObjectName("cb_use_index_url")

        self.verticalLayout.addWidget(self.cb_use_index_url)

        self.le_use_index_url = QLineEdit(self.centralwidget)
        self.le_use_index_url.setObjectName("le_use_index_url")

        self.verticalLayout.addWidget(self.le_use_index_url)

        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        font2 = QFont()
        font2.setFamily("Consolas")
        font2.setPointSize(8)
        self.label_2.setFont(font2)
        self.label_2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)

        self.verticalLayout_3.addWidget(self.label_2)

        package_install.setCentralWidget(self.centralwidget)

        self.retranslateUi(package_install)

        QMetaObject.connectSlotsByName(package_install)

    # setupUi

    def retranslateUi(self, package_install):
        package_install.setWindowTitle(
            QCoreApplication.translate("package_install", "\u5b89\u88c5", None)
        )
        # if QT_CONFIG(tooltip)
        self.label_3.setToolTip(
            QCoreApplication.translate(
                "package_install",
                "\u5f53\u524d\u5373\u5c06\u5b89\u88c5\u7684\u5305\u7684\u76ee\u6807\u73af\u5883\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_3.setText(
            QCoreApplication.translate(
                "package_install", "\u76ee\u6807\u73af\u5883\uff1a", None
            )
        )
        self.label.setText(
            QCoreApplication.translate(
                "package_install",
                "\u8981\u5b89\u88c5\u7684\u5305\u540d\u79f0\uff08\u6bcf\u884c\u4e00\u4e2a\uff09\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_including_pre.setToolTip(
            QCoreApplication.translate(
                "package_install",
                "\u4ece\u7f51\u7edc\u5b89\u88c5\u65f6\u662f\u5426\u67e5\u627e\u5305\u62ec\u9884\u53d1\u884c\u7248\u548c\u5f00\u53d1\u7248\u5728\u5185\u7684\u7248\u672c\u3002\n"
                "\u5982\u679c\u9884\u53d1\u884c\u7248\u6216\u5f00\u53d1\u7248\u662f\u6700\u65b0\u7248\u672c\uff0c\u5219\u5b89\u88c5\u9884\u53d1\u884c\u7248\u6216\u5f00\u53d1\u7248\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_including_pre.setText(
            QCoreApplication.translate(
                "package_install",
                "\u5305\u62ec\u9884\u53d1\u884c\u7248\u548c\u5f00\u53d1\u7248",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_install_for_user.setToolTip(
            QCoreApplication.translate(
                "package_install",
                "\u5c06\u5305\u5b89\u88c5\u5230\u7cfb\u7edf\u5f53\u524d\u767b\u5f55\u7684\u7528\u6237\u7684\u7528\u6237\u76ee\u5f55\u5185\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_install_for_user.setText(
            QCoreApplication.translate(
                "package_install",
                "\u4ec5\u4e3a\u7cfb\u7edf\u5f53\u524d\u7528\u6237\u5b89\u88c5",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.uiCheckBox_force_reinstall.setToolTip(
            QCoreApplication.translate(
                "package_install",
                "\u5f3a\u5236\u91cd\u65b0\u5b89\u88c5\u6307\u5b9a\u7684\u5305\uff0c\u5305\u62ec\u5b83\u7684\u4f9d\u8d56\u5305\uff0c\u4f9d\u8d56\u5305\u5c06\u88ab\u91cd\u65b0\u5b89\u88c5\u4e3a\u7b26\u5408\u8981\u6c42\u7684\u7248\u672c\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiCheckBox_force_reinstall.setText(
            QCoreApplication.translate(
                "package_install",
                "\u5f3a\u5236\u91cd\u65b0\u5b89\u88c5(\u5305\u62ec\u4f9d\u8d56)",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.pb_load_from_text.setToolTip(
            QCoreApplication.translate(
                "package_install",
                "\u4ece\u6587\u672c\u6587\u4ef6\u8f7d\u5165\u540d\u79f0\u53ca\u7248\u672c\u7b49\u5185\u5bb9\u3002\n"
                "\u4f8b\u5982\u4ece\u5e38\u89c1\u7684requirements.txt\u6587\u4ef6\u8f7d\u5165\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_load_from_text.setText(
            QCoreApplication.translate(
                "package_install", "\u4ece\u6587\u4ef6\u52a0\u8f7d\u540d\u79f0", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.pb_save_as_text.setToolTip(
            QCoreApplication.translate(
                "package_install",
                "\u5c06\u6587\u672c\u6846\u5185\u7684\u5185\u5bb9\u4fdd\u5b58\u81f3\u6587\u672c\u6587\u4ef6\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_save_as_text.setText(
            QCoreApplication.translate(
                "package_install", "\u540d\u79f0\u4fdd\u5b58\u81f3\u6587\u4ef6", None
            )
        )
        self.pb_do_install.setText(
            QCoreApplication.translate(
                "package_install", "\u5f00\u59cb\u5b89\u88c5", None
            )
        )
        self.cb_use_index_url.setText(
            QCoreApplication.translate(
                "package_install",
                "\u4e34\u65f6\u4f7f\u7528\u5176\u4ed6\u955c\u50cf\u6e90\uff1a",
                None,
            )
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "package_install",
                "\u540d\u79f0\u540e\u652f\u6301\u8ddf\u968f\u4ee5\u4e0b\u7b26\u53f7\u9650\u5b9a\u8981\u5b89\u88c5\u7684\u7248\u672c\uff1a\n"
                '"=="\u3001">="\u3001"<="\u3001">"\u3001"<"\u3001","\n'
                "\u6bcf\u884c\u4e00\u4e2a\u540d\u79f0\uff0c\u540d\u79f0\u548c\u9650\u5b9a\u7b26\u4e2d\u4e0d\u5141\u8bb8\u51fa\u73b0\u7a7a\u683c\u3002\n"
                "\u4f8b\u5982\uff1afastpip>=0.6.2,<0.10.0\n"
                "\u652f\u6301\u5c06whl\u6587\u4ef6\u62d6\u5165\u6587\u672c\u6846\u5185\u4ee5\u4ece\u672c\u5730\u6587\u4ef6\u5b89\u88c5\u8be5\u5305\uff0cwhl\u6587\u4ef6\u9700\u4e3a\u6b63\u786e\u7248\u672c\u3002",
                None,
            )
        )

    # retranslateUi

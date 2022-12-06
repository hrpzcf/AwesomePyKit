# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'package_download.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_package_download(object):
    def setupUi(self, package_download):
        if not package_download.objectName():
            package_download.setObjectName("package_download")
        package_download.setWindowModality(Qt.WindowModal)
        package_download.resize(620, 658)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        package_download.setFont(font)
        package_download.setContextMenuPolicy(Qt.NoContextMenu)
        self.centralwidget = QWidget(package_download)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_14 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(8, 8, 8, 8)
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")

        self.verticalLayout_8.addWidget(self.label)

        self.pte_package_names = QPlainTextEdit(self.centralwidget)
        self.pte_package_names.setObjectName("pte_package_names")

        self.verticalLayout_8.addWidget(self.pte_package_names)

        self.verticalLayout_10.addLayout(self.verticalLayout_8)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pb_clear_package_names = QPushButton(self.centralwidget)
        self.pb_clear_package_names.setObjectName("pb_clear_package_names")

        self.horizontalLayout_3.addWidget(self.pb_clear_package_names)

        self.pb_load_from_text = QPushButton(self.centralwidget)
        self.pb_load_from_text.setObjectName("pb_load_from_text")

        self.horizontalLayout_3.addWidget(self.pb_load_from_text)

        self.pb_save_as_text = QPushButton(self.centralwidget)
        self.pb_save_as_text.setObjectName("pb_save_as_text")

        self.horizontalLayout_3.addWidget(self.pb_save_as_text)

        self.horizontalLayout_3.setStretch(1, 1)
        self.horizontalLayout_3.setStretch(2, 1)

        self.verticalLayout_10.addLayout(self.horizontalLayout_3)

        self.verticalLayout_11.addLayout(self.verticalLayout_10)

        self.line_7 = QFrame(self.centralwidget)
        self.line_7.setObjectName("line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_11.addWidget(self.line_7)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName("label_8")

        self.verticalLayout_9.addWidget(self.label_8)

        self.cmb_derived_from = QComboBox(self.centralwidget)
        self.cmb_derived_from.setObjectName("cmb_derived_from")

        self.verticalLayout_9.addWidget(self.cmb_derived_from)

        self.verticalLayout_11.addLayout(self.verticalLayout_9)

        self.line_8 = QFrame(self.centralwidget)
        self.line_8.setObjectName("line_8")
        self.line_8.setFrameShape(QFrame.HLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_11.addWidget(self.line_8)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        font1 = QFont()
        font1.setFamily("Consolas")
        font1.setPointSize(8)
        self.label_2.setFont(font1)
        self.label_2.setWordWrap(True)

        self.verticalLayout_11.addWidget(self.label_2)

        self.horizontalLayout_6.addLayout(self.verticalLayout_11)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.cb_download_deps = QCheckBox(self.groupBox)
        self.cb_download_deps.setObjectName("cb_download_deps")

        self.verticalLayout_7.addWidget(self.cb_download_deps)

        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.rb_unlimited = QRadioButton(self.groupBox_2)
        self.rb_unlimited.setObjectName("rb_unlimited")

        self.verticalLayout_5.addWidget(self.rb_unlimited)

        self.rb_no_binary = QRadioButton(self.groupBox_2)
        self.rb_no_binary.setObjectName("rb_no_binary")

        self.verticalLayout_5.addWidget(self.rb_no_binary)

        self.rb_only_binary = QRadioButton(self.groupBox_2)
        self.rb_only_binary.setObjectName("rb_only_binary")

        self.verticalLayout_5.addWidget(self.rb_only_binary)

        self.rb_prefer_binary = QRadioButton(self.groupBox_2)
        self.rb_prefer_binary.setObjectName("rb_prefer_binary")

        self.verticalLayout_5.addWidget(self.rb_prefer_binary)

        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.cb_include_pre = QCheckBox(self.groupBox)
        self.cb_include_pre.setObjectName("cb_include_pre")

        self.verticalLayout_7.addWidget(self.cb_include_pre)

        self.cb_ignore_requires_python = QCheckBox(self.groupBox)
        self.cb_ignore_requires_python.setObjectName("cb_ignore_requires_python")

        self.verticalLayout_7.addWidget(self.cb_ignore_requires_python)

        self.line = QFrame(self.groupBox)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.pb_save_to = QPushButton(self.groupBox)
        self.pb_save_to.setObjectName("pb_save_to")

        self.horizontalLayout_5.addWidget(self.pb_save_to)

        self.horizontalLayout_5.setStretch(0, 9)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.le_save_to = QLineEdit(self.groupBox)
        self.le_save_to.setObjectName("le_save_to")

        self.verticalLayout_2.addWidget(self.le_save_to)

        self.verticalLayout_7.addLayout(self.verticalLayout_2)

        self.line_2 = QFrame(self.groupBox)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.le_platform = QLineEdit(self.groupBox)
        self.le_platform.setObjectName("le_platform")

        self.verticalLayout.addWidget(self.le_platform)

        self.verticalLayout_7.addLayout(self.verticalLayout)

        self.line_3 = QFrame(self.groupBox)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_3)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")

        self.horizontalLayout.addWidget(self.label_5)

        self.le_python_version = QLineEdit(self.groupBox)
        self.le_python_version.setObjectName("le_python_version")
        self.le_python_version.setMinimumSize(QSize(180, 0))
        self.le_python_version.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout.addWidget(self.le_python_version)

        self.horizontalLayout.setStretch(1, 9)

        self.verticalLayout_7.addLayout(self.horizontalLayout)

        self.line_4 = QFrame(self.groupBox)
        self.line_4.setObjectName("line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_4)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")

        self.horizontalLayout_2.addWidget(self.label_6)

        self.cmb_implementation = QComboBox(self.groupBox)
        self.cmb_implementation.addItem("")
        self.cmb_implementation.addItem("")
        self.cmb_implementation.addItem("")
        self.cmb_implementation.addItem("")
        self.cmb_implementation.addItem("")
        self.cmb_implementation.addItem("")
        self.cmb_implementation.setObjectName("cmb_implementation")
        self.cmb_implementation.setMinimumSize(QSize(180, 0))
        self.cmb_implementation.setMaximumSize(QSize(180, 16777215))

        self.horizontalLayout_2.addWidget(self.cmb_implementation)

        self.horizontalLayout_2.setStretch(1, 9)

        self.verticalLayout_7.addLayout(self.horizontalLayout_2)

        self.line_5 = QFrame(self.groupBox)
        self.line_5.setObjectName("line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_5)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")

        self.verticalLayout_3.addWidget(self.label_7)

        self.le_abis = QLineEdit(self.groupBox)
        self.le_abis.setObjectName("le_abis")

        self.verticalLayout_3.addWidget(self.le_abis)

        self.verticalLayout_7.addLayout(self.verticalLayout_3)

        self.line_6 = QFrame(self.groupBox)
        self.line_6.setObjectName("line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_6)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.cb_use_index_url = QCheckBox(self.groupBox)
        self.cb_use_index_url.setObjectName("cb_use_index_url")

        self.verticalLayout_4.addWidget(self.cb_use_index_url)

        self.le_index_url = QLineEdit(self.groupBox)
        self.le_index_url.setObjectName("le_index_url")

        self.verticalLayout_4.addWidget(self.le_index_url)

        self.verticalLayout_7.addLayout(self.verticalLayout_4)

        self.verticalLayout_12.addLayout(self.verticalLayout_7)

        self.verticalLayout_13.addWidget(self.groupBox)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_13.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pb_show_dl_list = QPushButton(self.centralwidget)
        self.pb_show_dl_list.setObjectName("pb_show_dl_list")
        self.pb_show_dl_list.setMinimumSize(QSize(0, 50))
        font2 = QFont()
        font2.setFamily("Microsoft YaHei UI")
        font2.setPointSize(10)
        self.pb_show_dl_list.setFont(font2)

        self.horizontalLayout_4.addWidget(self.pb_show_dl_list)

        self.pb_start_download = QPushButton(self.centralwidget)
        self.pb_start_download.setObjectName("pb_start_download")
        self.pb_start_download.setMinimumSize(QSize(0, 50))
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
        self.pb_start_download.setPalette(palette)
        font3 = QFont()
        font3.setFamily("Microsoft YaHei UI")
        font3.setPointSize(12)
        self.pb_start_download.setFont(font3)

        self.horizontalLayout_4.addWidget(self.pb_start_download)

        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_13.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_6.addLayout(self.verticalLayout_13)

        self.verticalLayout_14.addLayout(self.horizontalLayout_6)

        package_download.setCentralWidget(self.centralwidget)

        self.retranslateUi(package_download)

        QMetaObject.connectSlotsByName(package_download)

    # setupUi

    def retranslateUi(self, package_download):
        package_download.setWindowTitle(
            QCoreApplication.translate(
                "package_download", "\u6a21\u5757\u5b89\u88c5\u5305\u4e0b\u8f7d", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.label.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u9700\u8981\u4e0b\u8f7d\u7684\u6a21\u5757\u540d\u79f0\uff0c\u6bcf\u884c\u4e00\u4e2a\u540d\u79f0\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label.setText(
            QCoreApplication.translate("package_download", "\u540d\u79f0\uff1a", None)
        )
        # if QT_CONFIG(tooltip)
        self.pte_package_names.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u9700\u8981\u4e0b\u8f7d\u7684\u6a21\u5757\u540d\u79f0\uff0c\u6bcf\u884c\u4e00\u4e2a\u540d\u79f0\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.pb_clear_package_names.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u6e05\u7a7a\u540d\u79f0\u7f16\u8f91\u533a\u6587\u5b57\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_clear_package_names.setText(
            QCoreApplication.translate("package_download", "\u6e05\u7a7a", None)
        )
        # if QT_CONFIG(tooltip)
        self.pb_load_from_text.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u4ece\u6587\u672c\u6587\u4ef6\u52a0\u8f7d\u540d\u79f0\u5230\u540d\u79f0\u7f16\u8f91\u533a\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_load_from_text.setText(
            QCoreApplication.translate(
                "package_download", "\u4ece\u6587\u4ef6\u52a0\u8f7d\u540d\u79f0", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.pb_save_as_text.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u5c06\u540d\u79f0\u7f16\u8f91\u533a\u7684\u6587\u5b57\u4fdd\u5b58\u5230\u6587\u672c\u6587\u4ef6\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_save_as_text.setText(
            QCoreApplication.translate(
                "package_download", "\u540d\u79f0\u4fdd\u5b58\u5230\u6587\u4ef6", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.label_8.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u4e0b\u8f7d\u5b89\u88c5\u5305\u65f6\u9700\u8c03\u7528\u7684 Python \u73af\u5883\u3002\n"
                "\u53f3\u4fa7\u7559\u7a7a\u7684\u4e0b\u8f7d\u6761\u4ef6\uff0c\u4e0b\u8f7d\u65f6\u4f1a\u4f7f\u7528\u4ece\u6b64\u73af\u5883\u6d3e\u751f\u7684\u6761\u4ef6\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_8.setText(
            QCoreApplication.translate(
                "package_download",
                "\u4e0b\u8f7d\u6761\u4ef6\u9ed8\u8ba4\u6d3e\u751f\u81ea\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cmb_derived_from.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u4e0b\u8f7d\u5b89\u88c5\u5305\u65f6\u9700\u8c03\u7528\u7684 Python \u73af\u5883\u3002\n"
                "\u53f3\u4fa7\u7559\u7a7a\u7684\u4e0b\u8f7d\u6761\u4ef6\uff0c\u4e0b\u8f7d\u65f6\u4f1a\u4f7f\u7528\u4ece\u6b64\u73af\u5883\u6d3e\u751f\u7684\u6761\u4ef6\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_2.setText(
            QCoreApplication.translate(
                "package_download",
                "\u540d\u79f0\u540e\u652f\u6301\u8ddf\u968f\u4ee5\u4e0b\u7b26\u53f7\u9650\u5b9a\u8981\u4e0b\u8f7d\u7684\u7248\u672c\uff1a\n"
                '"=="\u3001">="\u3001"<="\u3001">"\u3001"<"\u3001","\n'
                "\u6bcf\u884c\u4e00\u4e2a\u540d\u79f0\uff0c\u540d\u79f0\u548c\u9650\u5b9a\u7b26\u4e2d\u4e0d\u5141\u8bb8\u51fa\u73b0\u7a7a\u683c\u3002\n"
                "\u4f8b\u5982\uff1afastpip>=0.6.2,<0.10.0\n"
                "\u5982\u679c\u9650\u5236\u6761\u4ef6\u7559\u7a7a\uff0c\u5219\u4e0b\u8f7d\u517c\u5bb9\u6240\u9009\u73af\u5883\u7684\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        self.groupBox.setTitle(
            QCoreApplication.translate(
                "package_download", "\u4e0b\u8f7d\u6761\u4ef6", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_download_deps.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u5bf9\u4e8e\u540d\u79f0\u7f16\u8f91\u533a\u4e2d\u7684\u6bcf\u4e00\u4e2a\u9700\u8981\u4e0b\u8f7d\u7684\u6a21\u5757\uff0c\u662f\u5426\u540c\u65f6\u4e0b\u8f7d\u6a21\u5757\u7684\u4f9d\u8d56\u5e93\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_download_deps.setText(
            QCoreApplication.translate(
                "package_download",
                "\u4e0b\u8f7d\u9700\u8981\u4e0b\u8f7d\u7684\u5305\u7684\u4f9d\u8d56",
                None,
            )
        )
        self.groupBox_2.setTitle("")
        # if QT_CONFIG(tooltip)
        self.rb_unlimited.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u4e0d\u9650\u5236\u4e0b\u8f7d\u4e8c\u8fdb\u5236\u5305\u6216\u8005\u6e90\u4ee3\u7801\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rb_unlimited.setText(
            QCoreApplication.translate(
                "package_download",
                "\u4e0d\u9650\u5236\u4e0b\u8f7d\u7684\u5305\u7c7b\u578b",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.rb_no_binary.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u4ec5\u4e0b\u8f7d\u5305\u7684\u6e90\u4ee3\u7801\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rb_no_binary.setText(
            QCoreApplication.translate(
                "package_download", "\u4ec5\u9009\u62e9\u6e90\u4ee3\u7801\u5305", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.rb_only_binary.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u4ec5\u4e0b\u8f7d\u5305\u7684\u4e8c\u8fdb\u5236\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rb_only_binary.setText(
            QCoreApplication.translate(
                "package_download", "\u4ec5\u9009\u62e9\u4e8c\u8fdb\u5236\u5305", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.rb_prefer_binary.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u5bf9\u4e8e\u65e2\u6709\u4e8c\u8fdb\u5236\u5b89\u88c5\u5305\u53c8\u6709\u6e90\u4ee3\u7801\u5b89\u88c5\u5305\u7684\u6a21\u5757\uff0c\n"
                "\u5982\u679c\u8f83\u65b0\u7248\u672c\u6ca1\u6709\u53d1\u5e03\u4e8c\u8fdb\u5236\u5b89\u88c5\u5305\uff0c\u5219\u5b81\u613f\u4e0b\u8f7d\u8f83\u65e7\u7248\u672c\u7684\u4e8c\u8fdb\u5236\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rb_prefer_binary.setText(
            QCoreApplication.translate(
                "package_download",
                "\u5b81\u9009\u62e9\u65e7\u4e8c\u8fdb\u5236\u5305\u800c\u975e\u65b0\u6e90\u4ee3\u7801\u5305",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_include_pre.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u5982\u679c\u6a21\u5757\u7684\u6700\u65b0\u7248\u672c\u662f\u9884\u53d1\u884c\u7248\u6216\u8005\u662f\u5f00\u53d1\u7248\uff0c\n"
                "\u4e5f\u4e0b\u8f7d\u8fd9\u4e9b\u7248\u672c\uff0c\u5426\u5219\u53ea\u4e0b\u8f7d\u6a21\u5757\u7684\u6700\u65b0\u7a33\u5b9a\u7248\u672c\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_include_pre.setText(
            QCoreApplication.translate(
                "package_download",
                "\u5305\u62ec\u9884\u53d1\u884c\u7248\u548c\u5f00\u53d1\u7248",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_ignore_requires_python.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u5bf9\u4e8e\u90a3\u4e9b\u5bf9 Python \u7248\u672c\u6709\u9650\u5236\u8981\u6c42\u7684\u6a21\u5757\uff0c\u662f\u5426\u5ffd\u7565\u5176\u9650\u5236\u8981\u6c42\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_ignore_requires_python.setText(
            QCoreApplication.translate(
                "package_download",
                "\u5ffd\u7565\u5305\u7684 Python \u7248\u672c\u9650\u5236",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.label_3.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u4e0b\u8f7d\u7684\u6a21\u5757\u5b89\u88c5\u5305\u7684\u4fdd\u5b58\u8def\u5f84\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_3.setText(
            QCoreApplication.translate(
                "package_download", "\u4e0b\u8f7d\u81f3\uff1a", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.pb_save_to.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u9009\u62e9\u4e0b\u8f7d\u7684\u6a21\u5757\u5b89\u88c5\u5305\u7684\u4fdd\u5b58\u8def\u5f84\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_save_to.setText(
            QCoreApplication.translate(
                "package_download", "\u9009\u62e9\u76ee\u5f55", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_save_to.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u4e0b\u8f7d\u7684\u6a21\u5757\u5b89\u88c5\u5305\u7684\u4fdd\u5b58\u8def\u5f84\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_4.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u662f\u5426\u53ea\u4e0b\u8f7d\u517c\u5bb9\u6b64\u5904\u5217\u51fa\u7684\u5e73\u53f0\u7684\u6a21\u5757\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_4.setText(
            QCoreApplication.translate(
                "package_download",
                "\u517c\u5bb9\u5e73\u53f0(\u7a7a\u683c\u5206\u9694)\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_platform.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u662f\u5426\u53ea\u4e0b\u8f7d\u517c\u5bb9\u6b64\u5904\u5217\u51fa\u7684\u5e73\u53f0\u7684\u6a21\u5757\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_5.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u662f\u5426\u53ea\u4e0b\u8f7d\u517c\u5bb9\u6b64\u5904\u5217\u51fa\u7684 Python \u7248\u672c\u7684\u6a21\u5757\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_5.setText(
            QCoreApplication.translate(
                "package_download", "\u517c\u5bb9 Python \u7248\u672c\uff1a", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_python_version.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u662f\u5426\u53ea\u4e0b\u8f7d\u517c\u5bb9\u6b64\u5904\u5217\u51fa\u7684 Python \u7248\u672c\u7684\u6a21\u5757\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_6.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u662f\u5426\u53ea\u4e0b\u8f7d\u517c\u5bb9\u6b64\u5904\u5217\u51fa\u7684 Python \u5b9e\u73b0\u7684\u6a21\u5757\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_6.setText(
            QCoreApplication.translate(
                "package_download",
                "\u517c\u5bb9\u89e3\u91ca\u5668\u5b9e\u73b0\uff1a",
                None,
            )
        )
        self.cmb_implementation.setItemText(0, "")
        self.cmb_implementation.setItemText(
            1,
            QCoreApplication.translate(
                "package_download", "\u65e0\u7279\u5b9a\u5b9e\u73b0", None
            ),
        )
        self.cmb_implementation.setItemText(
            2, QCoreApplication.translate("package_download", "CPython", None)
        )
        self.cmb_implementation.setItemText(
            3, QCoreApplication.translate("package_download", "Jython", None)
        )
        self.cmb_implementation.setItemText(
            4, QCoreApplication.translate("package_download", "PyPy", None)
        )
        self.cmb_implementation.setItemText(
            5, QCoreApplication.translate("package_download", "IronPython", None)
        )

        # if QT_CONFIG(tooltip)
        self.cmb_implementation.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u662f\u5426\u53ea\u4e0b\u8f7d\u517c\u5bb9\u6b64\u5904\u5217\u51fa\u7684 Python \u5b9e\u73b0\u7684\u6a21\u5757\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_7.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u662f\u5426\u53ea\u4e0b\u8f7d\u517c\u5bb9\u6b64\u5904\u5217\u51fa\u7684 Python ABI\u7684\u6a21\u5757\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_7.setText(
            QCoreApplication.translate(
                "package_download",
                "\u517c\u5bb9ABI(\u7a7a\u683c\u5206\u9694)\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_abis.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u662f\u5426\u53ea\u4e0b\u8f7d\u517c\u5bb9\u6b64\u5904\u5217\u51fa\u7684 Python ABI\u7684\u6a21\u5757\u5b89\u88c5\u5305\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.cb_use_index_url.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u662f\u5426\u4ece\u4e34\u65f6\u955c\u50cf\u6e90\u4e0b\u8f7d\u5b89\u88c5\u5305\u3002\n"
                "\u5982\u679c\u4e0d\u52fe\u9009\u6b64\u9009\u9879\uff0c\u5219\u9ed8\u8ba4\u4ece\u7cfb\u7edf\u5df2\u8bbe\u7f6e\u7684\u955c\u50cf\u6e90\u5730\u5740\u4e0b\u8f7d\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_use_index_url.setText(
            QCoreApplication.translate(
                "package_download",
                "\u4f7f\u7528\u4e34\u65f6\u955c\u50cf\u6e90\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_index_url.setToolTip(
            QCoreApplication.translate(
                "package_download",
                "\u4e34\u65f6\u955c\u50cf\u6e90\u5730\u5740\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_show_dl_list.setText(
            QCoreApplication.translate(
                "package_download", "\u4e0b\u8f7d\u5217\u8868", None
            )
        )
        self.pb_start_download.setText(
            QCoreApplication.translate(
                "package_download", "\u5f00\u59cb\u4e0b\u8f7d", None
            )
        )

    # retranslateUi

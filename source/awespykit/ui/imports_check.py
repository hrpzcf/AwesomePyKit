# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'imports_check.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_imports_check(object):
    def setupUi(self, imports_check):
        if not imports_check.objectName():
            imports_check.setObjectName(u"imports_check")
        imports_check.setWindowModality(Qt.WindowModal)
        imports_check.resize(900, 500)
        self.centralwidget = QWidget(imports_check)
        self.centralwidget.setObjectName(u"centralwidget")
        font = QFont()
        font.setFamily(u"Microsoft YaHei UI")
        self.centralwidget.setFont(font)
        self.centralwidget.setContextMenuPolicy(Qt.NoContextMenu)
        self.verticalLayout_3 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.uiLineEdit_current_env = QLineEdit(self.centralwidget)
        self.uiLineEdit_current_env.setObjectName(u"uiLineEdit_current_env")
        self.uiLineEdit_current_env.setFrame(False)
        self.uiLineEdit_current_env.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.uiLineEdit_current_env)

        self.horizontalLayout_2.setStretch(1, 9)

        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.uiTableWidget_missing_imports = QTableWidget(self.centralwidget)
        if (self.uiTableWidget_missing_imports.columnCount() < 3):
            self.uiTableWidget_missing_imports.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.uiTableWidget_missing_imports.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.uiTableWidget_missing_imports.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.uiTableWidget_missing_imports.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.uiTableWidget_missing_imports.setObjectName(u"uiTableWidget_missing_imports")
        self.uiTableWidget_missing_imports.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.uiTableWidget_missing_imports.setSelectionMode(QAbstractItemView.NoSelection)
        self.uiTableWidget_missing_imports.horizontalHeader().setHighlightSections(False)
        self.uiTableWidget_missing_imports.verticalHeader().setHighlightSections(False)

        self.verticalLayout.addWidget(self.uiTableWidget_missing_imports)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.uiPushButton_install_missings = QPushButton(self.centralwidget)
        self.uiPushButton_install_missings.setObjectName(u"uiPushButton_install_missings")

        self.horizontalLayout.addWidget(self.uiPushButton_install_missings)

        self.uiPushButton_confirm = QPushButton(self.centralwidget)
        self.uiPushButton_confirm.setObjectName(u"uiPushButton_confirm")

        self.horizontalLayout.addWidget(self.uiPushButton_confirm)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        imports_check.setCentralWidget(self.centralwidget)

        self.retranslateUi(imports_check)

        QMetaObject.connectSlotsByName(imports_check)
    # setupUi

    def retranslateUi(self, imports_check):
        imports_check.setWindowTitle(QCoreApplication.translate("imports_check", u"\u73af\u5883\u68c0\u67e5", None))
        self.label.setText(QCoreApplication.translate("imports_check", u"\u5f53\u524d\u73af\u5883:", None))
        ___qtablewidgetitem = self.uiTableWidget_missing_imports.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("imports_check", u"\u9879\u76ee\u6587\u4ef6", None));
        ___qtablewidgetitem1 = self.uiTableWidget_missing_imports.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("imports_check", u"\u6587\u4ef6\u5bfc\u5165\u9879", None));
        ___qtablewidgetitem2 = self.uiTableWidget_missing_imports.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("imports_check", u"\u73af\u5883\u7f3a\u5931\u9879", None));
#if QT_CONFIG(tooltip)
        self.uiPushButton_install_missings.setToolTip(QCoreApplication.translate("imports_check", u"\u4e00\u952e\u5b89\u88c5\u8be5\u73af\u5883\u6240\u6709\u7f3a\u5931\u7684\u9879\u76ee\u5bfc\u5165\u9879\u3002\n"
"\u6ce8\u610f\uff0c\u5f53\u7f3a\u5931\u7684\u5bfc\u5165\u9879\u65e0\u6cd5\u5728\u8be5\u73af\u5883\u5b89\u88c5\u65f6\uff0c\u4e0d\u4f1a\u6709\u9519\u8bef\u63d0\u793a\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.uiPushButton_install_missings.setText(QCoreApplication.translate("imports_check", u"\u4e00\u952e\u5b89\u88c5", None))
#if QT_CONFIG(tooltip)
        self.uiPushButton_confirm.setToolTip(QCoreApplication.translate("imports_check", u"\u4ec0\u4e48\u90fd\u4e0d\u505a\uff0c\u5173\u95ed\u7a97\u53e3\u5e76\u8fd4\u56de\u3002", None))
#endif // QT_CONFIG(tooltip)
        self.uiPushButton_confirm.setText(QCoreApplication.translate("imports_check", u"\u786e\u5b9a", None))
    # retranslateUi


# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'pyinstaller_tool.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_pyinstaller_tool(object):
    def setupUi(self, pyinstaller_tool):
        if not pyinstaller_tool.objectName():
            pyinstaller_tool.setObjectName("pyinstaller_tool")
        pyinstaller_tool.setWindowModality(Qt.WindowModal)
        pyinstaller_tool.resize(686, 655)
        font = QFont()
        font.setFamily("Microsoft YaHei UI")
        pyinstaller_tool.setFont(font)
        self.centralwidget = QWidget(pyinstaller_tool)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_37 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_37.setObjectName("horizontalLayout_37")
        self.horizontalLayout_37.setContentsMargins(8, 8, 8, 8)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_project_files = QWidget()
        self.tab_project_files.setObjectName("tab_project_files")
        self.verticalLayout_28 = QVBoxLayout(self.tab_project_files)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setSpacing(2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QLabel(self.tab_project_files)
        self.label.setObjectName("label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.le_program_entry_old = QLineEdit(self.tab_project_files)
        self.le_program_entry_old.setObjectName("le_program_entry_old")

        self.horizontalLayout_3.addWidget(self.le_program_entry_old)

        self.pb_select_program_entry = QPushButton(self.tab_project_files)
        self.pb_select_program_entry.setObjectName("pb_select_program_entry")

        self.horizontalLayout_3.addWidget(self.pb_select_program_entry)

        self.horizontalLayout_3.setStretch(0, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout_28.addLayout(self.verticalLayout_2)

        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setSpacing(2)
        self.verticalLayout_19.setObjectName("verticalLayout_19")
        self.label_13 = QLabel(self.tab_project_files)
        self.label_13.setObjectName("label_13")

        self.verticalLayout_19.addWidget(self.label_13)

        self.le_output_name = QLineEdit(self.tab_project_files)
        self.le_output_name.setObjectName("le_output_name")

        self.verticalLayout_19.addWidget(self.le_output_name)

        self.verticalLayout_28.addLayout(self.verticalLayout_19)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_2 = QLabel(self.tab_project_files)
        self.label_2.setObjectName("label_2")

        self.horizontalLayout_20.addWidget(self.label_2)

        self.pb_reset_root_level = QPushButton(self.tab_project_files)
        self.pb_reset_root_level.setObjectName("pb_reset_root_level")

        self.horizontalLayout_20.addWidget(self.pb_reset_root_level)

        self.pb_up_level_root = QPushButton(self.tab_project_files)
        self.pb_up_level_root.setObjectName("pb_up_level_root")

        self.horizontalLayout_20.addWidget(self.pb_up_level_root)

        self.horizontalLayout_20.setStretch(0, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_20)

        self.le_project_root = QLineEdit(self.tab_project_files)
        self.le_project_root.setObjectName("le_project_root")
        self.le_project_root.setReadOnly(True)

        self.verticalLayout.addWidget(self.le_project_root)

        self.verticalLayout_28.addLayout(self.verticalLayout)

        self.verticalLayout_29 = QVBoxLayout()
        self.verticalLayout_29.setSpacing(2)
        self.verticalLayout_29.setObjectName("verticalLayout_29")
        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName("horizontalLayout_34")
        self.label_31 = QLabel(self.tab_project_files)
        self.label_31.setObjectName("label_31")

        self.horizontalLayout_34.addWidget(self.label_31)

        self.horizontalLayout_34.setStretch(0, 1)

        self.verticalLayout_29.addLayout(self.horizontalLayout_34)

        self.uiLineEdit_program_root = QLineEdit(self.tab_project_files)
        self.uiLineEdit_program_root.setObjectName("uiLineEdit_program_root")
        self.uiLineEdit_program_root.setToolTipDuration(60000)
        self.uiLineEdit_program_root.setReadOnly(True)

        self.verticalLayout_29.addWidget(self.uiLineEdit_program_root)

        self.verticalLayout_28.addLayout(self.verticalLayout_29)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName("horizontalLayout_31")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setSpacing(2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_26 = QLabel(self.tab_project_files)
        self.label_26.setObjectName("label_26")

        self.horizontalLayout_19.addWidget(self.label_26)

        self.pb_clear_hidden_imports = QPushButton(self.tab_project_files)
        self.pb_clear_hidden_imports.setObjectName("pb_clear_hidden_imports")

        self.horizontalLayout_19.addWidget(self.pb_clear_hidden_imports)

        self.horizontalLayout_19.setStretch(0, 1)

        self.verticalLayout_5.addLayout(self.horizontalLayout_19)

        self.pte_hidden_imports = QPlainTextEdit(self.tab_project_files)
        self.pte_hidden_imports.setObjectName("pte_hidden_imports")
        self.pte_hidden_imports.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.verticalLayout_5.addWidget(self.pte_hidden_imports)

        self.horizontalLayout_31.addLayout(self.verticalLayout_5)

        self.verticalLayout_17 = QVBoxLayout()
        self.verticalLayout_17.setSpacing(2)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_27 = QLabel(self.tab_project_files)
        self.label_27.setObjectName("label_27")

        self.horizontalLayout_21.addWidget(self.label_27)

        self.pb_clear_exclude_module = QPushButton(self.tab_project_files)
        self.pb_clear_exclude_module.setObjectName("pb_clear_exclude_module")

        self.horizontalLayout_21.addWidget(self.pb_clear_exclude_module)

        self.horizontalLayout_21.setStretch(0, 1)

        self.verticalLayout_17.addLayout(self.horizontalLayout_21)

        self.pte_exclude_modules = QPlainTextEdit(self.tab_project_files)
        self.pte_exclude_modules.setObjectName("pte_exclude_modules")
        self.pte_exclude_modules.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.verticalLayout_17.addWidget(self.pte_exclude_modules)

        self.horizontalLayout_31.addLayout(self.verticalLayout_17)

        self.verticalLayout_28.addLayout(self.horizontalLayout_31)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setSpacing(2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QLabel(self.tab_project_files)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout_5.addWidget(self.label_3)

        self.pb_clear_module_search_path = QPushButton(self.tab_project_files)
        self.pb_clear_module_search_path.setObjectName("pb_clear_module_search_path")

        self.horizontalLayout_5.addWidget(self.pb_clear_module_search_path)

        self.pb_select_module_search_path = QPushButton(self.tab_project_files)
        self.pb_select_module_search_path.setObjectName("pb_select_module_search_path")

        self.horizontalLayout_5.addWidget(self.pb_select_module_search_path)

        self.horizontalLayout_5.setStretch(0, 1)

        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.te_module_search_path_old = QTextEdit(self.tab_project_files)
        self.te_module_search_path_old.setObjectName("te_module_search_path_old")

        self.verticalLayout_3.addWidget(self.te_module_search_path_old)

        self.verticalLayout_28.addLayout(self.verticalLayout_3)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_4 = QLabel(self.tab_project_files)
        self.label_4.setObjectName("label_4")

        self.horizontalLayout_6.addWidget(self.label_4)

        self.pb_clear_other_data = QPushButton(self.tab_project_files)
        self.pb_clear_other_data.setObjectName("pb_clear_other_data")

        self.horizontalLayout_6.addWidget(self.pb_clear_other_data)

        self.pb_select_other_data = QPushButton(self.tab_project_files)
        self.pb_select_other_data.setObjectName("pb_select_other_data")

        self.horizontalLayout_6.addWidget(self.pb_select_other_data)

        self.horizontalLayout_6.setStretch(0, 1)

        self.verticalLayout_4.addLayout(self.horizontalLayout_6)

        self.te_other_data_old = QTextEdit(self.tab_project_files)
        self.te_other_data_old.setObjectName("te_other_data_old")

        self.verticalLayout_4.addWidget(self.te_other_data_old)

        self.verticalLayout_28.addLayout(self.verticalLayout_4)

        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setSpacing(2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_7 = QLabel(self.tab_project_files)
        self.label_7.setObjectName("label_7")

        self.verticalLayout_8.addWidget(self.label_7)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.le_file_icon_path_old = QLineEdit(self.tab_project_files)
        self.le_file_icon_path_old.setObjectName("le_file_icon_path_old")

        self.horizontalLayout_11.addWidget(self.le_file_icon_path_old)

        self.pb_select_file_icon = QPushButton(self.tab_project_files)
        self.pb_select_file_icon.setObjectName("pb_select_file_icon")

        self.horizontalLayout_11.addWidget(self.pb_select_file_icon)

        self.horizontalLayout_11.setStretch(0, 1)

        self.verticalLayout_8.addLayout(self.horizontalLayout_11)

        self.verticalLayout_28.addLayout(self.verticalLayout_8)

        self.tabWidget.addTab(self.tab_project_files, "")
        self.tab_build_control = QWidget()
        self.tab_build_control.setObjectName("tab_build_control")
        self.verticalLayout_14 = QVBoxLayout(self.tab_build_control)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.rb_pack_to_one_dir = QRadioButton(self.tab_build_control)
        self.rb_pack_to_one_dir.setObjectName("rb_pack_to_one_dir")

        self.horizontalLayout_9.addWidget(self.rb_pack_to_one_dir)

        self.rb_pack_to_one_file = QRadioButton(self.tab_build_control)
        self.rb_pack_to_one_file.setObjectName("rb_pack_to_one_file")

        self.horizontalLayout_9.addWidget(self.rb_pack_to_one_file)

        self.verticalLayout_12.addLayout(self.horizontalLayout_9)

        self.cb_execute_with_console = QCheckBox(self.tab_build_control)
        self.cb_execute_with_console.setObjectName("cb_execute_with_console")

        self.verticalLayout_12.addWidget(self.cb_execute_with_console)

        self.cb_without_confirm = QCheckBox(self.tab_build_control)
        self.cb_without_confirm.setObjectName("cb_without_confirm")

        self.verticalLayout_12.addWidget(self.cb_without_confirm)

        self.cb_use_upx = QCheckBox(self.tab_build_control)
        self.cb_use_upx.setObjectName("cb_use_upx")

        self.verticalLayout_12.addWidget(self.cb_use_upx)

        self.cb_clean_before_build = QCheckBox(self.tab_build_control)
        self.cb_clean_before_build.setObjectName("cb_clean_before_build")

        self.verticalLayout_12.addWidget(self.cb_clean_before_build)

        self.cb_write_info_to_exec = QCheckBox(self.tab_build_control)
        self.cb_write_info_to_exec.setObjectName("cb_write_info_to_exec")

        self.verticalLayout_12.addWidget(self.cb_write_info_to_exec)

        self.cb_uac_admin = QCheckBox(self.tab_build_control)
        self.cb_uac_admin.setObjectName("cb_uac_admin")

        self.verticalLayout_12.addWidget(self.cb_uac_admin)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_11 = QLabel(self.tab_build_control)
        self.label_11.setObjectName("label_11")

        self.horizontalLayout_15.addWidget(self.label_11)

        self.le_bytecode_encryption_key = QLineEdit(self.tab_build_control)
        self.le_bytecode_encryption_key.setObjectName("le_bytecode_encryption_key")

        self.horizontalLayout_15.addWidget(self.le_bytecode_encryption_key)

        self.verticalLayout_12.addLayout(self.horizontalLayout_15)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setSpacing(2)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_8 = QLabel(self.tab_build_control)
        self.label_8.setObjectName("label_8")

        self.verticalLayout_9.addWidget(self.label_8)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.le_output_dir = QLineEdit(self.tab_build_control)
        self.le_output_dir.setObjectName("le_output_dir")

        self.horizontalLayout_12.addWidget(self.le_output_dir)

        self.pb_select_output_dir = QPushButton(self.tab_build_control)
        self.pb_select_output_dir.setObjectName("pb_select_output_dir")

        self.horizontalLayout_12.addWidget(self.pb_select_output_dir)

        self.verticalLayout_9.addLayout(self.horizontalLayout_12)

        self.verticalLayout_12.addLayout(self.verticalLayout_9)

        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setSpacing(2)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.label_17 = QLabel(self.tab_build_control)
        self.label_17.setObjectName("label_17")

        self.verticalLayout_15.addWidget(self.label_17)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.le_spec_dir = QLineEdit(self.tab_build_control)
        self.le_spec_dir.setObjectName("le_spec_dir")

        self.horizontalLayout_16.addWidget(self.le_spec_dir)

        self.pb_select_spec_dir = QPushButton(self.tab_build_control)
        self.pb_select_spec_dir.setObjectName("pb_select_spec_dir")

        self.horizontalLayout_16.addWidget(self.pb_select_spec_dir)

        self.verticalLayout_15.addLayout(self.horizontalLayout_16)

        self.verticalLayout_12.addLayout(self.verticalLayout_15)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setSpacing(2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_10 = QLabel(self.tab_build_control)
        self.label_10.setObjectName("label_10")

        self.verticalLayout_11.addWidget(self.label_10)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.le_temp_working_dir = QLineEdit(self.tab_build_control)
        self.le_temp_working_dir.setObjectName("le_temp_working_dir")

        self.horizontalLayout_14.addWidget(self.le_temp_working_dir)

        self.pb_select_temp_working_dir = QPushButton(self.tab_build_control)
        self.pb_select_temp_working_dir.setObjectName("pb_select_temp_working_dir")

        self.horizontalLayout_14.addWidget(self.pb_select_temp_working_dir)

        self.verticalLayout_11.addLayout(self.horizontalLayout_14)

        self.verticalLayout_12.addLayout(self.verticalLayout_11)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setSpacing(2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_9 = QLabel(self.tab_build_control)
        self.label_9.setObjectName("label_9")

        self.verticalLayout_10.addWidget(self.label_9)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.le_upx_search_path = QLineEdit(self.tab_build_control)
        self.le_upx_search_path.setObjectName("le_upx_search_path")

        self.horizontalLayout_13.addWidget(self.le_upx_search_path)

        self.pb_select_upx_search_path = QPushButton(self.tab_build_control)
        self.pb_select_upx_search_path.setObjectName("pb_select_upx_search_path")

        self.horizontalLayout_13.addWidget(self.pb_select_upx_search_path)

        self.verticalLayout_10.addLayout(self.horizontalLayout_13)

        self.verticalLayout_12.addLayout(self.verticalLayout_10)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setSpacing(2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.label_14 = QLabel(self.tab_build_control)
        self.label_14.setObjectName("label_14")

        self.verticalLayout_13.addWidget(self.label_14)

        self.te_upx_exclude_files = QTextEdit(self.tab_build_control)
        self.te_upx_exclude_files.setObjectName("te_upx_exclude_files")
        self.te_upx_exclude_files.setAcceptDrops(False)

        self.verticalLayout_13.addWidget(self.te_upx_exclude_files)

        self.verticalLayout_12.addLayout(self.verticalLayout_13)

        self.verticalLayout_14.addLayout(self.verticalLayout_12)

        self.tabWidget.addTab(self.tab_build_control, "")
        self.tab_file_ver_info = QWidget()
        self.tab_file_ver_info.setObjectName("tab_file_ver_info")
        self.verticalLayout_7 = QVBoxLayout(self.tab_file_ver_info)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.label_12 = QLabel(self.tab_file_ver_info)
        self.label_12.setObjectName("label_12")
        self.label_12.setMinimumSize(QSize(90, 0))
        self.label_12.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_23.addWidget(self.label_12)

        self.le_file_description = QLineEdit(self.tab_file_ver_info)
        self.le_file_description.setObjectName("le_file_description")

        self.horizontalLayout_23.addWidget(self.le_file_description)

        self.verticalLayout_7.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_25 = QLabel(self.tab_file_ver_info)
        self.label_25.setObjectName("label_25")
        self.label_25.setMinimumSize(QSize(90, 0))
        self.label_25.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_24.addWidget(self.label_25)

        self.le_company_name = QLineEdit(self.tab_file_ver_info)
        self.le_company_name.setObjectName("le_company_name")

        self.horizontalLayout_24.addWidget(self.le_company_name)

        self.verticalLayout_7.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_19 = QLabel(self.tab_file_ver_info)
        self.label_19.setObjectName("label_19")
        self.label_19.setMinimumSize(QSize(90, 0))
        self.label_19.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_25.addWidget(self.label_19)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.le_file_version_0 = QLineEdit(self.tab_file_ver_info)
        self.le_file_version_0.setObjectName("le_file_version_0")

        self.horizontalLayout_10.addWidget(self.le_file_version_0)

        self.le_file_version_1 = QLineEdit(self.tab_file_ver_info)
        self.le_file_version_1.setObjectName("le_file_version_1")

        self.horizontalLayout_10.addWidget(self.le_file_version_1)

        self.le_file_version_2 = QLineEdit(self.tab_file_ver_info)
        self.le_file_version_2.setObjectName("le_file_version_2")

        self.horizontalLayout_10.addWidget(self.le_file_version_2)

        self.le_file_version_3 = QLineEdit(self.tab_file_ver_info)
        self.le_file_version_3.setObjectName("le_file_version_3")

        self.horizontalLayout_10.addWidget(self.le_file_version_3)

        self.horizontalLayout_25.addLayout(self.horizontalLayout_10)

        self.verticalLayout_7.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_20 = QLabel(self.tab_file_ver_info)
        self.label_20.setObjectName("label_20")
        self.label_20.setMinimumSize(QSize(90, 0))
        self.label_20.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_26.addWidget(self.label_20)

        self.le_product_name = QLineEdit(self.tab_file_ver_info)
        self.le_product_name.setObjectName("le_product_name")

        self.horizontalLayout_26.addWidget(self.le_product_name)

        self.verticalLayout_7.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName("horizontalLayout_27")
        self.label_21 = QLabel(self.tab_file_ver_info)
        self.label_21.setObjectName("label_21")
        self.label_21.setMinimumSize(QSize(90, 0))
        self.label_21.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_27.addWidget(self.label_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.le_product_version_0 = QLineEdit(self.tab_file_ver_info)
        self.le_product_version_0.setObjectName("le_product_version_0")

        self.horizontalLayout_22.addWidget(self.le_product_version_0)

        self.le_product_version_1 = QLineEdit(self.tab_file_ver_info)
        self.le_product_version_1.setObjectName("le_product_version_1")

        self.horizontalLayout_22.addWidget(self.le_product_version_1)

        self.le_product_version_2 = QLineEdit(self.tab_file_ver_info)
        self.le_product_version_2.setObjectName("le_product_version_2")

        self.horizontalLayout_22.addWidget(self.le_product_version_2)

        self.le_product_version_3 = QLineEdit(self.tab_file_ver_info)
        self.le_product_version_3.setObjectName("le_product_version_3")

        self.horizontalLayout_22.addWidget(self.le_product_version_3)

        self.horizontalLayout_27.addLayout(self.horizontalLayout_22)

        self.verticalLayout_7.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName("horizontalLayout_28")
        self.label_22 = QLabel(self.tab_file_ver_info)
        self.label_22.setObjectName("label_22")
        self.label_22.setMinimumSize(QSize(90, 0))
        self.label_22.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_28.addWidget(self.label_22)

        self.le_legal_copyright = QLineEdit(self.tab_file_ver_info)
        self.le_legal_copyright.setObjectName("le_legal_copyright")

        self.horizontalLayout_28.addWidget(self.le_legal_copyright)

        self.verticalLayout_7.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName("horizontalLayout_29")
        self.label_23 = QLabel(self.tab_file_ver_info)
        self.label_23.setObjectName("label_23")
        self.label_23.setMinimumSize(QSize(90, 0))
        self.label_23.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_29.addWidget(self.label_23)

        self.le_legal_trademarks = QLineEdit(self.tab_file_ver_info)
        self.le_legal_trademarks.setObjectName("le_legal_trademarks")

        self.horizontalLayout_29.addWidget(self.le_legal_trademarks)

        self.verticalLayout_7.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName("horizontalLayout_30")
        self.label_24 = QLabel(self.tab_file_ver_info)
        self.label_24.setObjectName("label_24")
        self.label_24.setMinimumSize(QSize(90, 0))
        self.label_24.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.horizontalLayout_30.addWidget(self.label_24)

        self.le_original_filename = QLineEdit(self.tab_file_ver_info)
        self.le_original_filename.setObjectName("le_original_filename")

        self.horizontalLayout_30.addWidget(self.le_original_filename)

        self.verticalLayout_7.addLayout(self.horizontalLayout_30)

        self.verticalSpacer = QSpacerItem(
            20, 373, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.tabWidget.addTab(self.tab_file_ver_info, "")
        self.tab_advanced_setup = QWidget()
        self.tab_advanced_setup.setObjectName("tab_advanced_setup")
        self.verticalLayout_25 = QVBoxLayout(self.tab_advanced_setup)
        self.verticalLayout_25.setObjectName("verticalLayout_25")
        self.verticalLayout_24 = QVBoxLayout()
        self.verticalLayout_24.setObjectName("verticalLayout_24")
        self.groupBox = QGroupBox(self.tab_advanced_setup)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_22 = QVBoxLayout(self.groupBox)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.verticalLayout_21 = QVBoxLayout()
        self.verticalLayout_21.setObjectName("verticalLayout_21")
        self.cb_db_imports = QCheckBox(self.groupBox)
        self.cb_db_imports.setObjectName("cb_db_imports")

        self.verticalLayout_21.addWidget(self.cb_db_imports)

        self.cb_db_bootloader = QCheckBox(self.groupBox)
        self.cb_db_bootloader.setObjectName("cb_db_bootloader")

        self.verticalLayout_21.addWidget(self.cb_db_bootloader)

        self.cb_db_noarchive = QCheckBox(self.groupBox)
        self.cb_db_noarchive.setObjectName("cb_db_noarchive")

        self.verticalLayout_21.addWidget(self.cb_db_noarchive)

        self.verticalLayout_22.addLayout(self.verticalLayout_21)

        self.verticalLayout_24.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.tab_advanced_setup)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_23 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_23.setObjectName("verticalLayout_23")
        self.le_runtime_tmpdir = QLineEdit(self.groupBox_2)
        self.le_runtime_tmpdir.setObjectName("le_runtime_tmpdir")

        self.verticalLayout_23.addWidget(self.le_runtime_tmpdir)

        self.verticalLayout_24.addWidget(self.groupBox_2)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_24.addItem(self.verticalSpacer_2)

        self.verticalLayout_25.addLayout(self.verticalLayout_24)

        self.tabWidget.addTab(self.tab_advanced_setup, "")
        self.tab_pyitool_settings = QWidget()
        self.tab_pyitool_settings.setObjectName("tab_pyitool_settings")
        self.verticalLayout_33 = QVBoxLayout(self.tab_pyitool_settings)
        self.verticalLayout_33.setObjectName("verticalLayout_33")
        self.groupBox_3 = QGroupBox(self.tab_pyitool_settings)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_31 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_31.setObjectName("verticalLayout_31")
        self.verticalLayout_20 = QVBoxLayout()
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.cb_explorer_show = QCheckBox(self.groupBox_3)
        self.cb_explorer_show.setObjectName("cb_explorer_show")

        self.verticalLayout_20.addWidget(self.cb_explorer_show)

        self.cb_delete_spec_file = QCheckBox(self.groupBox_3)
        self.cb_delete_spec_file.setObjectName("cb_delete_spec_file")

        self.verticalLayout_20.addWidget(self.cb_delete_spec_file)

        self.cb_delete_working_dir = QCheckBox(self.groupBox_3)
        self.cb_delete_working_dir.setObjectName("cb_delete_working_dir")

        self.verticalLayout_20.addWidget(self.cb_delete_working_dir)

        self.verticalLayout_31.addLayout(self.verticalLayout_20)

        self.verticalLayout_33.addWidget(self.groupBox_3)

        self.groupBox_4 = QGroupBox(self.tab_pyitool_settings)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_32 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_32.setObjectName("verticalLayout_32")
        self.verticalLayout_32.setContentsMargins(8, 8, 8, 8)
        self.verticalLayout_26 = QVBoxLayout()
        self.verticalLayout_26.setSpacing(2)
        self.verticalLayout_26.setObjectName("verticalLayout_26")
        self.label_28 = QLabel(self.groupBox_4)
        self.label_28.setObjectName("label_28")

        self.verticalLayout_26.addWidget(self.label_28)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName("horizontalLayout_32")
        self.uiLineEdit_config_remark = QLineEdit(self.groupBox_4)
        self.uiLineEdit_config_remark.setObjectName("uiLineEdit_config_remark")

        self.horizontalLayout_32.addWidget(self.uiLineEdit_config_remark)

        self.uiPushButton_save_config = QPushButton(self.groupBox_4)
        self.uiPushButton_save_config.setObjectName("uiPushButton_save_config")

        self.horizontalLayout_32.addWidget(self.uiPushButton_save_config)

        self.verticalLayout_26.addLayout(self.horizontalLayout_32)

        self.verticalLayout_32.addLayout(self.verticalLayout_26)

        self.verticalLayout_30 = QVBoxLayout()
        self.verticalLayout_30.setSpacing(2)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.label_29 = QLabel(self.groupBox_4)
        self.label_29.setObjectName("label_29")

        self.verticalLayout_30.addWidget(self.label_29)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.uiListWidget_saved_config = QListWidget(self.groupBox_4)
        self.uiListWidget_saved_config.setObjectName("uiListWidget_saved_config")

        self.horizontalLayout_7.addWidget(self.uiListWidget_saved_config)

        self.verticalLayout_27 = QVBoxLayout()
        self.verticalLayout_27.setObjectName("verticalLayout_27")
        self.uiPushButton_apply_config = QPushButton(self.groupBox_4)
        self.uiPushButton_apply_config.setObjectName("uiPushButton_apply_config")

        self.verticalLayout_27.addWidget(self.uiPushButton_apply_config)

        self.uiPushButton_delete_config = QPushButton(self.groupBox_4)
        self.uiPushButton_delete_config.setObjectName("uiPushButton_delete_config")
        palette = QPalette()
        brush = QBrush(QColor(255, 0, 0, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.ButtonText, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.uiPushButton_delete_config.setPalette(palette)

        self.verticalLayout_27.addWidget(self.uiPushButton_delete_config)

        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_27.addItem(self.verticalSpacer_4)

        self.horizontalLayout_7.addLayout(self.verticalLayout_27)

        self.verticalLayout_30.addLayout(self.horizontalLayout_7)

        self.verticalLayout_32.addLayout(self.verticalLayout_30)

        self.verticalLayout_33.addWidget(self.groupBox_4)

        self.verticalSpacer_3 = QSpacerItem(
            20, 225, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_33.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tab_pyitool_settings, "")
        self.splitter.addWidget(self.tabWidget)
        self.layoutWidget = QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_16 = QVBoxLayout(self.layoutWidget)
        self.verticalLayout_16.setSpacing(4)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.label_6.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName("horizontalLayout_33")
        self.lb_py_info = QLabel(self.layoutWidget)
        self.lb_py_info.setObjectName("lb_py_info")
        self.lb_py_info.setFrameShape(QFrame.Box)

        self.horizontalLayout_33.addWidget(self.lb_py_info)

        self.pb_select_py_env = QPushButton(self.layoutWidget)
        self.pb_select_py_env.setObjectName("pb_select_py_env")

        self.horizontalLayout_33.addWidget(self.pb_select_py_env)

        self.horizontalLayout_33.setStretch(0, 1)

        self.gridLayout.addLayout(self.horizontalLayout_33, 0, 1, 1, 1)

        self.label_30 = QLabel(self.layoutWidget)
        self.label_30.setObjectName("label_30")
        self.label_30.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_30, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.uiLabel_venv_info = QLabel(self.layoutWidget)
        self.uiLabel_venv_info.setObjectName("uiLabel_venv_info")
        self.uiLabel_venv_info.setFrameShape(QFrame.Box)

        self.horizontalLayout_2.addWidget(self.uiLabel_venv_info)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.uiPushButton_create_venv = QPushButton(self.layoutWidget)
        self.uiPushButton_create_venv.setObjectName("uiPushButton_create_venv")

        self.horizontalLayout.addWidget(self.uiPushButton_create_venv)

        self.uiPushButton_refresh_venv = QPushButton(self.layoutWidget)
        self.uiPushButton_refresh_venv.setObjectName("uiPushButton_refresh_venv")

        self.horizontalLayout.addWidget(self.uiPushButton_refresh_venv)

        self.horizontalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2.setStretch(0, 1)

        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)

        self.cb_prioritize_venv = QCheckBox(self.layoutWidget)
        self.cb_prioritize_venv.setObjectName("cb_prioritize_venv")

        self.gridLayout.addWidget(self.cb_prioritize_venv, 2, 1, 1, 1)

        self.label_16 = QLabel(self.layoutWidget)
        self.label_16.setObjectName("label_16")
        self.label_16.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_16, 3, 0, 1, 1)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName("horizontalLayout_35")
        self.lb_pyi_info = QLabel(self.layoutWidget)
        self.lb_pyi_info.setObjectName("lb_pyi_info")
        self.lb_pyi_info.setFrameShape(QFrame.Box)

        self.horizontalLayout_35.addWidget(self.lb_pyi_info)

        self.pb_reinstall_pyi = QPushButton(self.layoutWidget)
        self.pb_reinstall_pyi.setObjectName("pb_reinstall_pyi")

        self.horizontalLayout_35.addWidget(self.pb_reinstall_pyi)

        self.horizontalLayout_35.setStretch(0, 1)

        self.gridLayout.addLayout(self.horizontalLayout_35, 3, 1, 1, 1)

        self.label_15 = QLabel(self.layoutWidget)
        self.label_15.setObjectName("label_15")
        self.label_15.setAlignment(Qt.AlignRight | Qt.AlignTrailing | Qt.AlignVCenter)

        self.gridLayout.addWidget(self.label_15, 4, 0, 1, 1)

        self.lb_platform_info = QLabel(self.layoutWidget)
        self.lb_platform_info.setObjectName("lb_platform_info")
        self.lb_platform_info.setMinimumSize(QSize(0, 25))
        self.lb_platform_info.setFrameShape(QFrame.Box)

        self.gridLayout.addWidget(self.lb_platform_info, 4, 1, 1, 1)

        self.verticalLayout_16.addLayout(self.gridLayout)

        self.line_5 = QFrame(self.layoutWidget)
        self.line_5.setObjectName("line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_16.addWidget(self.line_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")

        self.horizontalLayout_17.addWidget(self.label_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_18 = QLabel(self.layoutWidget)
        self.label_18.setObjectName("label_18")

        self.horizontalLayout_8.addWidget(self.label_18)

        self.cb_log_level = QComboBox(self.layoutWidget)
        self.cb_log_level.addItem("")
        self.cb_log_level.addItem("")
        self.cb_log_level.addItem("")
        self.cb_log_level.addItem("")
        self.cb_log_level.addItem("")
        self.cb_log_level.addItem("")
        self.cb_log_level.setObjectName("cb_log_level")

        self.horizontalLayout_8.addWidget(self.cb_log_level)

        self.horizontalLayout_17.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_17.setStretch(0, 9)

        self.verticalLayout_6.addLayout(self.horizontalLayout_17)

        self.te_pyi_out_stream = QTextEdit(self.layoutWidget)
        self.te_pyi_out_stream.setObjectName("te_pyi_out_stream")
        font1 = QFont()
        font1.setFamily("Consolas")
        font1.setPointSize(10)
        self.te_pyi_out_stream.setFont(font1)
        self.te_pyi_out_stream.setLineWrapMode(QTextEdit.NoWrap)
        self.te_pyi_out_stream.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.te_pyi_out_stream)

        self.verticalLayout_6.setStretch(1, 1)

        self.verticalLayout_16.addLayout(self.verticalLayout_6)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName("horizontalLayout_36")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.lb_running_gif = QLabel(self.layoutWidget)
        self.lb_running_gif.setObjectName("lb_running_gif")

        self.horizontalLayout_4.addWidget(self.lb_running_gif)

        self.lb_running_tip = QLabel(self.layoutWidget)
        self.lb_running_tip.setObjectName("lb_running_tip")

        self.horizontalLayout_4.addWidget(self.lb_running_tip)

        self.horizontalLayout_4.setStretch(1, 1)

        self.horizontalLayout_36.addLayout(self.horizontalLayout_4)

        self.uiPushButton_clear_log = QPushButton(self.layoutWidget)
        self.uiPushButton_clear_log.setObjectName("uiPushButton_clear_log")

        self.horizontalLayout_36.addWidget(self.uiPushButton_clear_log)

        self.horizontalLayout_36.setStretch(0, 1)

        self.verticalLayout_16.addLayout(self.horizontalLayout_36)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setSpacing(4)
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.pb_check_imports = QPushButton(self.layoutWidget)
        self.pb_check_imports.setObjectName("pb_check_imports")
        self.pb_check_imports.setMinimumSize(QSize(0, 42))
        palette1 = QPalette()
        palette1.setBrush(QPalette.Active, QPalette.ButtonText, brush)
        brush2 = QBrush(QColor(0, 0, 0, 255))
        brush2.setStyle(Qt.SolidPattern)
        palette1.setBrush(QPalette.Inactive, QPalette.ButtonText, brush2)
        palette1.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.pb_check_imports.setPalette(palette1)
        font2 = QFont()
        font2.setFamily("Microsoft YaHei UI")
        font2.setPointSize(10)
        self.pb_check_imports.setFont(font2)

        self.horizontalLayout_18.addWidget(self.pb_check_imports)

        self.uiPushButton_clear_data = QPushButton(self.layoutWidget)
        self.uiPushButton_clear_data.setObjectName("uiPushButton_clear_data")
        self.uiPushButton_clear_data.setMinimumSize(QSize(0, 42))
        palette2 = QPalette()
        brush3 = QBrush(QColor(0, 170, 0, 255))
        brush3.setStyle(Qt.SolidPattern)
        palette2.setBrush(QPalette.Active, QPalette.ButtonText, brush3)
        palette2.setBrush(QPalette.Inactive, QPalette.ButtonText, brush2)
        palette2.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.uiPushButton_clear_data.setPalette(palette2)
        self.uiPushButton_clear_data.setFont(font2)

        self.horizontalLayout_18.addWidget(self.uiPushButton_clear_data)

        self.pb_gen_executable = QPushButton(self.layoutWidget)
        self.pb_gen_executable.setObjectName("pb_gen_executable")
        self.pb_gen_executable.setMinimumSize(QSize(0, 42))
        palette3 = QPalette()
        brush4 = QBrush(QColor(0, 0, 255, 255))
        brush4.setStyle(Qt.SolidPattern)
        palette3.setBrush(QPalette.Active, QPalette.ButtonText, brush4)
        palette3.setBrush(QPalette.Inactive, QPalette.ButtonText, brush2)
        palette3.setBrush(QPalette.Disabled, QPalette.ButtonText, brush1)
        self.pb_gen_executable.setPalette(palette3)
        font3 = QFont()
        font3.setFamily("Microsoft YaHei UI")
        font3.setPointSize(12)
        self.pb_gen_executable.setFont(font3)

        self.horizontalLayout_18.addWidget(self.pb_gen_executable)

        self.horizontalLayout_18.setStretch(0, 3)
        self.horizontalLayout_18.setStretch(1, 2)
        self.horizontalLayout_18.setStretch(2, 5)

        self.verticalLayout_16.addLayout(self.horizontalLayout_18)

        self.splitter.addWidget(self.layoutWidget)

        self.horizontalLayout_37.addWidget(self.splitter)

        pyinstaller_tool.setCentralWidget(self.centralwidget)

        self.retranslateUi(pyinstaller_tool)

        self.tabWidget.setCurrentIndex(0)
        self.cb_log_level.setCurrentIndex(2)

        QMetaObject.connectSlotsByName(pyinstaller_tool)

    # setupUi

    def retranslateUi(self, pyinstaller_tool):
        pyinstaller_tool.setWindowTitle(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u7a0b\u5e8f\u6253\u5305\u5de5\u5177", None
            )
        )
        self.label.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u7a0b\u5e8f\u542f\u52a8\u5165\u53e3\uff1a", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_program_entry_old.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u8981\u6253\u5305\u7684\u7a0b\u5e8f\u7684\u542f\u52a8\u5165\u53e3(*.py *.pyw *.pyc *.spec)\uff0c\u6b64\u9879\u5fc5\u586b\u3002\n"
                "\u5982\u679c\u6307\u5b9a\u4e86SPEC\u6587\u4ef6\uff0c\u5219\u4ee5\u4e0b\u7edd\u5927\u90e8\u5206\u9879\u76ee\u6587\u4ef6\u53ca\u751f\u6210\u63a7\u5236\u90fd\u5c06\u4e0d\u751f\u6548\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_select_program_entry.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u9009\u62e9", None)
        )
        self.label_13.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u540e\u7684\u6587\u4ef6\u540d\uff08\u4e0d\u542b\u540e\u7f00\uff09\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_output_name.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a-n, --name\n"
                "\u6253\u5305\u5b8c\u6210\u540e\u7684 exe \u53ef\u6267\u884c\u6587\u4ef6\u6587\u4ef6\u7684\u540d\u79f0\uff0c\u6b64\u9879\u7559\u7a7a\u5219\u4f7f\u7528\u7a0b\u5e8f\u542f\u52a8\u5165\u53e3\u6587\u4ef6\u540d\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_2.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u9879\u76ee\u6839\u76ee\u5f55\uff1a", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.pb_reset_root_level.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5c06\u9879\u76ee\u6839\u76ee\u5f55\u91cd\u7f6e\u4e3a\u7a0b\u5e8f\u542f\u52a8\u5165\u53e3\u6240\u5728\u76ee\u5f55\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_reset_root_level.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u91cd\u7f6e", None)
        )
        # if QT_CONFIG(tooltip)
        self.pb_up_level_root.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5c06\u9879\u76ee\u6839\u76ee\u5f55\u5411\u4e0a\u79fb\u4e00\u7ea7\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_up_level_root.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u4e0a\u4e00\u7ea7", None)
        )
        # if QT_CONFIG(tooltip)
        self.le_project_root.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u662f\u6307\u5f53\u524d\u7a0b\u5e8f\u9879\u76ee\u7684\u8d77\u59cb\u76ee\u5f55\uff0c\u4e3b\u8981\u7528\u4e8e\u786e\u5b9a\u865a\u62df\u73af\u5883\u7684\u521b\u5efa\u4f4d\u7f6e\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_31.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u7a0b\u5e8f\u6839\u76ee\u5f55\uff1a", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.uiLineEdit_program_root.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u7a0b\u5e8f\u8fd0\u884c\u6240\u9700\u6587\u4ef6\u76ee\u5f55\u7ed3\u6784\u7684\u8d77\u59cb\u76ee\u5f55\uff0c\u9009\u62e9\u7a0b\u5e8f\u542f\u52a8\u5165\u53e3\u6587\u4ef6\u540e\u81ea\u52a8\u786e\u5b9a\u3002\n"
                "\u8f83\u5b8c\u5584\u7684\u9879\u76ee\u901a\u5e38\u4f1a\u5728\u9879\u76ee\u76ee\u5f55\u91cc\u5355\u72ec\u7528\u4e00\u4e2a\u76ee\u5f55\u6765\u5b58\u653e\u7a0b\u5e8f\u6e90\u4ee3\u7801\uff0c\u4ee5\u514d\u9879\u76ee\u5176\u4ed6\u6587\u4ef6\u4e0e\u7a0b\u5e8f\u8fd0\u884c\u76f8\u5173\u6587\u4ef6\u6df7\u6dc6\uff0c\u800c\u6e90\u4ee3\u7801\u7684\u8d77\u59cb\u76ee\u5f55\u5373\u4e3a\u201c\u7a0b\u5e8f\u6839\u76ee\u5f55\u201d\u3002\n"
                "\u7a0b\u5e8f\u6839\u76ee\u5f55\u662f\u201c\u9879\u76ee\u6839\u76ee\u5f55\u201d\u7684\u4e00\u90e8\u5206\uff0c\u4f46\u4e5f\u53ef\u4ee5\u548c\u9879\u76ee\u6839\u76ee\u5f55\u76f8\u540c\uff0c\u89c6\u4f60\u7684\u9879\u76ee\u7ed3\u6784\u800c\u5b9a\u3002\n"
                "\u8bf7\u5c06\u4f60\u7684\u7a0b\u5e8f\u8bbe\u8ba1\u4e3a\u201c\u7a0b\u5e8f\u542f\u52a8\u5165\u53e3\u6587\u4ef6\u201d\u662f\u201c\u7a0b\u5e8f\u6839"
                "\u76ee\u5f55\u201d\u7684\u76f4\u63a5\u5b50\u6587\u4ef6\u4ee5\u4fbf\u9002\u5e94 Pyinstaller\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_26.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u9690\u853d\u7684\u5bfc\u5165\uff1a", None
            )
        )
        self.pb_clear_hidden_imports.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u6e05\u7a7a", None)
        )
        # if QT_CONFIG(tooltip)
        self.pte_hidden_imports.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--hidden-import, --hiddenimport\n"
                "\u67d0\u4e9b\u6a21\u5757\u53ef\u80fd\u4f1a\u88ab\u901a\u8fc7\u9690\u853d\u7684\u65b9\u5f0f\u5bfc\u5165\u5bfc\u81f4 Pyinstaller \u6ca1\u6709\u53d1\u73b0\u5b83\uff0c\u5c06\u6ca1\u6709\u88ab\u53d1\u73b0\u7684\u6a21\u5757\u540d\u586b\u5165\u6b64\u5904\u4ee5\u4f7f Pyinstaller \u4e3b\u52a8\u5305\u542b\u8fd9\u4e9b\u6a21\u5757\u3002\n"
                '\u6bcf\u884c\u4e00\u4e2a\u6a21\u5757\u540d\u79f0\uff0c"\u540d\u79f0"\u662f\u6307 Python \u4ee3\u7801\u4e2d import \u8bed\u53e5\u6240\u4f7f\u7528\u7684\u6a21\u5757\u540d\u79f0\uff0c\u533a\u5206\u5927\u5c0f\u5199\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_27.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6392\u9664\u7684\u6a21\u5757\uff1a", None
            )
        )
        self.pb_clear_exclude_module.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u6e05\u7a7a", None)
        )
        # if QT_CONFIG(tooltip)
        self.pte_exclude_modules.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--exclude-module\n"
                "\u5982\u679c\u60a8\u4e0d\u60f3\u8ba9 Pyinstaller \u6253\u5305\u67d0\u4e9b\u6a21\u5757\uff0c\u5219\u8bf7\u628a\u6a21\u5757\u540d\u79f0\u586b\u5165\u6b64\u5904\uff0c\u6bcf\u884c\u4e00\u4e2a\u3002\n"
                '\u4ee5\u4e0a"\u540d\u79f0"\u662f\u6307 Python \u4ee3\u7801\u4e2d import \u8bed\u53e5\u6240\u4f7f\u7528\u7684\u6a21\u5757\u540d\u79f0\uff0c\u533a\u5206\u5927\u5c0f\u5199\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_3.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5176\u4ed6\u6a21\u5757\u641c\u7d22\u76ee\u5f55\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.pb_clear_module_search_path.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6e05\u7a7a\u5176\u4ed6\u6a21\u5757\u641c\u7d22\u76ee\u5f55\u6587\u672c\u6846\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_clear_module_search_path.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u6e05\u7a7a", None)
        )
        self.pb_select_module_search_path.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u9009\u62e9", None)
        )
        self.label_4.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u975e\u6e90\u4ee3\u7801\u8d44\u6e90\u6587\u4ef6\uff1a",
                None,
            )
        )
        self.pb_clear_other_data.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u6e05\u7a7a", None)
        )
        self.pb_select_other_data.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u9009\u62e9", None)
        )
        self.label_7.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u53ef\u6267\u884c\u6587\u4ef6\u7684\u56fe\u6807\u8def\u5f84\uff1a",
                None,
            )
        )
        self.pb_select_file_icon.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u9009\u62e9", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_project_files),
            QCoreApplication.translate(
                "pyinstaller_tool", "\u9879\u76ee\u6587\u4ef6", None
            ),
        )
        # if QT_CONFIG(tooltip)
        self.rb_pack_to_one_dir.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a-D, --onedir\n"
                "\u5c06\u7a0b\u5e8f\u6253\u5305\u6210\u5355\u6587\u4ef6\u5939\u5f62\u5f0f\uff0cexe \u53ef\u6267\u884c\u7a0b\u5e8f\u5728\u6587\u4ef6\u5939\u7684\u9996\u5c42\u76ee\u5f55\u5185\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rb_pack_to_one_dir.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6253\u5305\u6210\u5355\u76ee\u5f55", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.rb_pack_to_one_file.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1b-F, --onefile\n"
                "\u5c06\u7a0b\u5e8f\u4ee5\u53ca\u6dfb\u52a0\u7684\u5176\u4ed6\u8d44\u6e90\u6587\u4ef6\u6253\u5305\u6210\u5355\u4e00\u6587\u4ef6\u7684\u5f62\u5f0f\uff0c\u542f\u52a8\u901f\u5ea6\u7a0d\u6162\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.rb_pack_to_one_file.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6253\u5305\u6210\u5355\u6587\u4ef6", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_execute_with_console.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u52fe\u9009\u65f6\u5bf9\u5e94\u9009\u9879\uff1a-c, --console, --nowindowed\n"
                "\u4e0d\u52fe\u9009\u65f6\u5bf9\u5e94\u9009\u9879\uff1a-w, --windowed, --noconsole\n"
                "\u6253\u5305\u5b8c\u6210\u540e\u542f\u52a8\u7a0b\u5e8f\u662f\u5426\u663e\u793a\u547d\u4ee4\u884c\u7a97\u53e3\uff0c\u6ce8\u610f\uff0c\u540e\u7f00\u4e3a .pyw \u7684\u7a0b\u5e8f\u542f\u52a8\u5165\u53e3\u6253\u5305\u540e\u4e0d\u663e\u793a\u63a7\u5236\u53f0\uff0c\u6b64\u9879\u8bbe\u7f6e\u5931\u6548\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_execute_with_console.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u7684\u7a0b\u5e8f\u8fd0\u884c\u65f6\u663e\u793a\u63a7\u5236\u53f0",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_without_confirm.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a-y, --noconfirm\n"
                "\u6253\u5305\u65f6\u5982\u679c\u9884\u5b9a\u7684 exe \u6587\u4ef6\u50a8\u5b58\u76ee\u5f55\u4e0d\u4e3a\u7a7a\uff0c\u662f\u6e05\u7a7a\u8be5\u76ee\u5f55\u8fd8\u662f\u4e2d\u65ad\u6253\u5305\u8fc7\u7a0b\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_without_confirm.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u8f93\u51fa\u76ee\u5f55\u4e0d\u4e3a\u7a7a\u65f6\u6e05\u7a7a\u800c\u4e0d\u662f\u4e2d\u65ad",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_use_upx.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u4e0d\u52fe\u9009\u65f6\u5bf9\u5e94\u9009\u9879\uff1a--noupx\n"
                "\u6253\u5305\u8fc7\u7a0b\u4e2d\u662f\u5426\u4f7f\u7528 upx \u5bf9\u6587\u4ef6\u8fdb\u884c\u538b\u7f29\u3002\u6ce8\u610f\uff0c\u67d0\u4e9b\u4e8c\u8fdb\u5236\u6587\u4ef6\u5728\u7ecf\u8fc7 upx \u538b\u7f29\u540e\u53ef\u80fd\u65e0\u6cd5\u6b63\u5e38\u8fd0\u884c\u3002\n"
                "\u4ec5\u5f53\u7cfb\u7edf\u73af\u5883\u53d8\u91cf PATH \u4e2d\u6709 upx \u6240\u5728\u76ee\u5f55\u4fe1\u606f\u6216\u5728\u4ee5\u4e0b\u201cupx \u53ef\u6267\u884c\u6587\u4ef6\u6240\u5728\u76ee\u5f55\u201d\u6307\u5b9a\u4e86 upx \u6240\u5728\u76ee\u5f55\u65f6\uff0c\u6b64\u9879\u8bbe\u7f6e\u624d\u751f\u6548\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_use_upx.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u4f7f\u7528 upx \u5bf9\u6587\u4ef6\u8fdb\u884c\u538b\u7f29",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_clean_before_build.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--clean\n"
                "\u6253\u5305\u524d\u662f\u5426\u6e05\u7a7a Pyinstaller \u751f\u6210\u7684\u4e34\u65f6\u6587\u4ef6\u5939\uff08\u4e34\u65f6\u6587\u4ef6\u53ef\u4f7f\u4e0b\u6b21\u6253\u5305\u52a0\u901f\uff09\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_clean_before_build.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u524d\u6e05\u7406\u7f13\u5b58\u5e76\u5220\u9664\u4e34\u65f6\u6587\u4ef6",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_write_info_to_exec.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--version-file\n"
                '\u52fe\u9009\u6b64\u9009\u9879\u5219\u5c06"\u9644\u52a0\u4fe1\u606f"\u6807\u7b7e\u9875\u4e2d\u7684\u5185\u5bb9\u5199\u5165\u751f\u6210\u7684 exe \u6587\u4ef6\uff0c\u8fd9\u4e9b\u4fe1\u606f\u53ef\u4ee5\u5728\u67e5\u770b exe \u6587\u4ef6\u5c5e\u6027\u65f6\u770b\u89c1\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_write_info_to_exec.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5c06\u201c\u9644\u52a0\u4fe1\u606f\u201d\u6807\u7b7e\u9875\u7684\u5185\u5bb9\u5199\u5165\u751f\u6210\u7684\u53ef\u6267\u884c\u6587\u4ef6",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_uac_admin.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--uac-admin\n"
                "\u4f7f\u6253\u5305\u7684 exe \u7a0b\u5e8f\u542f\u52a8\u65f6\u8bf7\u6c42\u63d0\u5347\u6743\u9650\uff0c\u6253\u5305\u9700\u8981\u7ba1\u7406\u5458\u6743\u9650\u624d\u80fd\u6b63\u5e38\u5de5\u4f5c\u7684\u7a0b\u5e8f\u65f6\uff0c\u8bf7\u52fe\u9009\u6b64\u9009\u9879\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_uac_admin.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u7684\u7a0b\u5e8f\u542f\u52a8\u65f6\u8bf7\u6c42\u63d0\u5347\u6743\u9650",
                None,
            )
        )
        self.label_11.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5b57\u8282\u7801\u52a0\u5bc6\u79d8\u94a5\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_bytecode_encryption_key.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--key\n"
                "\u7528\u4e8e\u52a0\u5bc6 Python \u5b57\u8282\u7801\u7684\u5bc6\u94a5\uff0c\u6b64\u9879\u53ef\u7559\u7a7a\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_8.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u540e\u7684\u6587\u4ef6\u50a8\u5b58\u4f4d\u7f6e\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_output_dir.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--distpath\n"
                '\u6b64\u9879\u53ef\u7559\u7a7a\uff0c\u9ed8\u8ba4\u50a8\u5b58\u4f4d\u7f6e\uff1a"\u6e90\u4ee3\u7801\u6839\u76ee\u5f55/dist"\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_select_output_dir.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u9009\u62e9", None)
        )
        self.label_17.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "spec \u6587\u4ef6\u50a8\u5b58\u4f4d\u7f6e\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_spec_dir.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--specpath\n"
                '\u6b64\u9879\u53ef\u7559\u7a7a\uff0c\u9ed8\u8ba4\u50a8\u5b58\u4f4d\u7f6e\uff1a"\u6e90\u4ee3\u7801\u6839\u76ee\u5f55"\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_select_spec_dir.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u9009\u62e9", None)
        )
        self.label_10.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u4e34\u65f6\u5de5\u4f5c\u76ee\u5f55\u6240\u5728\u4f4d\u7f6e\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_temp_working_dir.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--workpath\n"
                '\u6b64\u9879\u53ef\u7559\u7a7a\uff0c\u9ed8\u8ba4\u76ee\u5f55\uff1a"\u6e90\u4ee3\u7801\u6839\u76ee\u5f55/build"\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_select_temp_working_dir.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u9009\u62e9", None)
        )
        self.label_9.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "upx \u53ef\u6267\u884c\u6587\u4ef6\u6240\u5728\u76ee\u5f55\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_upx_search_path.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--upx-dir\n"
                "\u6b64\u9879\u53ef\u7559\u7a7a\uff0c\u627e\u4e0d\u5230 upx \u65f6\u5c06\u4e0d\u8fdb\u884c\u538b\u7f29\u3002\u5f53\u7cfb\u7edf\u73af\u5883\u53d8\u91cf PATH \u4e2d\u6709 upx \u8def\u5f84\u65f6\uff0c\u4e0d\u9700\u8981\u6307\u5b9a\u6b64\u9009\u9879\u4e5f\u53ef\u4f7f\u7528 upx\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_select_upx_search_path.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u9009\u62e9", None)
        )
        self.label_14.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "upx \u538b\u7f29\u65f6\u6392\u9664\u7684\u6587\u4ef6\u540d\uff1a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.te_upx_exclude_files.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--upx-exclude\n"
                "\u4f7f\u7528 upx \u8fdb\u884c\u538b\u7f29\u65f6\u9700\u8981\u5ffd\u7565\u7684\u6587\u4ef6\uff0c\u6bcf\u884c\u4e00\u4e2a\u4e0d\u542b\u8def\u5f84\u7684\u6587\u4ef6\u540d\u3002\n"
                "\u67d0\u4e9b\u4e8c\u8fdb\u5236\u6587\u4ef6\u7ecf\u8fc7 upx \u538b\u7f29\u540e\u53ef\u80fd\u65e0\u6cd5\u8fd0\u884c\uff0c\u53ef\u5c06\u8fd9\u4e9b\u6587\u4ef6\u540d\u6dfb\u52a0\u5230\u6b64\u5904\u4ee5\u4f7f upx \u5728\u538b\u7f29\u65f6\u7565\u8fc7\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_build_control),
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6253\u5305\u63a7\u5236", None
            ),
        )
        # if QT_CONFIG(tooltip)
        self.tab_file_ver_info.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                '\u9700\u8981\u5728"\u751f\u6210\u63a7\u5236"\u4e2d\u52fe\u9009"\u5c06\u6587\u4ef6\u4fe1\u606f\u5199\u5165\u751f\u6210\u7684\u53ef\u6267\u884c\u6587\u4ef6"\uff0c\u6b64\u8bbe\u7f6e\u624d\u751f\u6548\u3002\n'
                "\u751f\u6210\u7684\u53ef\u6267\u884c\u6587\u4ef6\u7684\u9644\u52a0\u4fe1\u606f\uff0c\u5373\u9f20\u6807\u60ac\u505c\u4e8eexe\u6587\u4ef6\u4e0a\u663e\u793a\u7684\u4fe1\u606f\uff0c\u4ee5\u53caexe\u6587\u4ef6\u5c5e\u6027\u4e2d\u7684\u8be6\u7ec6\u4fe1\u606f\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_12.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6587\u4ef6\u8bf4\u660e\uff1a", None
            )
        )
        self.label_25.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u516c\u53f8\uff1a", None)
        )
        self.label_19.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6587\u4ef6\u7248\u672c\uff1a", None
            )
        )
        self.label_20.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u4ea7\u54c1\u540d\u79f0\uff1a", None
            )
        )
        self.label_21.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u4ea7\u54c1\u7248\u672c\uff1a", None
            )
        )
        self.label_22.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u7248\u6743\uff1a", None)
        )
        self.label_23.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u5408\u6cd5\u5546\u6807\uff1a", None
            )
        )
        self.label_24.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u539f\u59cb\u6587\u4ef6\u540d\uff1a", None
            )
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_file_ver_info),
            QCoreApplication.translate(
                "pyinstaller_tool", "\u9644\u52a0\u4fe1\u606f", None
            ),
        )
        self.groupBox.setTitle(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u4ee5\u8c03\u8bd5\u6a21\u5f0f\u6253\u5305\u7a0b\u5e8f",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_db_imports.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a-d {imports}, --debug {imports}\n"
                "\u6bcf\u6b21\u521d\u59cb\u5316\u6a21\u5757\u65f6\uff0c\u6253\u5370\u4e00\u6761\u6d88\u606f\uff0c\u663e\u793a\u52a0\u8f7d\u8be5\u6a21\u5757\u7684\u4f4d\u7f6e(\u6587\u4ef6\u540d\u6216\u5185\u7f6e\u6a21\u5757)\u3002\n"
                '\u8981\u6c42\u6e90\u4ee3\u7801\u6587\u4ef6\u540e\u7f00\u540d\u4e0d\u80fd\u662f *.pyw\uff0c"\u751f\u6210\u63a7\u5236"\u6807\u7b7e\u4e2d\u7684"\u6253\u5305\u7684\u7a0b\u5e8f\u8fd0\u884c\u65f6\u663e\u793a\u63a7\u5236\u53f0"\u9009\u9879\u5fc5\u987b\u52fe\u9009\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_db_imports.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u8fd0\u884c\u65f6\u8f93\u51fa\u6a21\u5757\u5bfc\u5165\u4fe1\u606f",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_db_bootloader.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a-d {bootloader}, --debug {bootloader}\n"
                "\u4f7f\u5f15\u5bfc\u7a0b\u5e8f\u5728\u521d\u59cb\u5316\u548c\u542f\u52a8\u6346\u7ed1\u7684\u5e94\u7528\u7a0b\u5e8f\u65f6\u53d1\u51fa\u8fdb\u5ea6\u6d88\u606f\uff0c\u7528\u4e8e\u8bca\u65ad\u5bfc\u5165\u4e22\u5931\u7684\u95ee\u9898\u3002\n"
                '\u8981\u6c42\u6e90\u4ee3\u7801\u6587\u4ef6\u540e\u7f00\u540d\u4e0d\u80fd\u662f *.pyw\uff0c"\u751f\u6210\u63a7\u5236"\u6807\u7b7e\u4e2d\u7684"\u6253\u5305\u7684\u7a0b\u5e8f\u8fd0\u884c\u65f6\u663e\u793a\u63a7\u5236\u53f0"\u9009\u9879\u5fc5\u987b\u52fe\u9009\u3002',
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_db_bootloader.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u8fd0\u884c\u65f6\u8f93\u51fa\u5f15\u5bfc\u8fdb\u5ea6\u4fe1\u606f",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_db_noarchive.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a-d {noarchive}, --debug {noarchive}\n"
                "\u4e0d\u5c06\u6240\u6709\u51bb\u7ed3\u7684\u6e90\u4ee3\u7801\u6587\u4ef6\u5b58\u6863\u5728\u751f\u6210\u7684\u53ef\u6267\u884c\u6587\u4ef6\u4e2d\uff0c\u800c\u662f\u5c06\u5b83\u4eec\u4f5c\u4e3a\u5355\u72ec\u7684\u6587\u4ef6\u5b58\u50a8\u5728\u751f\u6210\u7684\u8f93\u51fa\u76ee\u5f55\u4e2d\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_db_noarchive.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u4e0d\u5c06\u6e90\u6587\u4ef6\u5b58\u6863\u81f3\u53ef\u6267\u884c\u6587\u4ef6\u4e2d",
                None,
            )
        )
        self.groupBox_2.setTitle(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u5355\u6587\u4ef6\u8fd0\u884c\u65f6\u4e34\u65f6\u76ee\u5f55",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.le_runtime_tmpdir.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--runtime-tmpdir\n"
                '\u4ee5"\u5355\u6587\u4ef6"\u6a21\u5f0f\u6253\u5305\u7684\u7a0b\u5e8f\u8fd0\u884c\u65f6\u63d0\u53d6\u7684\u5e93\u548c\u652f\u6301\u6587\u4ef6\u7684\u4e34\u65f6\u50a8\u5b58\u4f4d\u7f6e\u3002\n'
                '\u5982\u679c\u6307\u5b9a\u4e86\u6b64\u9009\u9879\uff0c\u5219\u5f15\u5bfc\u52a0\u8f7d\u7a0b\u5e8f\u5c06\u5ffd\u7565\u8fd0\u884c\u65f6\u64cd\u4f5c\u7cfb\u7edf\u5b9a\u4e49\u7684\u4efb\u4f55\u4e34\u65f6\u6587\u4ef6\u5939\u4f4d\u7f6e\uff0c"_MEIxxxxxx"\u6587\u4ef6\u5939\u5c06\u5728\u60a8\u6307\u5b9a\u7684\u4f4d\u7f6e\u521b\u5efa\u3002\n'
                "\u4ec5\u5f53\u60a8\u77e5\u9053\u81ea\u5df1\u5728\u505a\u4ec0\u4e48\u65f6\uff0c\u624d\u4f7f\u7528\u6b64\u9009\u9879\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_advanced_setup),
            QCoreApplication.translate(
                "pyinstaller_tool", "\u9ad8\u7ea7\u8bbe\u7f6e", None
            ),
        )
        self.groupBox_3.setTitle(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u6210\u529f\u540e\u6267\u884c...",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_explorer_show.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u6210\u529f\u540e\u6253\u5f00\u8d44\u6e90\u7ba1\u7406\u5668\u5e76\u9009\u4e2d\u6253\u5305\u597d\u7684 .exe \u6587\u4ef6\uff0c\u5982\u679c\u6253\u5305\u5931\u8d25\u5219\u4e0d\u4f1a\u6253\u5f00\u8d44\u6e90\u7ba1\u7406\u5668\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_explorer_show.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5728\u8d44\u6e90\u7ba1\u7406\u5668\u4e2d\u663e\u793a",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_delete_spec_file.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u6210\u529f\u540e\u5220\u9664 Pyinstaller \u751f\u6210\u7684 .spec \u6587\u4ef6\uff0c\u6253\u5305\u5931\u8d25\u5219\u4e0d\u4f1a\u6267\u884c\u5220\u9664\u64cd\u4f5c\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_delete_spec_file.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u5220\u9664 spec \u6587\u4ef6", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.cb_delete_working_dir.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u6210\u529f\u540e\u5220\u9664\u4e34\u65f6\u5de5\u4f5c\u6587\u4ef6\u5939\uff0c\u6253\u5305\u5931\u8d25\u5219\u4e0d\u4f1a\u6267\u884c\u5220\u9664\u64cd\u4f5c\u3002\n"
                "\u5982\u679c\u4f60\u6ca1\u6709\u81ea\u5b9a\u4e49\u4e34\u65f6\u5de5\u4f5c\u76ee\u5f55\u6240\u5728\u76ee\u5f55\uff0c\u5219\u4e34\u65f6\u5de5\u4f5c\u76ee\u5f55\u6307\u7684\u5c31\u662f\u6e90\u4ee3\u7801\u6839\u76ee\u5f55\u4e0b\u7684 build \u76ee\u5f55\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_delete_working_dir.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5220\u9664\u4e34\u65f6\u5de5\u4f5c\u6587\u4ef6\u5939",
                None,
            )
        )
        self.groupBox_4.setTitle(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6253\u5305\u914d\u7f6e\u7ba1\u7406", None
            )
        )
        self.label_28.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u4fdd\u5b58\u5f53\u524d\u6253\u5305\u914d\u7f6e\uff08\u70b9\u51fb\u4e0b\u65b9\u5217\u8868\u4e2d\u7684\u6761\u76ee\u53ef\u5feb\u901f\u586b\u5145\u540d\u79f0\uff09",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.uiLineEdit_config_remark.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5f53\u524d\u6253\u5305\u914d\u7f6e\u662f\u6307\u7a0b\u5e8f\u6253\u5305\u5de5\u5177\u6240\u6709\u590d\u9009\u6846\u3001\u8f93\u5165\u6846\u7b49\u63a7\u4ef6\u7684\u72b6\u6001\u3001\u5185\u5bb9\u3002\n"
                "\u8f93\u5165\u5907\u6ce8\u540d\u79f0\u5e76\u70b9\u51fb\u201c\u4fdd\u5b58\u201d\u6309\u94ae\u5c06\u8fd9\u4e9b\u8bbe\u7f6e\u4fdd\u5b58\u4e0b\u6765\u4ee5\u4fbf\u5728\u6253\u5305\u4e0d\u540c\u9879\u76ee\u65f6\u5feb\u901f\u5207\u6362\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiLineEdit_config_remark.setPlaceholderText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u9ed8\u8ba4\u5907\u6ce8\u540d\u79f0", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.uiPushButton_save_config.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u4ee5\u5de6\u4fa7\u8f93\u5165\u6846\u5185\u5bb9\u4f5c\u4e3a\u540d\u79f0\uff0c\u5c06\u6253\u5305\u5de5\u5177\u7684\u590d\u9009\u6846\u3001\u8f93\u5165\u6846\u7b49\u63a7\u4ef6\u7684\u72b6\u6001\u3001\u5185\u5bb9\u4fdd\u5b58\u4e0b\u6765\u3002\n"
                "\u5982\u679c\u5de6\u4fa7\u8f93\u5165\u6846\u4e0d\u8f93\u5165\u4efb\u4f55\u5185\u5bb9\uff0c\u5219\u4f7f\u7528\u9ed8\u8ba4\u540d\u79f0\u6765\u4fdd\u5b58\u914d\u7f6e\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiPushButton_save_config.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u4fdd\u5b58", None)
        )
        self.label_29.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5df2\u4fdd\u5b58\u7684\u6253\u5305\u914d\u7f6e",
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.uiListWidget_saved_config.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6240\u6709\u5df2\u4fdd\u5b58\u7684\u914d\u7f6e\uff0c\u8fd9\u91cc\u663e\u793a\u7684\u662f\u4f60\u5728\u4fdd\u5b58\u914d\u7f6e\u65f6\u8f93\u5165\u7684\u5907\u6ce8\u540d\u79f0\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.uiPushButton_apply_config.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u590d\u5236\u4e00\u4efd\u6253\u5305\u914d\u7f6e\u5217\u8868\u4e2d\u88ab\u9009\u4e2d\u7684\u914d\u7f6e\uff0c\u5c06\u5b83\u4f5c\u4e3a\u5f53\u524d\u914d\u7f6e\u5e76\u66f4\u65b0\u5230\u6253\u5305\u5de5\u5177\u7684\u754c\u9762\u4e0a\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiPushButton_apply_config.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u5e94\u7528", None)
        )
        # if QT_CONFIG(tooltip)
        self.uiPushButton_delete_config.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5c06\u5de6\u4fa7\u914d\u7f6e\u5217\u8868\u4e2d\u5df2\u88ab\u9009\u4e2d\u7684\u914d\u7f6e\u5220\u9664\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiPushButton_delete_config.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u5220\u9664", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.tab_pyitool_settings),
            QCoreApplication.translate(
                "pyinstaller_tool", "\u5de5\u5177\u8bbe\u7f6e", None
            ),
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u4e3b\u8981\u73af\u5883", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.lb_py_info.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5f53\u524d\u9009\u62e9\u7684 Python \u73af\u5883\u7684\u7248\u672c\u4fe1\u606f\u3002\n"
                "\u9009\u62e9\u4e0d\u540c Python \u73af\u5883\u65f6\uff0c\u5728\u8be5\u73af\u5883\u4e2d\u4e5f\u5e94\u5b89\u88c5\u8fd0\u884c\u9879\u76ee\u6240\u9700\u7684\u6240\u6709\u6a21\u5757\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.pb_select_py_env.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u9009\u62e9\u5728\u4e0d\u540c Python \u73af\u5883\u4e2d\u5c06\u7a0b\u5e8f\u6253\u5305\u6210\u53ef\u6267\u884c\u6587\u4ef6\u3002\n"
                "\u9009\u62e9\u4e0d\u540c Python \u73af\u5883\u65f6\uff0c\u5728\u8be5\u73af\u5883\u4e2d\u4e5f\u5e94\u5b89\u88c5\u8fd0\u884c\u9879\u76ee\u6240\u9700\u7684\u6240\u6709\u6a21\u5757\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_select_py_env.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u9009\u62e9\u73af\u5883", None
            )
        )
        self.label_30.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u865a\u62df\u73af\u5883", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.uiLabel_venv_info.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6b64\u5904\u7684\u201c\u865a\u62df\u73af\u5883\u201d\u4ec5\u6307\u5728\u4f60\u7684\u9879\u76ee\u76ee\u5f55\u4e0b\u521b\u5efa\u7684 Python \u73af\u5883\uff0c\u800c\u975e\u6240\u6709\u5e7f\u4e49\u4e0a\u7684\u865a\u62df\u73af\u5883\u3002\n"
                "\u6ce8\u610f\uff1a\u521b\u5efa\u73af\u5883\u540e\u8bf7\u52ff\u5bf9\u73af\u5883\u76ee\u5f55\u8fdb\u884c\u91cd\u547d\u540d\u7b49\u64cd\u4f5c\uff0c\u5426\u5219\u53ef\u80fd\u4f1a\u9020\u6210\u8be5\u73af\u5883 Scripts \u76ee\u5f55\u4e0b\u7684\u547d\u4ee4\u65e0\u6cd5\u6267\u884c\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiLabel_venv_info.setText("")
        # if QT_CONFIG(tooltip)
        self.uiPushButton_create_venv.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5728\u9879\u76ee\u6839\u76ee\u5f55\u4e0b\u521b\u5efa\u4e00\u4e2a venv \u865a\u62df\u73af\u5883\u5e76\u5728\u5176\u4e2d\u5b89\u88c5\u4f60\u7684\u7a0b\u5e8f\u7684\u4f9d\u8d56\u3002\n"
                "\u6ce8\u610f\uff1a\u521b\u5efa\u73af\u5883\u540e\u8bf7\u52ff\u5bf9\u73af\u5883\u76ee\u5f55\u8fdb\u884c\u91cd\u547d\u540d\u7b49\u64cd\u4f5c\uff0c\u5426\u5219\u53ef\u80fd\u4f1a\u9020\u6210\u8be5\u73af\u5883 Scripts \u76ee\u5f55\u4e0b\u7684\u547d\u4ee4\u65e0\u6cd5\u6267\u884c\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiPushButton_create_venv.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u521b\u5efa", None)
        )
        # if QT_CONFIG(tooltip)
        self.uiPushButton_refresh_venv.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u91cd\u65b0\u5728\u9879\u76ee\u6839\u76ee\u5f55\u4e0b\u67e5\u627e\u865a\u62df\u73af\u5883\u5e76\u5237\u65b0\u7248\u672c\u4fe1\u606f\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiPushButton_refresh_venv.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u5237\u65b0", None)
        )
        # if QT_CONFIG(tooltip)
        self.cb_prioritize_venv.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u9009\u4e2d\u6b64\u9879\u540e\uff0c\u5c06\u4f7f\u7528\u9879\u76ee\u76ee\u5f55\u4e0b\u7684\u865a\u62df\u73af\u5883\u6765\u6253\u5305\u7a0b\u5e8f\u3002\n"
                "\u5982\u679c\u9879\u76ee\u76ee\u5f55\u4e0b\u6ca1\u6709\u865a\u62df\u73af\u5883\uff0c\u5219\u5f39\u51fa\u83dc\u5355\u8be2\u95ee\uff1a\u4f7f\u7528\u4e3b\u73af\u5883\u3001\u521b\u5efa\u865a\u62df\u73af\u5883\u3001\u53d6\u6d88\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.cb_prioritize_venv.setText(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u4f7f\u7528\u9879\u76ee\u76ee\u5f55\u4e0b\u7684\u865a\u62df\u73af\u5883\u800c\u975e\u4e3b\u8981\u73af\u5883",
                None,
            )
        )
        self.label_16.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6253\u5305\u5de5\u5177", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.lb_pyi_info.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6240\u9009 Python \u73af\u5883\u6216\u9879\u76ee\u865a\u62df\u73af\u5883\u4e0b\u7684 Pyinstaller \u7684\u7248\u672c\u4fe1\u606f\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.pb_reinstall_pyi.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5728\u5f53\u524d\u9009\u62e9\u7684 Python \u73af\u5883\u6216\u865a\u62df\u73af\u5883\u4e2d\u5b89\u88c5/\u91cd\u65b0\u5b89\u88c5 Pyinstaller \u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_reinstall_pyi.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u5b89\u88c5", None)
        )
        self.label_15.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u7cfb\u7edf\u4fe1\u606f", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.lb_platform_info.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u64cd\u4f5c\u7cfb\u7edf\u7684\u7248\u672c\u4fe1\u606f\uff0c\u7531\u5185\u7f6e platform \u6a21\u5757\u63d0\u4f9b\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.label_5.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6253\u5305\u65f6\u5411\u63a7\u5236\u53f0\u8f93\u51fa\u7684\u8be6\u7ec6\u4fe1\u606f\uff0c\u7528\u4e8e\u5206\u6790\u6253\u5305\u65f6\u51fa\u73b0\u7684\u95ee\u9898\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.label_5.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6253\u5305\u4fe1\u606f", None
            )
        )
        self.label_18.setText(
            QCoreApplication.translate("pyinstaller_tool", "\u7ea7\u522b\uff1a", None)
        )
        self.cb_log_level.setItemText(
            0, QCoreApplication.translate("pyinstaller_tool", "TRACE", None)
        )
        self.cb_log_level.setItemText(
            1, QCoreApplication.translate("pyinstaller_tool", "DEBUG", None)
        )
        self.cb_log_level.setItemText(
            2, QCoreApplication.translate("pyinstaller_tool", "INFO", None)
        )
        self.cb_log_level.setItemText(
            3, QCoreApplication.translate("pyinstaller_tool", "WARN", None)
        )
        self.cb_log_level.setItemText(
            4, QCoreApplication.translate("pyinstaller_tool", "ERROR", None)
        )
        self.cb_log_level.setItemText(
            5, QCoreApplication.translate("pyinstaller_tool", "CRITICAL", None)
        )

        # if QT_CONFIG(tooltip)
        self.cb_log_level.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5bf9\u5e94\u9009\u9879\uff1a--log-level\n"
                "\u6253\u5305\u7a0b\u5e8f\u65f6\u8f93\u51fa\u7684\u4fe1\u606f\u91cf\uff0c\u9009\u62e9\u8d8a\u9760\u524d\u7684\u9009\u9879\u8f93\u51fa\u7684\u4fe1\u606f\u91cf\u8d8a\u5927\uff0c\u9ed8\u8ba4INFO\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(tooltip)
        self.uiPushButton_clear_log.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6e05\u7a7a\u4e0a\u65b9\u7684\u6253\u5305\u4fe1\u606f\uff0c\u6b64\u64cd\u4f5c\u4e0d\u4f1a\u5f71\u54cd\u6253\u5305\u8fc7\u7a0b\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiPushButton_clear_log.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6e05\u7a7a\u4fe1\u606f", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.pb_check_imports.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u68c0\u67e5\u7a0b\u5e8f\u8fd0\u884c\u6240\u9700\u7684\u6240\u6709\u6a21\u5757\u662f\u5426\u5728\u6240\u9009\u7684 Python \u73af\u5883\u4e2d\u5b89\u88c5\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_check_imports.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u73af\u5883\u68c0\u67e5", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.uiPushButton_clear_data.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u6e05\u7a7a\u6216\u6062\u590d\u6253\u5305\u5de5\u5177\u4e2d\u6240\u6709\u5df2\u8f93\u5165\u3001\u6539\u53d8\u7684\u6253\u5305\u9009\u9879\uff08\u5df2\u4fdd\u5b58\u7684\u6253\u5305\u914d\u7f6e\u4e0d\u4f1a\u88ab\u6e05\u7a7a\uff09",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.uiPushButton_clear_data.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u6e05\u7a7a\u6570\u636e", None
            )
        )
        # if QT_CONFIG(tooltip)
        self.pb_gen_executable.setToolTip(
            QCoreApplication.translate(
                "pyinstaller_tool",
                "\u5c06 Python \u7a0b\u5e8f\u53ca\u6240\u9009\u8d44\u6e90\u6587\u4ef6\u6253\u5305\u6210 .exe \u53ef\u6267\u884c\u6587\u4ef6\u3002",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        self.pb_gen_executable.setText(
            QCoreApplication.translate(
                "pyinstaller_tool", "\u5f00\u59cb\u6253\u5305", None
            )
        )

    # retranslateUi

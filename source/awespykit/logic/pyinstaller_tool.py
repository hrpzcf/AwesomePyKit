# coding: utf-8

import os
import shutil
from platform import machine, platform
from typing import *

from com import *
from fastpip import PyEnv
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from settings import *
from ui import *
from utils.cip import ImportInspector
from utils.main import launch_explorer
from utils.pyi import PyiTool
from utils.venv import VtEnv

from .messagebox import MessageBox


class PyinstallerToolWindow(Ui_pyinstaller_tool, QMainWindow):
    signal_update_pyinfo = pyqtSignal(str)
    signal_update_packtoolinfo = pyqtSignal(str)
    signal_update_ptpbtext = pyqtSignal(str)
    signal_update_venv_pyinfo = pyqtSignal(str)
    PYIVER_FMT = "Pyinstaller - {} @ {}"
    QREV_FNAME = QRegExpValidator(QRegExp(r'[^\\/:*?"<>|]*'))
    QREV_NUMBER = QRegExpValidator(QRegExp(r"[0-9]*"))

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # 执行耗时操作完毕恢复控件可用时的例外情况
        self.__enabled_exception = dict()
        self.widgets_group_Enabled = (
            self.tab_project_files,
            self.tab_build_control,
            self.tab_file_ver_info,
            self.tab_advanced_setup,
            self.uiPushButton_select_pyenv,
            self.uiPushButton_reinstall_packtool,
            self.uiComboBox_log_level,
            self.uiLineEdit_output_name,
            self.uiPushButton_check_imports,
            self.uiPushButton_start_packing,
            self.uiCheckBox_prioritize_venv,
            self.uiPushButton_apply_config,
            self.uiPushButton_delete_config,
            self.uiPushButton_save_config,
            self.uiPushButton_create_venv,
            self.uiPushButton_clear_data,
            self.uiPushButton_refresh_venv,
        )
        self.uiLineEdit_vers_group = (
            self.uiLineEdit_file_version_0,
            self.uiLineEdit_file_version_1,
            self.uiLineEdit_file_version_2,
            self.uiLineEdit_file_version_3,
            self.uiLineEdit_product_version_0,
            self.uiLineEdit_product_version_1,
            self.uiLineEdit_product_version_2,
            self.uiLineEdit_product_version_3,
        )
        self.config = PyinstallerToolConfig()
        self.__setup_other_widgets()
        self.set_platform_info()
        self.thread_repo = ThreadRepo(500)
        self.main_environ = None
        self.virt_environ = None
        self.pyi_tool = PyiTool()
        self.__envch_win = EnvironChosenWindow(self, self.__environ_call_back)
        self.__impcheck_win = ImportsCheckWindow(self, self.__install_missings)
        self.signal_slot_connection()
        self.pyi_running_mov = QMovie(":/loading.gif")
        self.pyi_running_mov.setScaledSize(QSize(16, 16))
        self.__creating_venv_result = 1

    def __save_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.config.window_size = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        if not self.thread_repo.is_empty():
            MessageBox(
                "提醒",
                "任务正在运行中，关闭此窗口后任务将在后台运行。\n请勿对相关目录进行任\
何操作，否则可能会造成打包失败！",
                QMessageBox.Warning,
            ).exec_()
        self.__save_window_size()
        self.config_widgets_to_cfg()
        self.config.save_config()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

    def display(self):
        self.resize(*self.config.window_size)
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()
        if not self.thread_repo.is_empty():
            return
        self.config_cfg_to_widgets(None)

    def __setup_other_widgets(self):
        # 替换“程序启动入口”LineEdit控件
        self.uiLineEdit_program_entry = LineEdit(
            Accept.File, {".py", ".pyc", ".pyw", ".spec"}
        )
        self.uiLineEdit_program_entry.setToolTip(
            "要打包的程序的启动入口(*.py *.pyw *.pyc *.spec)，此项必填。\n"
            "如果指定了 SPEC 文件，则以下绝大部分项目文件及生成控制都将不生效。\n"
            "可将格式正确的文件拖放到此处。"
        )
        self.horizontalLayout_3.replaceWidget(
            self.uiLineEdit_program_entry_old, self.uiLineEdit_program_entry
        )
        self.uiLineEdit_program_entry_old.deleteLater()
        # 替换“其他模块搜索路径”TextEdit控件
        self.uiTextEdit_module_search_path = TextEdit(Accept.Dir)
        self.uiTextEdit_module_search_path.setToolTip(
            "对应选项：-p, --paths\n程序的其他模块的搜索路径(模块的父目录)，此项可留空。\n"
            "仅当 Pyinstaller 无法自动找到模块时使用，支持将文件夹直接拖放到此处。"
        )
        self.verticalLayout_3.replaceWidget(
            self.uiTextEdit_module_search_path_old,
            self.uiTextEdit_module_search_path,
        )
        self.uiTextEdit_module_search_path_old.deleteLater()
        # 替换“非源代码资源文件”LineEdit控件
        self.uiTextEdit_other_data = TextEdit(Accept.File)
        self.uiTextEdit_other_data.setToolTip(
            "对应选项：--add-data\n非源代码性质的其他资源文件，例如一些图片、配置文件等，"
            "此项可留空。\n注意：资源文件需是打包前程序真正使用的资源且在源代码根目录范围内，"
            "否则打包后程序可能无法运行。可将文件或者文件夹直接拖到此处。"
        )
        self.verticalLayout_4.replaceWidget(
            self.uiTextEdit_other_data_old, self.uiTextEdit_other_data
        )
        self.uiTextEdit_other_data_old.deleteLater()
        # 替换“文件图标路径”LineEdit控件
        self.uiLineEdit_file_icon_path = LineEdit(
            Accept.File, {".ico", ".png", ".jpg", ".jpeg", ".icns", ".exe"}
        )
        self.uiLineEdit_file_icon_path.setToolTip(
            "对应选项：-i, --icon\n生成的 exe 可执行文件使用的图标，支持 .ico 等格式。\n"
            "注意：如果选择 .png、.jpg、.jpeg 格式的图片，则需在打包环境中安装 Pillow 用于转换格式，"
            "否则打包失败。\n如果选择的是 .exe 文件，选择后需要在文件路径后加上[英文逗号和图标ID]，"
            "例如 'F:\\executable.exe,123'，不含引号\n除了 .ico 格式，"
            "其他格式图标的支持因 Pyinstaller 版本而异，可以将格式正确的文件直接拖放到此处。"
        )
        self.horizontalLayout_11.replaceWidget(
            self.uiLineEdit_file_icon_path_old, self.uiLineEdit_file_icon_path
        )
        self.uiLineEdit_file_icon_path_old.deleteLater()
        for line_edit in self.uiLineEdit_vers_group:
            line_edit.setValidator(self.QREV_NUMBER)
        self.uiLineEdit_output_name.setValidator(self.QREV_FNAME)
        self.uiLineEdit_runtime_tmpdir.setValidator(self.QREV_FNAME)
        self.splitter.setSizes((10000, 10000))

    def signal_slot_connection(self):
        self.pyi_tool.completed.connect(self.after_task_completed)
        self.pyi_tool.stdout.connect(self.uiTextEdit_packtool_logging.append)
        self.uiPushButton_select_pyenv.clicked.connect(self.__envch_win.display)
        self.uiPushButton_create_venv.clicked.connect(
            lambda: self.check_createvenv()
        )
        self.uiPushButton_refresh_venv.clicked.connect(
            self.refresh_virtualenv_info
        )
        self.uiLineEdit_program_entry.textChanged.connect(
            self.set_uilineedit_roots
        )
        self.uiPushButton_select_module_search_path.clicked.connect(
            self.set_te_module_search_path
        )
        self.uiPushButton_select_program_entry.clicked.connect(
            self.set_le_program_entry
        )
        self.uiPushButton_up_level_root.clicked.connect(
            lambda: self.project_root_level(1)
        )
        self.uiPushButton_reset_root_level.clicked.connect(
            lambda: self.project_root_level(0)
        )
        self.uiPushButton_clear_module_search_path.clicked.connect(
            self.uiTextEdit_module_search_path.clear
        )
        self.uiPushButton_select_other_data.clicked.connect(
            self.set_te_other_data
        )
        self.uiPushButton_clear_other_data.clicked.connect(
            self.uiTextEdit_other_data.clear
        )
        self.uiPushButton_select_file_icon.clicked.connect(
            self.set_le_file_icon_path
        )
        self.uiPushButton_select_spec_dir.clicked.connect(self.set_le_spec_dir)
        self.uiPushButton_select_temp_working_dir.clicked.connect(
            self.set_le_temp_working_dir
        )
        self.uiPushButton_select_output_dir.clicked.connect(
            self.set_le_output_dir
        )
        self.uiPushButton_select_upx_search_path.clicked.connect(
            self.set_le_upx_search_path
        )
        self.uiPushButton_start_packing.clicked.connect(self.build_executable)
        self.uiPushButton_reinstall_packtool.clicked.connect(
            self.reinstall_pyinstaller
        )
        self.uiPushButton_check_imports.clicked.connect(
            self.check_project_imports
        )
        self.uiPushButton_clear_hidden_imports.clicked.connect(
            self.uiPlainTextEdit_hidden_imports.clear
        )
        self.uiPushButton_clear_exclude_module.clicked.connect(
            self.uiPlainTextEdit_exclude_modules.clear
        )
        self.uiPushButton_save_config.clicked.connect(self.store_current_config)
        self.uiPushButton_apply_config.clicked.connect(
            self.apply_selected_config
        )
        self.uiPushButton_delete_config.clicked.connect(
            self.delete_selected_config
        )
        self.signal_update_pyinfo.connect(self.uiLabel_python_info.setText)
        self.signal_update_packtoolinfo.connect(
            self.uiLabel_packtool_info.setText
        )
        self.signal_update_ptpbtext.connect(
            self.uiPushButton_reinstall_packtool.setText
        )
        self.signal_update_venv_pyinfo.connect(self.uiLabel_venv_info.setText)
        self.uiLineEdit_config_remark.textChanged.connect(
            self.lineedit_remark_textchanged
        )
        self.uiListWidget_saved_config.currentRowChanged.connect(
            self.listwidget_savedconfig_clicked
        )
        self.uiPushButton_clear_data.clicked.connect(self.clear_packing_data)
        self.uiCheckBox_prioritize_venv.clicked.connect(
            self.refresh_virtualenv_info
        )
        self.uiPushButton_clear_log.clicked.connect(
            self.uiTextEdit_packtool_logging.clear
        )

    def refresh_virtualenv_info(self):
        self.config_widgets_to_cfg()
        self.load_version_information_lazily(True, True)

    def clear_packing_data(self):
        self.config.current.clear()
        self.config_cfg_to_widgets(None)

    def check_project_imports(self):
        self.config_widgets_to_cfg()
        self.virt_environ = VtEnv(self.config.current.project_root)
        self.virt_environ.find_venv()
        if self.config.current.prioritize_venv:
            if not self.virt_environ.venv_exists:
                return MessageBox(
                    "提示",
                    "项目根目录下不存在虚拟环境，如果你确定你设置的“项目根目录”"
                    "正确无误，那么请先点击“创建”创建项目虚拟环境，或直接点击“开始打包”，"
                    "程序会引导创建虚拟环境。",
                    QMessageBox.Warning,
                ).exec_()
            environ = self.virt_environ
        else:
            environ = self.main_environ
        if not environ:
            MessageBox(
                "提示",
                "还没有选择主 Python 环境或者勾选优先使用项目目录下的虚拟环境。",
                QMessageBox.Warning,
            ).exec_()
            return
        program_root = self.config.current.program_root
        if not program_root:
            MessageBox(
                "提示",
                "源代码根目录未填写！",
                QMessageBox.Warning,
            ).exec_()
            return
        if not os.path.isdir(program_root):
            MessageBox(
                "提示",
                "源代码根目录不存在！",
                QMessageBox.Warning,
            ).exec_()
            return
        dist_dir = self.config.current.distribution_dir
        if not dist_dir:
            dist_dir = os.path.join(program_root, "dist")
        elif not os.path.isabs(dist_dir):
            dist_dir = os.path.join(program_root, dist_dir)
        missings = list()
        self.pyi_tool.initialize(environ, program_root)
        if not self.pyi_tool.pyi_is_ready:
            missings.append(("打包功能核心模块", {}, {"pyinstaller"}))

        def get_missing_imps():
            inspector = ImportInspector(
                environ.env_path,
                program_root,
                [self.virt_environ.env_path, dist_dir],
            )
            if (
                self.config.current.encryption_key
                and "tinyaes" not in inspector.importables
            ):
                missings.append(("字节码加密功能", {}, {"tinyaes>=1.0.0"}))
            missings.extend(inspector.get_missing_items())

        thread_check_imp = QThreadModel(get_missing_imps)
        thread_check_imp.before_starting(
            self.__lock_widgets,
            lambda: self.__show_running("正在分析项目依赖在环境中的安装情况..."),
        )
        thread_check_imp.after_completion(
            self.__hide_running,
            self.__release_widgets,
            lambda: self.__impcheck_win.display_result(environ, missings),
        )
        thread_check_imp.start()
        self.thread_repo.put(thread_check_imp, 1)

    def set_le_program_entry(self):
        selected_file = self.__ask_file_or_dir_path(
            "选择程序启动入口",
            self.config.current.program_root,
            ext_filter="脚本文件 (*.py *.pyc *.pyw *.spec)",
        )[0]
        if not selected_file:
            return
        self.uiLineEdit_program_entry.setText(selected_file)

    def set_uilineedit_roots(self):
        root = os.path.dirname(self.uiLineEdit_program_entry.text())
        self.uiLineEdit_project_root.setText(root)
        self.uiLineEdit_program_root.setText(root)

    def set_te_module_search_path(self):
        selected_dir = self.__ask_file_or_dir_path(
            "其他模块搜索目录", self.config.current.program_root, ch=Accept.Dir
        )[0]
        if not selected_dir:
            return
        self.uiTextEdit_module_search_path.append(selected_dir)

    def set_te_other_data(self):
        selected_files = self.__ask_file_or_dir_path(
            "选择非源码资源文件", self.config.current.program_root, multi=True
        )
        if not selected_files:
            return
        self.uiTextEdit_other_data.append("\n".join(selected_files))

    def set_le_file_icon_path(self):
        selected_file = self.__ask_file_or_dir_path(
            "选择可执行文件图标",
            self.config.current.program_root,
            ext_filter="图标文件 (*.ico *.icns);;常规图片 (*.png *.jpg *.jpeg);;可执行文件 (*.exe)",
        )[0]
        if not selected_file:
            return
        self.uiLineEdit_file_icon_path.setText(selected_file)

    def set_le_spec_dir(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择SPEC文件储存目录", self.config.current.program_root, ch=Accept.Dir
        )[0]
        if not selected_dir:
            return
        self.uiLineEdit_spec_dir.setText(selected_dir)

    def set_le_temp_working_dir(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择临时文件目录", self.config.current.program_root, ch=Accept.Dir
        )[0]
        if not selected_dir:
            return
        self.uiLineEdit_temp_working_dir.setText(selected_dir)

    def set_le_output_dir(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择生成文件储存目录", self.config.current.program_root, ch=Accept.Dir
        )[0]
        if not selected_dir:
            return
        self.uiLineEdit_output_dir.setText(selected_dir)

    def set_le_upx_search_path(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择UPX程序搜索目录", self.config.current.program_root, ch=Accept.Dir
        )[0]
        if not selected_dir:
            return
        self.uiLineEdit_upx_search_path.setText(selected_dir)

    def __ask_file_or_dir_path(
        self,
        title="",
        start="",
        ch=Accept.File,
        multi=False,
        ext_filter="所有文件 (*)",
    ):
        file_dir_paths = []
        if ch == Accept.File and multi:
            if not title:
                title = "选择多文件"
            path_getter = QFileDialog.getOpenFileNames
        elif ch == Accept.File and not multi:
            if not title:
                title = "选择文件"
            path_getter = QFileDialog.getOpenFileName
        elif ch == Accept.Dir:
            if not title:
                title = "选择文件夹"
            path_getter = QFileDialog.getExistingDirectory
        else:
            return file_dir_paths
        if ch == Accept.File and not multi:
            path = path_getter(self, title, start, ext_filter)[0]
            if not path:
                file_dir_paths.append("")
            else:
                file_dir_paths.append(os.path.realpath(path))
        elif ch == Accept.File and multi:
            paths = path_getter(self, title, start, ext_filter)[0]
            file_dir_paths.extend(
                os.path.realpath(path) for path in paths if path
            )
            if not file_dir_paths:
                file_dir_paths.append("")
        elif ch == Accept.Dir:
            path = path_getter(self, title, start)
            if not path:
                file_dir_paths.append("")
            else:
                file_dir_paths.append(os.path.realpath(path))
        return file_dir_paths

    def __environ_call_back(self, env):
        """供环境选择窗口类使用的回调函数，在窗口选择环境后调用此方法"""
        self.main_environ = env
        self.pyi_tool.initialize(
            self.main_environ, self.config.current.program_root
        )
        self.load_version_information_lazily(False, False)

    def config_cfg_to_widgets(self, cfg_name):
        self.update_listwidget_configure_items()
        if cfg_name is not None:
            self.config.checkout_cfg(cfg_name)
        self.load_version_information_lazily(True, True)
        self.uiLineEdit_program_entry.setText(self.config.current.script_path)
        self.uiLineEdit_program_root.setText(self.config.current.program_root)
        self.uiLineEdit_project_root.setText(self.config.current.project_root)
        self.uiTextEdit_module_search_path.setText(
            "\n".join(self.config.current.module_paths)
        )
        self.uiTextEdit_other_data.setText(
            "\n".join(pg[0] for pg in self.config.current.other_datas)
        )
        self.uiLineEdit_file_icon_path.setText(self.config.current.icon_path)
        if self.config.current.onedir_bundle:
            self.uiRadioButton_pack_to_one_dir.setChecked(True)
        else:
            self.uiRadioButton_pack_to_one_file.setChecked(True)
        self.uiCheckBox_execute_with_console.setChecked(
            self.config.current.provide_console
        )
        self.uiCheckBox_without_confirm.setChecked(
            self.config.current.no_confirm
        )
        self.uiCheckBox_use_upx.setChecked(
            not self.config.current.donot_use_upx
        )
        self.uiCheckBox_clean_before_build.setChecked(
            self.config.current.clean_building
        )
        self.uiCheckBox_write_info_to_exec.setChecked(
            self.config.current.add_verfile
        )
        self.uiLineEdit_temp_working_dir.setText(
            self.config.current.working_dir
        )
        self.uiLineEdit_output_dir.setText(self.config.current.distribution_dir)
        self.uiLineEdit_spec_dir.setText(self.config.current.spec_dir)
        self.uiLineEdit_upx_search_path.setText(self.config.current.upx_dir)
        self.uiTextEdit_upx_exclude_files.setText(
            "\n".join(self.config.current.upx_excludes)
        )
        self.uiLineEdit_output_name.setText(
            self.config.current.bundle_spec_name
        )
        self.uiComboBox_log_level.setCurrentText(self.config.current.log_level)
        self.set_file_ver_info_text()
        self.set_pyi_debug_options()
        self.uiLineEdit_runtime_tmpdir.setText(
            self.config.current.runtime_tmpdir
        )
        self.uiCheckBox_prioritize_venv.setChecked(
            self.config.current.prioritize_venv
        )
        self.uiLineEdit_bytecode_encryption_key.setText(
            self.config.current.encryption_key
        )
        self.uiCheckBox_explorer_show.setChecked(
            self.config.current.open_dist_folder
        )
        self.uiCheckBox_delete_working_dir.setChecked(
            self.config.current.delete_working_dir
        )
        self.uiCheckBox_delete_spec_file.setChecked(
            self.config.current.delete_spec_file
        )
        self.uiPlainTextEdit_hidden_imports.setPlainText(
            "\n".join(self.config.current.hidden_imports)
        )
        self.uiPlainTextEdit_exclude_modules.setPlainText(
            "\n".join(self.config.current.exclude_modules)
        )
        self.uiCheckBox_uac_admin.setChecked(self.config.current.uac_admin)

    def config_widgets_to_cfg(self):
        self.config.current.script_path = (
            self.uiLineEdit_program_entry.local_path
        )
        self.config.current.bundle_spec_name = (
            self.uiLineEdit_output_name.text()
        )
        program_root = self.uiLineEdit_program_root.text()
        self.config.current.program_root = program_root
        self.config.current.project_root = self.uiLineEdit_project_root.text()
        self.config.current.module_paths = (
            self.uiTextEdit_module_search_path.local_paths
        )
        self.config.current.other_datas = self.__gen_absrel_groups(program_root)
        self.config.current.icon_path = (
            self.uiLineEdit_file_icon_path.local_path
        )
        self.config.current.onedir_bundle = (
            self.uiRadioButton_pack_to_one_dir.isChecked()
        )
        self.config.current.provide_console = (
            self.uiCheckBox_execute_with_console.isChecked()
        )
        self.config.current.no_confirm = (
            self.uiCheckBox_without_confirm.isChecked()
        )
        self.config.current.donot_use_upx = (
            not self.uiCheckBox_use_upx.isChecked()
        )
        self.config.current.clean_building = (
            self.uiCheckBox_clean_before_build.isChecked()
        )
        self.config.current.add_verfile = (
            self.uiCheckBox_write_info_to_exec.isChecked()
        )
        self.config.current.working_dir = (
            self.uiLineEdit_temp_working_dir.text()
        )
        self.config.current.distribution_dir = self.uiLineEdit_output_dir.text()
        self.config.current.spec_dir = self.uiLineEdit_spec_dir.text()
        self.config.current.upx_dir = self.uiLineEdit_upx_search_path.text()
        self.config.current.upx_excludes = [
            s
            for s in self.uiTextEdit_upx_exclude_files.toPlainText().split("\n")
            if s
        ]
        if self.main_environ is not None:
            self.config.current.environ_path = self.main_environ.env_path
        self.config.current.log_level = self.uiComboBox_log_level.currentText()
        self.config.current.version_info = self.file_ver_info_text()
        self.config.current.debug_options = self.get_pyi_debug_options()
        self.config.current.runtime_tmpdir = (
            self.uiLineEdit_runtime_tmpdir.text()
        )
        self.config.current.prioritize_venv = (
            self.uiCheckBox_prioritize_venv.isChecked()
        )
        self.config.current.encryption_key = (
            self.uiLineEdit_bytecode_encryption_key.text()
        )
        self.config.current.open_dist_folder = (
            self.uiCheckBox_explorer_show.isChecked()
        )
        self.config.current.delete_working_dir = (
            self.uiCheckBox_delete_working_dir.isChecked()
        )
        self.config.current.delete_spec_file = (
            self.uiCheckBox_delete_spec_file.isChecked()
        )
        self.config.current.uac_admin = self.uiCheckBox_uac_admin.isChecked()
        self.config.current.hidden_imports = [
            s
            for s in self.uiPlainTextEdit_hidden_imports.toPlainText().split(
                "\n"
            )
            if s
        ]
        self.config.current.exclude_modules = [
            s
            for s in self.uiPlainTextEdit_exclude_modules.toPlainText().split(
                "\n"
            )
            if s
        ]

    def __gen_absrel_groups(self, starting_point):
        """获取其他要打包的文件的本地路径和与源代码根目录的相对位置。"""
        other_data_local_paths = self.uiTextEdit_other_data.local_paths
        abs_rel_path_groups = []
        for abs_path in other_data_local_paths:
            try:
                rel_path = os.path.relpath(
                    os.path.dirname(abs_path), starting_point
                )
            except Exception:
                continue
            abs_rel_path_groups.append((abs_path, rel_path))
        return abs_rel_path_groups

    def get_pyi_debug_options(self):
        return {
            "imports": self.uiCheckBox_db_imports.isChecked(),
            "bootloader": self.uiCheckBox_db_bootloader.isChecked(),
            "noarchive": self.uiCheckBox_db_noarchive.isChecked(),
        }

    def set_pyi_debug_options(self):
        dbo = self.config.current.debug_options
        self.uiCheckBox_db_imports.setChecked(dbo.get("imports", False))
        self.uiCheckBox_db_bootloader.setChecked(dbo.get("bootloader", False))
        self.uiCheckBox_db_noarchive.setChecked(dbo.get("noarchive", False))

    def file_ver_info_text(self):
        file_vers = tuple(
            int(x.text() or 0) for x in self.uiLineEdit_vers_group[:4]
        )
        prod_vers = tuple(
            int(x.text() or 0) for x in self.uiLineEdit_vers_group[4:]
        )
        return {
            "$filevers$": str(file_vers),
            "$prodvers$": str(prod_vers),
            "$CompanyName$": self.uiLineEdit_company_name.text(),
            "$FileDescription$": self.uiLineEdit_file_description.text(),
            "$FileVersion$": ".".join(map(str, file_vers)),
            "$LegalCopyright$": self.uiLineEdit_legal_copyright.text(),
            "$OriginalFilename$": self.uiLineEdit_original_filename.text(),
            "$ProductName$": self.uiLineEdit_product_name.text(),
            "$ProductVersion$": ".".join(map(str, prod_vers)),
            "$LegalTrademarks$": self.uiLineEdit_legal_trademarks.text(),
        }

    def set_file_ver_info_text(self):
        version_info = self.config.current.version_info
        self.uiLineEdit_file_description.setText(
            version_info.get("$FileDescription$", "")
        )
        self.uiLineEdit_company_name.setText(
            version_info.get("$CompanyName$", "")
        )
        for ind, val in enumerate(
            version_info.get("$FileVersion$", "0.0.0.0").split(".")
        ):
            self.uiLineEdit_vers_group[ind].setText(val)
        self.uiLineEdit_product_name.setText(
            version_info.get("$ProductName$", "")
        )
        for ind, val in enumerate(
            version_info.get("$ProductVersion$", "0.0.0.0").split(".")
        ):
            self.uiLineEdit_vers_group[ind + 4].setText(val)
        self.uiLineEdit_legal_copyright.setText(
            version_info.get("$LegalCopyright$", "")
        )
        self.uiLineEdit_legal_trademarks.setText(
            version_info.get("$LegalTrademarks$", "")
        )
        self.uiLineEdit_original_filename.setText(
            version_info.get("$OriginalFilename$", "")
        )

    def reinstall_pyinstaller(self):
        if self.uiCheckBox_prioritize_venv.isChecked():
            message = "虚拟环境"
            operating_environment = self.virt_environ
        else:
            message = "主要环境"
            operating_environment = self.main_environ
        if operating_environment is None:
            return MessageBox(
                "提示",
                "当前未选择任何主要 Python 环境或没有选择虚拟环境。",
                QMessageBox.Warning,
            ).exec_()
        # NewMessageBox的exec_方法返回0才是选择"确定"按钮
        if MessageBox(
            "安装",
            f"确定安装 Pyinstaller 到{message}吗？",
            QMessageBox.Question,
            (("accept", "确定"), ("reject", "取消")),
        ).exec_():
            return

        def do_reinstall_pyi():
            operating_environment.uninstall("pyinstaller")
            operating_environment.install("pyinstaller", upgrade=1)

        thread_reinstall = QThreadModel(do_reinstall_pyi)
        thread_reinstall.before_starting(
            self.__lock_widgets,
            lambda: self.__show_running("正在安装 Pyinstaller..."),
        )
        thread_reinstall.after_completion(
            self.__hide_running,
            self.__release_widgets,
            lambda: self.load_version_information_lazily(False, False),
        )
        thread_reinstall.start()
        self.thread_repo.put(thread_reinstall, 0)

    def set_platform_info(self):
        self.uiLabel_platform_info.setText(f"{platform()}-{machine()}")

    def project_root_level(self, option):
        """option: 0 表示重置为初始路径，1 表示设为上一级"""
        assert option in (0, 1)
        root = self.uiLineEdit_project_root.text()
        if not root:
            return
        if option == 1:
            _path = os.path.dirname(root)
        else:
            origin = self.uiLineEdit_program_entry.text()
            if not origin:
                return
            _path = os.path.dirname(origin)
        self.uiLineEdit_project_root.setText(_path)

    def __check_requireds(self):
        self.config_widgets_to_cfg()
        program_entry = self.config.current.script_path
        if not program_entry:
            MessageBox(
                "错误",
                "程序启动入口未填写！",
                QMessageBox.Critical,
            ).exec_()
            return False
        if not os.path.isfile(program_entry):
            MessageBox(
                "错误",
                "程序启动入口文件不存在！",
                QMessageBox.Critical,
            ).exec_()
            return False
        if not os.path.isdir(self.config.current.program_root):
            MessageBox(
                "错误",
                "程序根目录未填写或目录不存在！",
                QMessageBox.Critical,
            ).exec_()
            return False
        if not os.path.isdir(self.config.current.project_root):
            MessageBox(
                "错误",
                "项目根目录未填写或目录不存在！",
                QMessageBox.Critical,
            ).exec_()
            return False
        icon_path = self.config.current.icon_path
        if icon_path != "" and not os.path.isfile(icon_path):
            MessageBox(
                "错误",
                "程序图标文件不存在！",
                QMessageBox.Critical,
            ).exec_()
            return False
        return True

    def __show_running(self, msg):
        self.uiLabel_running_tip.setText(msg)
        self.uiLabel_running_gif.setMovie(self.pyi_running_mov)
        self.pyi_running_mov.start()

    def __hide_running(self):
        self.pyi_running_mov.stop()
        self.uiLabel_running_gif.clear()
        self.uiLabel_running_tip.clear()

    def __lock_widgets(self):
        for widget in self.widgets_group_Enabled:
            widget.setEnabled(False)

    def __release_widgets(self):
        for widget in self.widgets_group_Enabled:
            widget.setEnabled(self.__enabled_exception.get(widget, True))

    def importance_operation_start(self, string):
        def function():
            self.__lock_widgets()
            self.__show_running(string)

        return function

    def importance_operation_finished(self):
        self.__hide_running()
        self.__release_widgets()

    def __get_program_name(self):
        program_name = self.config.current.bundle_spec_name
        if not program_name:
            program_name = os.path.splitext(
                os.path.basename(self.config.current.script_path)
            )[0]
        return program_name

    def open_explorer_select_file(self):
        program_name = self.__get_program_name()
        if self.uiRadioButton_pack_to_one_file.isChecked():
            sub_directory = ""
        else:
            sub_directory = program_name
        final_execfn, ext = os.path.splitext(program_name)
        if ext.lower() != ".exe":
            final_execfn = program_name
        dist_folder = self.config.current.distribution_dir
        if not dist_folder:
            dist_folder = os.path.join(self.config.current.program_root, "dist")
        elif not os.path.isabs(dist_folder):
            dist_folder = os.path.join(
                self.config.current.program_root, dist_folder
            )
        launch_explorer(
            os.path.join(dist_folder, sub_directory), [final_execfn + ".exe"]
        )

    def delete_spec_file(self):
        spec_file_dir = self.config.current.spec_dir
        if not spec_file_dir:
            spec_file_dir = self.config.current.program_root
        elif not os.path.isabs(spec_file_dir):
            spec_file_dir = os.path.join(
                self.config.current.program_root, spec_file_dir
            )
        program_name = self.__get_program_name()
        spec_file_path = os.path.join(spec_file_dir, program_name) + ".spec"
        try:
            os.remove(spec_file_path)
        except Exception:
            pass
        # 自定义 spec 文件储存目录的情况下，考虑到目录内可能有其他文件
        # 所以只考虑删除 spec 文件，不删除自定义目录，以防误删其他无关文件

    def delete_working_dir(self):
        program_name = self.__get_program_name()
        custom_working_dir = self.config.current.working_dir
        if not custom_working_dir:
            working_dir_root = os.path.join(
                self.config.current.program_root, "build"
            )
        elif not os.path.isabs(custom_working_dir):
            working_dir_root = os.path.join(
                self.config.current.program_root, custom_working_dir
            )
        else:
            working_dir_root = os.path.join(custom_working_dir, program_name)
        thread_delete_working = QThreadModel(
            shutil.rmtree, working_dir_root, True
        )
        thread_delete_working.start()
        self.thread_repo.put(thread_delete_working)

    def after_task_completed(self, retcode):
        if retcode == 0:
            if self.uiCheckBox_explorer_show.isChecked():
                self.open_explorer_select_file()
            if self.uiCheckBox_delete_spec_file.isChecked():
                self.delete_spec_file()
            if self.uiCheckBox_delete_working_dir.isChecked():
                self.delete_working_dir()
            MessageBox(
                "任务结束",
                "Python 程序已打包完成！",
            ).exec_()
        else:
            MessageBox(
                "任务结束",
                "打包失败，请检查错误信息！",
                QMessageBox.Critical,
            ).exec_()

    def __creating_venv(self):
        dist_dir = self.config.current.distribution_dir
        if not dist_dir:
            dist_dir = os.path.join(self.config.current.program_root, "dist")
        elif not os.path.isabs(dist_dir):
            dist_dir = os.path.join(self.config.current.program_root, dist_dir)
        if self.virt_environ.create_project_venv(self.main_environ.interpreter):
            import_inspect = ImportInspector(
                self.virt_environ.env_path,
                self.config.current.program_root,
                [self.virt_environ.env_path, dist_dir],
            )
            missings: Set[str] = {"pyinstaller"}
            for ms in import_inspect.get_missing_items():
                for m in ms[2]:
                    missings.add(PKGNAME_MAP.get(m, m))
            if self.config.current.encryption_key:
                missings.add("tinyaes>=1.0.0")
            self.virt_environ.install("wheel")
            for pkg in missings:
                self.virt_environ.install(pkg)
            self.__creating_venv_result = 0  # 虚拟环境创建成功
        else:
            self.__creating_venv_result = 1  # 虚拟环境创建失败

    def check_createvenv(self, finished: Callable[[], Any] = None):
        self.config_widgets_to_cfg()
        self.virt_environ = VtEnv(self.config.current.project_root)
        if self.virt_environ.find_venv():
            MessageBox("提示", "当前项目下已存在虚拟环境。").exec_()
            return
        if not self.config.current.project_root:
            MessageBox(
                "提示",
                "项目根目录还未设置，无法确定虚拟环境创建位置。",
            ).exec_()
            return
        if self.main_environ is None or not self.main_environ.env_path:
            MessageBox(
                "提示",
                "没有选择主 Python 环境或者主 Python 环境不可用。",
                QMessageBox.Warning,
            ).exec_()
            return
        thread_venv_creating = QThreadModel(self.__creating_venv)
        thread_venv_creating.before_starting(
            self.__lock_widgets,
            lambda: self.__show_running("正在创建虚拟环境并安装模块..."),
        )
        thread_venv_creating.after_completion(
            self.__hide_running,
            self.__release_widgets,
        )
        if finished is not None:
            thread_venv_creating.after_completion(finished)
        thread_venv_creating.start()
        self.thread_repo.put(thread_venv_creating, 0)

    def build_executable(self):
        if not self.__check_requireds():
            return
        if self.uiListWidget_saved_config.currentRow() != -1:
            result = MessageBox(
                "提示",
                "你选择的打包配置似乎还没有应用以使其生效，确定开始打包吗？",
                QMessageBox.Warning,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            if result != 0:
                return
        self.uiListWidget_saved_config.setCurrentRow(-1)
        self.uiTextEdit_packtool_logging.clear()
        if self.config.current.prioritize_venv:
            self.virt_environ = VtEnv(self.config.current.project_root)
            self.__creating_venv_result = 0
            if not self.virt_environ.find_venv():
                role = MessageBox(
                    "提示",
                    "项目根目录下不存在虚拟环境，请选择合适选项。",
                    QMessageBox.Warning,
                    (
                        ("accept", "使用主环境"),
                        ("destructive", "创建虚拟环境"),
                        ("reject", "取消"),
                    ),
                ).exec_()
                if role == 0:
                    environ_using = self.main_environ
                elif role == 1:
                    self.check_createvenv(self.build_executable)
                    return
                else:
                    return
            else:
                if self.__creating_venv_result != 0:
                    MessageBox(
                        "错误",
                        "项目目录下的虚拟环境创建失败。",
                        QMessageBox.Critical,
                    ).exec_()
                    return
                environ_using = self.virt_environ
        else:
            environ_using = self.main_environ
        self.pyi_tool.initialize(
            environ_using, self.config.current.program_root
        )
        if not self.pyi_tool.pyi_is_ready:
            MessageBox(
                "Pyinstaller 不可用",
                "请点击右上角'选择环境'按钮选择打包环境，再点击'安装'按钮将 Pyinstaller "
                "安装到所选的打包环境。\n如果勾选了'使用项目目录下的虚拟环境而不是以上环境'，"
                "请点击'环境检查'按钮检查环境中缺失的模块并'一键安装'。",
                QMessageBox.Warning,
            ).exec_()
            return
        self.pyi_tool.prepare_cmds(self.config.current)
        thread_build = QThreadModel(self.pyi_tool.execute_cmd)
        thread_build.before_starting(
            self.__lock_widgets,
            lambda: self.__show_running("正在生成可执行文件..."),
        )
        thread_build.after_completion(
            self.__hide_running, self.__release_widgets
        )
        thread_build.start()
        self.thread_repo.put(thread_build, 0)

    def __install_missings(self, missings):
        if not missings:
            MessageBox(
                "提示",
                "没有缺失的模块，无需安装。",
            ).exec_()
            return self.__impcheck_win.close()
        if (
            MessageBox(
                "安装",
                "确定将所有缺失模块安装至所选 Python 环境中吗？",
                QMessageBox.Question,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            != 0
        ):
            return
        if self.config.current.prioritize_venv:
            environ = self.virt_environ
        else:
            environ = self.main_environ

        def install_pkgs():
            names_for_install = set()
            for imp in missings:
                names_for_install.add(PKGNAME_MAP.get(imp, imp))
            for imp in names_for_install:
                environ.install(imp)

        self.__impcheck_win.close()
        thread_install_missings = QThreadModel(install_pkgs)
        thread_install_missings.before_starting(
            self.__lock_widgets,
            lambda: self.__show_running("正在安装缺失模块..."),
        )
        thread_install_missings.after_completion(
            self.__hide_running,
            self.__release_widgets,
            lambda: MessageBox(
                "完成",
                "已完成安装流程，请重新检查是否安装成功。",
                QMessageBox.Information,
            ).exec_(),
        )
        thread_install_missings.start()
        self.thread_repo.put(thread_install_missings, 0)

    def listwidget_savedconfig_clicked(self):
        index = self.uiListWidget_saved_config.currentRow()
        if index == -1:
            return
        self.uiLineEdit_config_remark.textChanged.disconnect(
            self.lineedit_remark_textchanged
        )
        self.uiLineEdit_config_remark.setText(
            self.uiListWidget_saved_config.item(index).text()
        )
        self.uiLineEdit_config_remark.textChanged.connect(
            self.lineedit_remark_textchanged
        )

    def update_listwidget_configure_items(self):
        self.uiListWidget_saved_config.clear()
        for item_title in self.config.multicfg.keys():
            item = QListWidgetItem(item_title)
            self.uiListWidget_saved_config.addItem(item)

    def lineedit_remark_textchanged(self):
        self.uiListWidget_saved_config.setCurrentRow(-1)

    def store_current_config(self):
        text = (
            self.uiLineEdit_config_remark.text()
            or self.uiLineEdit_config_remark.placeholderText()
        )
        if not text:
            return MessageBox(
                "提示",
                "还没有输入备注名称。",
            ).exec_()
        if text in self.config.multicfg:
            result = MessageBox(
                "提示",
                f"配置列表已存在名称：{text}，是否覆盖？",
                QMessageBox.Warning,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            if result != 0:
                return
        self.uiLineEdit_config_remark.clear()
        self.config_widgets_to_cfg()
        self.config.store_curcfg(text)
        self.update_listwidget_configure_items()
        MessageBox("提示", f"配置已保存：{text}。").exec_()

    def delete_selected_config(self):
        if not len(self.config.multicfg):
            return MessageBox("提示", "没有已保存的配置。").exec_()
        cur_item = self.uiListWidget_saved_config.currentItem()
        if not cur_item:
            return MessageBox("提示", "没有选择任何配置。").exec_()
        text = cur_item.text()
        if text not in self.config.multicfg:
            return
        if (
            MessageBox(
                "提示",
                f"即将被删除的配置：{text}",
                QMessageBox.Warning,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            != 0
        ):
            return
        del self.config.multicfg[text]
        self.update_listwidget_configure_items()

    def apply_selected_config(self):
        if not len(self.config.multicfg):
            return MessageBox("提示", "没有已保存的配置。").exec_()
        cur_item = self.uiListWidget_saved_config.currentItem()
        if not cur_item:
            return MessageBox("提示", "没有选择任何配置。").exec_()
        self.config_cfg_to_widgets(cur_item.text())
        self.uiListWidget_saved_config.setCurrentRow(-1)

    def load_version_information_lazily(self, refresh_pyenv, refresh_venv):
        """延迟执行显示 Python 和 Pyinstaller 版本信息这两个耗时操做"""

        def do_load_version_information():
            if refresh_pyenv:
                self.main_environ = PyEnv(self.config.current.environ_path)
            if refresh_venv:
                self.virt_environ = VtEnv(self.config.current.project_root)
                self.virt_environ.find_venv()
            if self.uiCheckBox_prioritize_venv.isChecked():
                ptool_side = "虚拟环境"
                ptool_env = self.virt_environ
            else:
                ptool_side = "主要环境"
                ptool_env = self.main_environ
            btn_create = False
            if (
                self.virt_environ is not None
                and not self.virt_environ.venv_exists
                and self.main_environ is not None
                and self.main_environ.env_path
            ):
                btn_create = True
            self.__enabled_exception[self.uiPushButton_create_venv] = btn_create
            self.pyi_tool.initialize(
                ptool_env, self.config.current.program_root
            )
            packtool_info = self.pyi_tool.pyi_info()
            if ptool_env is None or not ptool_env.env_is_valid:
                btn_install = False
                button_text = "安装"
            else:
                btn_install = True
                if not self.pyi_tool.pyi_is_ready:
                    button_text = "安装"
                else:
                    button_text = "重新安装"
            self.__enabled_exception[
                self.uiPushButton_reinstall_packtool
            ] = btn_install
            packtool_info = self.PYIVER_FMT.format(packtool_info, ptool_side)
            if self.main_environ is None or not self.main_environ.env_path:
                python_info = ""
            else:
                python_info = self.main_environ.py_info()
            if self.virt_environ is None or not self.virt_environ.find_venv():
                venv_pyinfo = ""
            else:
                venv_pyinfo = self.virt_environ.py_info()
            self.signal_update_venv_pyinfo.emit(venv_pyinfo)
            self.signal_update_pyinfo.emit(python_info)
            self.signal_update_packtoolinfo.emit(packtool_info)
            self.signal_update_ptpbtext.emit(button_text)

        thread_load_info = QThreadModel(do_load_version_information)
        thread_load_info.before_starting(
            self.importance_operation_start("正在读取环境信息...")
        )
        thread_load_info.after_completion(self.importance_operation_finished)
        thread_load_info.start()
        self.thread_repo.put(thread_load_info, 1)


class EnvironChosenWindow(Ui_environ_chosen, QMainWindow):
    def __init__(self, parent: PyinstallerToolWindow, callback):
        self.__parent = parent
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.__envpairlist: Union[None, List[EnvDisplayPair]] = None
        self.__call_back = callback
        self.uiListWidget_environ_list.clicked.connect(self.__call_environ_back)

    def display(self):
        self.resize(*self.__parent.config.envch_winsize)
        self.showNormal()
        self.__env_list_update()

    def __env_list_update(self):
        self.uiListWidget_environ_list.clear()
        self.__envpairlist = [
            EnvDisplayPair(PyEnv(p)) for p in self.__parent.config.pypaths
        ]
        for envp in self.__envpairlist:
            item = QListWidgetItem(QIcon(":/python.png"), envp.display)
            self.uiListWidget_environ_list.addItem(item)
            envp.signal_connect(item.setText)
            envp.load_real_display()

    def __clear_envpairlist(self):
        if self.__envpairlist is None:
            return
        for envp in self.__envpairlist:
            envp.discard()

    def closeEvent(self, event: QCloseEvent):
        self.__save_window_size()
        self.__clear_envpairlist()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

    def __call_environ_back(self):
        self.close()
        selected = self.uiListWidget_environ_list.currentRow()
        if selected != -1:
            self.__call_back(self.__envpairlist[selected].environ)

    def __save_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__parent.config.envch_winsize = self.width(), self.height()


class ImportsCheckWindow(Ui_imports_check, QMainWindow):
    def __init__(self, parent: PyinstallerToolWindow, call_install):
        super().__init__(parent)
        self.__parent = parent
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.__setup_other_widgets()
        self.uiPushButton_confirm.clicked.connect(self.close)
        self.uiPushButton_install_missings.clicked.connect(
            self.__call_install_back
        )
        self.__missing_modules = None
        self.__call_install = call_install

    def __setup_other_widgets(self):
        self.uiTableWidget_missing_imports.setColumnWidth(0, 260)
        self.uiTableWidget_missing_imports.setColumnWidth(1, 360)
        self.uiTableWidget_missing_imports.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )
        self.uiTableWidget_missing_imports.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.Stretch
        )

    def __call_install_back(self):
        self.close()  # 触发 closeEvent
        self.__call_install(self.__missing_modules)

    def __save_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__parent.config.impcheck_winsize = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        self.__save_window_size()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()
        elif event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.__call_install_back()

    def display_window(self):
        self.resize(*self.__parent.config.impcheck_winsize)
        self.showNormal()

    def display_result(self, environ, missings_list):
        """
        missings_list: [(filepath, {imps...}, {missings...})...]
        """
        if environ:
            self.uiLineEdit_current_env.setText(str(environ))
        self.__missing_modules = set()
        for *_, m in missings_list:
            self.__missing_modules.update(m)
        self.uiTableWidget_missing_imports.clearContents()
        self.uiTableWidget_missing_imports.setRowCount(len(missings_list))
        for index, value in enumerate(missings_list):
            # value[0] 即 filepath 为 None，依
            # ImportInspector.missing_items 返回值特点可知没有可以打开的文件
            if value[0] is None:
                break
            self.uiTableWidget_missing_imports.setVerticalHeaderItem(
                index, QTableWidgetItem(f" {index + 1} ")
            )
            item1 = QTableWidgetItem(os.path.basename(value[0]))
            item2 = QTableWidgetItem("，".join(value[1]))
            item3 = QTableWidgetItem("，".join(value[2]))
            item1.setToolTip(value[0])
            item2.setToolTip("\n".join(value[1]))
            item3.setToolTip("\n".join(value[2]))
            self.uiTableWidget_missing_imports.setItem(index, 0, item1)
            self.uiTableWidget_missing_imports.setItem(index, 1, item2)
            self.uiTableWidget_missing_imports.setItem(index, 2, item3)
        self.display_window()

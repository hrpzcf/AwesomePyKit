# coding: utf-8

import os
import shutil
from platform import machine, platform

from com.mapping import import_publishing
from fastpip import PyEnv
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from settings import *
from ui import *
from utils import *
from utils.cip import ImportInspector
from utils.main import open_explorer
from utils.pyi import PyiTool
from utils.qt import QLineEditMod, QTextEditMod
from utils.venv import VirtualEnv

from .messagebox import MessageBox

QREV_NUMBER = QRegExpValidator(QRegExp(r"[0-9]*"))
QREV_FILE_NAME = QRegExpValidator(QRegExp(r'[^\\/:*?"<>|]*'))
QREV_FILE_PATH = QRegExpValidator(QRegExp(r'[^:*?"<>|]*'))


class PyinstallerToolWindow(Ui_pyinstaller_tool, QMainWindow):
    signal_update_pyinfo = pyqtSignal(str)
    signal_update_pyiinfo = pyqtSignal(str)
    signal_update_pyipbtext = pyqtSignal(str)
    PYIVER_FMT = "Pyinstaller - {}"
    COMBOBOX_DEFITEM = "当前打包配置"

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.widget_group = (
            self.tab_project_files,
            self.tab_build_control,
            self.tab_file_ver_info,
            self.tab_advanced_setup,
            self.pb_select_py_env,
            self.pb_reinstall_pyi,
            self.cb_log_level,
            self.le_output_name,
            self.pb_check_imports,
            self.pb_gen_executable,
            self.cb_prioritize_venv,
            self.uiPushButton_apply_config,
            self.uiPushButton_delete_config,
            self.uiPushButton_save_config,
        )
        self.le_vers_group = (
            self.le_file_version_0,
            self.le_file_version_1,
            self.le_file_version_2,
            self.le_file_version_3,
            self.le_product_version_0,
            self.le_product_version_1,
            self.le_product_version_2,
            self.le_product_version_3,
        )
        self.__setup_other_widgets()
        self.repo = ThreadRepo(500)
        self.pyiconfig = PyinstallerToolConfig()
        self.toolwin_venv = None
        self.toolwin_pyenv = None
        self.__handle = None
        self.pyi_tool = PyiTool()
        self.set_platform_info()
        self.__envch_win = EnvironChosenWindow(self, self.__call_env_back)
        self.__impcheck_win = ImportsCheckWindow(self)
        self.signal_slot_connection()
        self.pyi_running_mov = QMovie(":/loading.gif")
        self.pyi_running_mov.setScaledSize(QSize(16, 16))
        self.__normal_size = self.size()
        self.__venv_creating_result = 1

    def closeEvent(self, event: QCloseEvent):
        if not self.repo.is_empty():
            MessageBox(
                "提醒",
                "任务正在运行中，关闭此窗口后任务将在后台运行。\n请勿对相关目录进行任\
何操作，否则可能会造成打包失败！",
                QMessageBox.Warning,
            ).exec_()
        self.config_widgets_to_cfg()
        self.pyiconfig.save_config()

    def show(self):
        super().show()
        self.resize(self.__normal_size)
        if self.repo.is_empty():
            self.config_cfg_to_widgets(None)

    def resizeEvent(self, event: QResizeEvent):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self.__normal_size = old_size

    def __setup_other_widgets(self):
        # 替换“程序启动入口”LineEdit控件
        self.le_program_entry = QLineEditMod("file", {".py", ".pyc", ".pyw", ".spec"})
        self.le_program_entry.setToolTip(
            "要打包的程序的启动入口(*.py *.pyw *.pyc *.spec)，此项必填。\n"
            "如果指定了 SPEC 文件，则以下绝大部分项目文件及生成控制都将不生效。\n"
            "可将格式正确的文件拖放到此处。"
        )
        self.horizontalLayout_3.replaceWidget(
            self.le_program_entry_old, self.le_program_entry
        )
        self.le_program_entry_old.deleteLater()
        # 替换“其他模块搜索路径”TextEdit控件
        self.te_module_search_path = QTextEditMod("dir")
        self.te_module_search_path.setToolTip(
            "对应选项：-p, --paths\n程序的其他模块的搜索路径(模块的父目录)，此项可留空。\
\n仅当 Pyinstaller 无法自动找到模块时使用，支持将文件夹直接拖放到此处。"
        )
        self.verticalLayout_3.replaceWidget(
            self.te_module_search_path_old, self.te_module_search_path
        )
        self.te_module_search_path_old.deleteLater()
        # 替换“非源代码资源文件”LineEdit控件
        self.te_other_data = QTextEditMod("file")
        self.te_other_data.setToolTip(
            """对应选项：--add-data\n非源代码性质的其他资源文件，例如一些图片、配置文件等，此项可留空。\n"""
            """注意：资源文件需是打包前程序真正使用的资源且在项目根目录范围内，否则打包后程序可能无法运行。可将文件\
或者文件夹直接拖到此处。"""
        )
        self.verticalLayout_4.replaceWidget(self.te_other_data_old, self.te_other_data)
        self.te_other_data_old.deleteLater()
        # 替换“文件图标路径”LineEdit控件
        self.le_file_icon_path = QLineEditMod("file", {".ico", ".icns"})
        self.le_file_icon_path.setToolTip(
            "对应选项：-i, --icon\n生成的 exe 可执行文件使用的图标，支持 .ico 等图标文件。\n可将格式正确的文件拖放到此处。"
        )
        self.horizontalLayout_11.replaceWidget(
            self.le_file_icon_path_old, self.le_file_icon_path
        )
        self.le_file_icon_path_old.deleteLater()
        for line_edit in self.le_vers_group:
            line_edit.setValidator(QREV_NUMBER)
        self.le_output_name.setValidator(QREV_FILE_NAME)
        self.le_runtime_tmpdir.setValidator(QREV_FILE_NAME)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 2)

    def signal_slot_connection(self):
        self.pyi_tool.completed.connect(self.after_task_completed)
        self.pyi_tool.stdout.connect(self.te_pyi_out_stream.append)
        self.pb_select_py_env.clicked.connect(self.__envch_win.initialize)
        self.le_program_entry.textChanged.connect(self.set_le_project_root)
        self.pb_select_module_search_path.clicked.connect(
            self.set_te_module_search_path
        )
        self.pb_select_program_entry.clicked.connect(self.set_le_program_entry)
        self.pb_up_level_root.clicked.connect(lambda: self.project_root_level("up"))
        self.pb_reset_root_level.clicked.connect(
            lambda: self.project_root_level("reset")
        )
        self.pb_clear_module_search_path.clicked.connect(
            self.te_module_search_path.clear
        )
        self.pb_select_other_data.clicked.connect(self.set_te_other_data)
        self.pb_clear_other_data.clicked.connect(self.te_other_data.clear)
        self.pb_select_file_icon.clicked.connect(self.set_le_file_icon_path)
        self.pb_select_spec_dir.clicked.connect(self.set_le_spec_dir)
        self.pb_select_temp_working_dir.clicked.connect(self.set_le_temp_working_dir)
        self.pb_select_output_dir.clicked.connect(self.set_le_output_dir)
        self.pb_select_upx_search_path.clicked.connect(self.set_le_upx_search_path)
        self.pb_gen_executable.clicked.connect(self.build_executable)
        self.pb_reinstall_pyi.clicked.connect(self.reinstall_pyinstaller)
        self.pb_check_imports.clicked.connect(self.check_project_imports)
        self.__impcheck_win.pb_install_all_missing.clicked.connect(
            lambda: self.install_missings(self.__impcheck_win.all_missing_modules)
        )
        self.pb_clear_hidden_imports.clicked.connect(self.pte_hidden_imports.clear)
        self.pb_clear_exclude_module.clicked.connect(self.pte_exclude_modules.clear)
        self.uiPushButton_save_config.clicked.connect(self.store_current_config)
        self.uiPushButton_apply_config.clicked.connect(self.apply_selected_config)
        self.uiPushButton_delete_config.clicked.connect(self.delete_selected_config)
        self.signal_update_pyinfo.connect(self.lb_py_info.setText)
        self.signal_update_pyiinfo.connect(self.lb_pyi_info.setText)
        self.signal_update_pyipbtext.connect(self.pb_reinstall_pyi.setText)

    def check_project_imports(self):
        self.config_widgets_to_cfg()
        self.toolwin_venv = VirtualEnv(self.pyiconfig.curconfig.project_root)
        self.toolwin_venv.find_project_venv()
        if self.pyiconfig.curconfig.prioritize_venv:
            if not self.toolwin_venv.venv_exists:
                return MessageBox(
                    "提示",
                    "项目目录下不存在虚拟环境，请直接点击生成可执行文件，程序会引导创建虚拟环境。",
                    QMessageBox.Warning,
                ).exec_()
            environ = self.toolwin_venv
        else:
            environ = self.toolwin_pyenv
        if not environ:
            MessageBox(
                "提示",
                "还没有选择主 Python 环境或者勾选优先使用项目目录下的虚拟环境。",
                QMessageBox.Warning,
            ).exec_()
            return
        project_root = self.pyiconfig.curconfig.project_root
        if not project_root:
            MessageBox(
                "提示",
                "项目根目录未填写！",
                QMessageBox.Warning,
            ).exec_()
            return
        if not os.path.isdir(project_root):
            MessageBox(
                "提示",
                "项目根目录不存在！",
                QMessageBox.Warning,
            ).exec_()
            return
        dist_dir = self.pyiconfig.curconfig.distribution_dir
        if not dist_dir:
            dist_dir = os.path.join(project_root, "dist")
        elif not os.path.isabs(dist_dir):
            dist_dir = os.path.join(project_root, dist_dir)
        missings = list()
        self.pyi_tool.initialize(environ.env_path, project_root)
        if not self.pyi_tool.pyi_ready:
            missings.append(("打包功能核心模块", {}, {"pyinstaller"}))

        def get_missing_imps():
            inspector = ImportInspector(
                environ.env_path,
                project_root,
                [self.toolwin_venv.env_path, dist_dir],
            )
            if (
                self.pyiconfig.curconfig.encryption_key
                and "tinyaes" not in inspector.importables
            ):
                missings.append(("字节码加密功能", {}, {"tinyaes"}))
            missings.extend(inspector.get_missing_items())

        thread_check_imp = QThreadModel(get_missing_imps)
        thread_check_imp.at_start(
            self.__lock_widgets,
            lambda: self.__show_running("正在分析项目依赖在环境中的安装情况..."),
        )
        thread_check_imp.at_finish(
            self.__hide_running,
            self.__release_widgets,
            lambda: self.__impcheck_win.set_env_info(environ),
            lambda: self.__impcheck_win.checkimp_table_update(missings),
            self.__impcheck_win.show,
        )
        thread_check_imp.start()
        self.repo.put(thread_check_imp, 1)

    def set_le_program_entry(self):
        selected_file = self.__ask_file_or_dir_path(
            "选择程序启动入口",
            self.pyiconfig.curconfig.project_root,
            file_filter="脚本文件 (*.py *.pyc *.pyw *.spec)",
        )[0]
        if not selected_file:
            return
        self.le_program_entry.setText(selected_file)

    def set_le_project_root(self):
        root = os.path.dirname(self.le_program_entry.text())
        self.le_project_root.setText(root)
        self.pyiconfig.curconfig.project_root = root

    def set_te_module_search_path(self):
        selected_dir = self.__ask_file_or_dir_path(
            "其他模块搜索目录", self.pyiconfig.curconfig.project_root, cht="dir"
        )[0]
        if not selected_dir:
            return
        self.te_module_search_path.append(selected_dir)

    def set_te_other_data(self):
        selected_files = self.__ask_file_or_dir_path(
            "选择非源码资源文件", self.pyiconfig.curconfig.project_root, mult=True
        )
        if not selected_files:
            return
        self.te_other_data.append("\n".join(selected_files))

    def set_le_file_icon_path(self):
        selected_file = self.__ask_file_or_dir_path(
            "选择可执行文件图标",
            self.pyiconfig.curconfig.project_root,
            file_filter="图标文件 (*.ico *.icns)",
        )[0]
        if not selected_file:
            return
        self.le_file_icon_path.setText(selected_file)

    def set_le_spec_dir(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择SPEC文件储存目录",
            self.pyiconfig.curconfig.project_root,
            cht="dir",
        )[0]
        if not selected_dir:
            return
        self.le_spec_dir.setText(selected_dir)

    def set_le_temp_working_dir(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择临时文件目录", self.pyiconfig.curconfig.project_root, cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_temp_working_dir.setText(selected_dir)

    def set_le_output_dir(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择生成文件储存目录", self.pyiconfig.curconfig.project_root, cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_output_dir.setText(selected_dir)

    def set_le_upx_search_path(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择UPX程序搜索目录", self.pyiconfig.curconfig.project_root, cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_upx_search_path.setText(selected_dir)

    def __ask_file_or_dir_path(
        self, title="", start="", cht="file", mult=False, file_filter="所有文件 (*)"
    ):
        file_dir_paths = []
        if cht == "file" and mult:
            if not title:
                title = "选择多文件"
            path_getter = QFileDialog.getOpenFileNames
        elif cht == "file" and not mult:
            if not title:
                title = "选择文件"
            path_getter = QFileDialog.getOpenFileName
        elif cht == "dir":
            if not title:
                title = "选择文件夹"
            path_getter = QFileDialog.getExistingDirectory
        else:
            return file_dir_paths
        if cht == "file" and not mult:
            path = path_getter(self, title, start, file_filter)[0]
            if not path:
                file_dir_paths.append("")
            else:
                file_dir_paths.append(os.path.realpath(path))
        elif cht == "file" and mult:
            paths = path_getter(self, title, start, file_filter)[0]
            file_dir_paths.extend(os.path.realpath(path) for path in paths if path)
            if not file_dir_paths:
                file_dir_paths.append("")
        elif cht == "dir":
            path = path_getter(self, title, start)
            if not path:
                file_dir_paths.append("")
            else:
                file_dir_paths.append(os.path.realpath(path))
        return file_dir_paths

    def __call_env_back(self, env):
        self.toolwin_pyenv = env
        self.pyi_tool.initialize(
            self.toolwin_pyenv.env_path,
            self.pyiconfig.curconfig.project_root,
        )
        self.load_version_information_lazily(refresh=False)

    def config_cfg_to_widgets(self, cfg_name):
        if cfg_name is not None:
            self.pyiconfig.checkout_cfg(cfg_name)
        self.update_configure_combobox_items()
        self.load_version_information_lazily(refresh=True)
        self.le_program_entry.setText(self.pyiconfig.curconfig.script_path)
        self.le_project_root.setText(self.pyiconfig.curconfig.project_root)
        self.te_module_search_path.setText(
            "\n".join(self.pyiconfig.curconfig.module_paths)
        )
        self.te_other_data.setText(
            "\n".join(pg[0] for pg in self.pyiconfig.curconfig.other_datas)
        )
        self.le_file_icon_path.setText(self.pyiconfig.curconfig.icon_path)
        if self.pyiconfig.curconfig.onedir_bundle:
            self.rb_pack_to_one_dir.setChecked(True)
        else:
            self.rb_pack_to_one_file.setChecked(True)
        self.cb_execute_with_console.setChecked(
            self.pyiconfig.curconfig.provide_console
        )
        self.cb_without_confirm.setChecked(self.pyiconfig.curconfig.no_confirm)
        self.cb_use_upx.setChecked(not self.pyiconfig.curconfig.donot_use_upx)
        self.cb_clean_before_build.setChecked(self.pyiconfig.curconfig.clean_building)
        self.cb_write_info_to_exec.setChecked(self.pyiconfig.curconfig.add_verfile)
        self.le_temp_working_dir.setText(self.pyiconfig.curconfig.working_dir)
        self.le_output_dir.setText(self.pyiconfig.curconfig.distribution_dir)
        self.le_spec_dir.setText(self.pyiconfig.curconfig.spec_dir)
        self.le_upx_search_path.setText(self.pyiconfig.curconfig.upx_dir)
        self.te_upx_exclude_files.setText(
            "\n".join(self.pyiconfig.curconfig.upx_excludes)
        )
        self.le_output_name.setText(self.pyiconfig.curconfig.bundle_spec_name)
        self.cb_log_level.setCurrentText(self.pyiconfig.curconfig.log_level)
        self.set_file_ver_info_text()
        self.set_pyi_debug_options()
        self.le_runtime_tmpdir.setText(self.pyiconfig.curconfig.runtime_tmpdir)
        self.cb_prioritize_venv.setChecked(self.pyiconfig.curconfig.prioritize_venv)
        self.le_bytecode_encryption_key.setText(self.pyiconfig.curconfig.encryption_key)
        self.cb_explorer_show.setChecked(self.pyiconfig.curconfig.open_dist_folder)
        self.cb_delete_working_dir.setChecked(
            self.pyiconfig.curconfig.delete_working_dir
        )
        self.cb_delete_spec_file.setChecked(self.pyiconfig.curconfig.delete_spec_file)
        self.pte_hidden_imports.setPlainText(
            "\n".join(self.pyiconfig.curconfig.hidden_imports)
        )
        self.pte_exclude_modules.setPlainText(
            "\n".join(self.pyiconfig.curconfig.exclude_modules)
        )
        self.cb_uac_admin.setChecked(self.pyiconfig.curconfig.uac_admin)

    def config_widgets_to_cfg(self):
        self.pyiconfig.curconfig.script_path = self.le_program_entry.local_path
        self.pyiconfig.curconfig.bundle_spec_name = self.le_output_name.text()
        project_root = self.le_project_root.text()
        self.pyiconfig.curconfig.project_root = project_root
        self.pyiconfig.curconfig.module_paths = self.te_module_search_path.local_paths
        self.pyiconfig.curconfig.other_datas = self.__gen_abs_rel_groups(project_root)
        self.pyiconfig.curconfig.icon_path = self.le_file_icon_path.local_path
        self.pyiconfig.curconfig.onedir_bundle = self.rb_pack_to_one_dir.isChecked()
        self.pyiconfig.curconfig.provide_console = (
            self.cb_execute_with_console.isChecked()
        )
        self.pyiconfig.curconfig.no_confirm = self.cb_without_confirm.isChecked()
        self.pyiconfig.curconfig.donot_use_upx = not self.cb_use_upx.isChecked()
        self.pyiconfig.curconfig.clean_building = self.cb_clean_before_build.isChecked()
        self.pyiconfig.curconfig.add_verfile = self.cb_write_info_to_exec.isChecked()
        self.pyiconfig.curconfig.working_dir = self.le_temp_working_dir.text()
        self.pyiconfig.curconfig.distribution_dir = self.le_output_dir.text()
        self.pyiconfig.curconfig.spec_dir = self.le_spec_dir.text()
        self.pyiconfig.curconfig.upx_dir = self.le_upx_search_path.text()
        self.pyiconfig.curconfig.upx_excludes = [
            s for s in self.te_upx_exclude_files.toPlainText().split("\n") if s
        ]
        if self.toolwin_pyenv is not None:
            self.pyiconfig.curconfig.environ_path = self.toolwin_pyenv.env_path
        self.pyiconfig.curconfig.log_level = self.cb_log_level.currentText()
        self.pyiconfig.curconfig.version_info = self.file_ver_info_text()
        self.pyiconfig.curconfig.debug_options = self.get_pyi_debug_options()
        self.pyiconfig.curconfig.runtime_tmpdir = self.le_runtime_tmpdir.text()
        self.pyiconfig.curconfig.prioritize_venv = self.cb_prioritize_venv.isChecked()
        self.pyiconfig.curconfig.encryption_key = self.le_bytecode_encryption_key.text()
        self.pyiconfig.curconfig.open_dist_folder = self.cb_explorer_show.isChecked()
        self.pyiconfig.curconfig.delete_working_dir = (
            self.cb_delete_working_dir.isChecked()
        )
        self.pyiconfig.curconfig.delete_spec_file = self.cb_delete_spec_file.isChecked()
        self.pyiconfig.curconfig.uac_admin = self.cb_uac_admin.isChecked()
        self.pyiconfig.curconfig.hidden_imports = [
            s for s in self.pte_hidden_imports.toPlainText().split("\n") if s
        ]
        self.pyiconfig.curconfig.exclude_modules = [
            s for s in self.pte_exclude_modules.toPlainText().split("\n") if s
        ]

    def __gen_abs_rel_groups(self, starting_point):
        """获取其他要打包的文件的本地路径和与项目根目录的相对位置。"""
        other_data_local_paths = self.te_other_data.local_paths
        abs_rel_path_groups = []
        for abs_path in other_data_local_paths:
            try:
                rel_path = os.path.relpath(os.path.dirname(abs_path), starting_point)
            except Exception:
                continue
            abs_rel_path_groups.append((abs_path, rel_path))
        return abs_rel_path_groups

    def get_pyi_debug_options(self):
        return {
            "imports": self.cb_db_imports.isChecked(),
            "bootloader": self.cb_db_bootloader.isChecked(),
            "noarchive": self.cb_db_noarchive.isChecked(),
        }

    def set_pyi_debug_options(self):
        dbo = self.pyiconfig.curconfig.debug_options
        self.cb_db_imports.setChecked(dbo.get("imports", False))
        self.cb_db_bootloader.setChecked(dbo.get("bootloader", False))
        self.cb_db_noarchive.setChecked(dbo.get("noarchive", False))

    def file_ver_info_text(self):
        file_vers = tuple(int(x.text() or 0) for x in self.le_vers_group[:4])
        prod_vers = tuple(int(x.text() or 0) for x in self.le_vers_group[4:])
        return {
            "$filevers$": str(file_vers),
            "$prodvers$": str(prod_vers),
            "$CompanyName$": self.le_company_name.text(),
            "$FileDescription$": self.le_file_description.text(),
            "$FileVersion$": ".".join(map(str, file_vers)),
            "$LegalCopyright$": self.le_legal_copyright.text(),
            "$OriginalFilename$": self.le_original_filename.text(),
            "$ProductName$": self.le_product_name.text(),
            "$ProductVersion$": ".".join(map(str, prod_vers)),
            "$LegalTrademarks$": self.le_legal_trademarks.text(),
        }

    def set_file_ver_info_text(self):
        version_info = self.pyiconfig.curconfig.version_info
        self.le_file_description.setText(version_info.get("$FileDescription$", ""))
        self.le_company_name.setText(version_info.get("$CompanyName$", ""))
        for ind, val in enumerate(
            version_info.get("$FileVersion$", "0.0.0.0").split(".")
        ):
            self.le_vers_group[ind].setText(val)
        self.le_product_name.setText(version_info.get("$ProductName$", ""))
        for ind, val in enumerate(
            version_info.get("$ProductVersion$", "0.0.0.0").split(".")
        ):
            self.le_vers_group[ind + 4].setText(val)
        self.le_legal_copyright.setText(version_info.get("$LegalCopyright$", ""))
        self.le_legal_trademarks.setText(version_info.get("$LegalTrademarks$", ""))
        self.le_original_filename.setText(version_info.get("$OriginalFilename$", ""))

    def reinstall_pyinstaller(self):
        if not self.toolwin_pyenv:
            return MessageBox(
                "提示",
                "当前未选择任何 Python 环境。",
                QMessageBox.Warning,
            ).exec_()
        # NewMessageBox的exec_方法返回0才是选择"确定"按钮
        if MessageBox(
            "安装",
            "确定安装 Pyinstaller 吗？",
            QMessageBox.Question,
            (("accept", "确定"), ("reject", "取消")),
        ).exec_():
            return

        def do_reinstall_pyi():
            self.toolwin_pyenv.uninstall("pyinstaller")
            self.toolwin_pyenv.install("pyinstaller", upgrade=1)

        thread_reinstall = QThreadModel(target=do_reinstall_pyi)
        thread_reinstall.at_start(
            self.__lock_widgets,
            lambda: self.__show_running("正在安装 Pyinstaller..."),
        )
        thread_reinstall.at_finish(
            self.__hide_running,
            self.__release_widgets,
            lambda: self.load_version_information_lazily(False),
        )
        thread_reinstall.start()
        self.repo.put(thread_reinstall, 0)

    def set_platform_info(self):
        self.lb_platform_info.setText(f"{platform()}-{machine()}")

    def project_root_level(self, opt):
        root = self.le_project_root.text()
        if not root:
            return
        if opt == "up":
            self.le_project_root.setText(os.path.dirname(root))
        elif opt == "reset":
            deep = self.le_program_entry.text()
            if not deep:
                return
            self.le_project_root.setText(os.path.dirname(deep))

    def __check_requireds(self):
        self.config_widgets_to_cfg()
        program_entry = self.pyiconfig.curconfig.script_path
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
        icon_path = self.pyiconfig.curconfig.icon_path
        if icon_path != "" and not os.path.isfile(icon_path):
            MessageBox(
                "错误",
                "程序图标文件不存在！",
                QMessageBox.Critical,
            ).exec_()
            return False
        return True

    def __show_running(self, msg):
        self.lb_running_tip.setText(msg)
        self.lb_running_gif.setMovie(self.pyi_running_mov)
        self.pyi_running_mov.start()

    def __hide_running(self):
        self.pyi_running_mov.stop()
        self.lb_running_gif.clear()
        self.lb_running_tip.clear()

    def __lock_widgets(self):
        for widget in self.widget_group:
            widget.setEnabled(False)

    def __release_widgets(self):
        for widget in self.widget_group:
            widget.setEnabled(True)

    def importance_operation_start(self, string):
        def function():
            self.__lock_widgets()
            self.__show_running(string)

        return function

    def importance_operation_finish(self):
        self.__hide_running()
        self.__release_widgets()

    def __get_program_name(self):
        program_name = self.pyiconfig.curconfig.bundle_spec_name
        if not program_name:
            program_name = os.path.splitext(
                os.path.basename(self.pyiconfig.curconfig.script_path)
            )[0]
        return program_name

    def open_explorer_select_file(self):
        program_name = self.__get_program_name()
        if self.rb_pack_to_one_file.isChecked():
            sub_directory = ""
        else:
            sub_directory = program_name
        final_execfn, ext = os.path.splitext(program_name)
        if ext.lower() != ".exe":
            final_execfn = program_name
        dist_folder = self.pyiconfig.curconfig.distribution_dir
        if not dist_folder:
            dist_folder = os.path.join(self.pyiconfig.curconfig.project_root, "dist")
        elif not os.path.isabs(dist_folder):
            dist_folder = os.path.join(
                self.pyiconfig.curconfig.project_root, dist_folder
            )
        explorer_selected = (
            os.path.join(dist_folder, sub_directory, final_execfn) + ".exe"
        )
        open_explorer(explorer_selected, "select")

    def delete_spec_file(self):
        spec_file_dir = self.pyiconfig.curconfig.spec_dir
        if not spec_file_dir:
            spec_file_dir = self.pyiconfig.curconfig.project_root
        elif not os.path.isabs(spec_file_dir):
            spec_file_dir = os.path.join(
                self.pyiconfig.curconfig.project_root, spec_file_dir
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
        custom_working_dir = self.pyiconfig.curconfig.working_dir
        if not custom_working_dir:
            working_dir_root = os.path.join(
                self.pyiconfig.curconfig.project_root, "build"
            )
        elif not os.path.isabs(custom_working_dir):
            working_dir_root = os.path.join(
                self.pyiconfig.curconfig.project_root, custom_working_dir
            )
        else:
            working_dir_root = os.path.join(custom_working_dir, program_name)
        thread_delete_working = QThreadModel(shutil.rmtree, (working_dir_root, True))
        thread_delete_working.start()
        self.repo.put(thread_delete_working)

    def after_task_completed(self, retcode):
        if retcode == 0:
            if self.cb_explorer_show.isChecked():
                self.open_explorer_select_file()
            if self.cb_delete_spec_file.isChecked():
                self.delete_spec_file()
            if self.cb_delete_working_dir.isChecked():
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

    def creating_virtualenv(self):
        dist_dir = self.pyiconfig.curconfig.distribution_dir
        if not dist_dir:
            dist_dir = os.path.join(self.toolwin_venv.project, "dist")
        elif not os.path.isabs(dist_dir):
            dist_dir = os.path.join(self.toolwin_venv.project, dist_dir)
        if self.toolwin_venv.create_project_venv(self.toolwin_pyenv.interpreter):
            import_inspect = ImportInspector(
                self.toolwin_venv.env_path,
                self.toolwin_venv.project,
                [self.toolwin_venv.env_path, dist_dir],
            )
            missings = set()
            for i in import_inspect.get_missing_items():
                missings.update(i[2])
            missings.add("pyinstaller")
            if self.pyiconfig.curconfig.encryption_key:
                missings.add("tinyaes")
            for pkg in missings:
                self.toolwin_venv.install(pkg)
            self.__venv_creating_result = 0  # 虚拟环境创建成功
        else:
            self.__venv_creating_result = 1  # 虚拟环境创建不成功

    def build_executable(self):
        if not self.__check_requireds():
            return
        if self.uiComboBox_saved_config.currentIndex() != 0:
            result = MessageBox(
                "提示",
                "你选择的打包配置似乎还没有应用以使其生效，确定开始打包吗？",
                QMessageBox.Warning,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            if result != 0:
                return
        self.te_pyi_out_stream.clear()
        if self.pyiconfig.curconfig.prioritize_venv:
            self.toolwin_venv = VirtualEnv(self.pyiconfig.curconfig.project_root)
            self.__venv_creating_result = 0
            if not self.toolwin_venv.find_project_venv():
                role = MessageBox(
                    "提示",
                    "项目目录下不存在虚拟环境，请选择合适选项。",
                    QMessageBox.Warning,
                    (
                        ("accept", "使用主环境"),
                        ("destructive", "创建虚拟环境"),
                        ("reject", "取消"),
                    ),
                ).exec_()
                if role == 0:
                    using_py_path = self.pyiconfig.curconfig.environ_path
                elif role == 1:
                    if self.toolwin_pyenv is None or not self.toolwin_pyenv.env_path:
                        return MessageBox(
                            "提示",
                            "没有选择主 Python 环境或者主 Python 环境不可用。",
                            QMessageBox.Warning,
                        ).exec_()
                    thread_venv_creating = QThreadModel(self.creating_virtualenv)
                    thread_venv_creating.at_start(
                        self.__lock_widgets,
                        lambda: self.__show_running("正在创建虚拟环境并安装模块..."),
                    )
                    thread_venv_creating.at_finish(
                        self.__hide_running,
                        self.__release_widgets,
                        self.build_executable,
                    )
                    thread_venv_creating.start()
                    self.repo.put(thread_venv_creating, 0)
                    return
                else:
                    return
            else:
                if self.__venv_creating_result != 0:
                    return MessageBox(
                        "错误", "项目目录下的虚拟环境创建失败。", QMessageBox.Critical
                    ).exec_()
                using_py_path = self.toolwin_venv.env_path
        else:
            using_py_path = self.pyiconfig.curconfig.environ_path
        self.pyi_tool.initialize(
            using_py_path,
            self.pyiconfig.curconfig.project_root,
        )
        if not self.pyi_tool.pyi_ready:
            MessageBox(
                "Pyinstaller 不可用",
                "请点击右上角'选择环境'按钮选择打包环境，再点击'安装'按钮将 Pyinstaller 安装到所选的打包环境。\n"
                "如果勾选了'使用项目目录下的虚拟环境而不是以上环境'，请点击'环境检查'按钮检查环境中缺失的模块并'一键安装'。",
                QMessageBox.Warning,
            ).exec_()
            return
        self.pyi_tool.prepare_cmd(self.pyiconfig.curconfig)
        self.__handle = self.pyi_tool.handle()
        thread_build = QThreadModel(self.pyi_tool.execute_cmd)
        thread_build.at_start(
            self.__lock_widgets,
            lambda: self.__show_running("正在生成可执行文件..."),
        )
        thread_build.at_finish(self.__hide_running, self.__release_widgets)
        thread_build.start()
        self.repo.put(thread_build, 0)

    def install_missings(self, missings):
        if not missings:
            MessageBox(
                "提示",
                "没有缺失的模块，无需安装。",
            ).exec_()
            self.__impcheck_win.close()
            return
        if MessageBox(
            "安装",
            "确定将所有缺失模块安装至所选 Python 环境中吗？",
            QMessageBox.Question,
            (("accept", "确定"), ("reject", "取消")),
        ).exec_():
            return
        if self.pyiconfig.curconfig.prioritize_venv:
            environ = self.toolwin_venv
        else:
            environ = self.toolwin_pyenv

        def install_pkgs():
            names_for_install = set()
            for name in missings:
                if name not in import_publishing:
                    names_for_install.add(name)
                else:
                    names_for_install.add(import_publishing[name])
            for name in names_for_install:
                environ.install(name)

        thread_install_missings = QThreadModel(install_pkgs)
        thread_install_missings.at_start(
            self.__lock_widgets,
            lambda: self.__show_running("正在安装缺失模块..."),
            self.__impcheck_win.close,
        )
        thread_install_missings.at_finish(
            self.__hide_running,
            self.__release_widgets,
            lambda: MessageBox(
                "完成",
                "已完成安装流程，请重新检查是否安装成功。",
                QMessageBox.Information,
            ).exec_(),
        )
        thread_install_missings.start()
        self.repo.put(thread_install_missings, 0)

    def update_configure_combobox_items(self):
        self.uiComboBox_saved_config.clear()
        self.uiComboBox_saved_config.addItem(self.COMBOBOX_DEFITEM)
        self.uiComboBox_saved_config.addItems(self.pyiconfig.multicfg)

    def store_current_config(self):
        text = self.uiLineEdit_config_remark.text()
        if not text:
            return MessageBox(
                "提示",
                "还没有输入备注名称。",
            ).exec_()
        if text == self.COMBOBOX_DEFITEM:
            return MessageBox(
                "提示",
                f"不能用“{text}”作为备注名。",
            ).exec_()
        if text in self.pyiconfig.multicfg:
            result = MessageBox(
                "提示",
                f"当前配置列表已存在名为“{text}”的配置，是否覆盖？",
                QMessageBox.Warning,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            if result != 0:
                return
        self.uiLineEdit_config_remark.clear()
        self.config_widgets_to_cfg()
        self.pyiconfig.store_curcfg(text)
        self.update_configure_combobox_items()
        MessageBox("提示", f"配置已以此备注名保存：{text}。").exec_()

    def delete_selected_config(self):
        if not len(self.pyiconfig.multicfg):
            return MessageBox("提示", "没有已保存的配置。").exec_()
        text = self.uiComboBox_saved_config.currentText()
        if not text:
            return MessageBox("提示", "没有选择任何配置。").exec_()
        if text == self.COMBOBOX_DEFITEM:
            return
        if text not in self.pyiconfig.multicfg:
            return
        if (
            MessageBox(
                "提示",
                f"确认删除当前选中的配置？",
                QMessageBox.Warning,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            != 0
        ):
            return
        del self.pyiconfig.multicfg[text]
        self.update_configure_combobox_items()

    def apply_selected_config(self):
        if not len(self.pyiconfig.multicfg):
            return MessageBox("提示", "没有已保存的配置。").exec_()
        text = self.uiComboBox_saved_config.currentText()
        if not text:
            return MessageBox("提示", "没有选择任何配置。").exec_()
        if text == self.COMBOBOX_DEFITEM:
            return
        self.config_cfg_to_widgets(text)
        self.uiComboBox_saved_config.setCurrentText(self.COMBOBOX_DEFITEM)

    def load_version_information_lazily(self, refresh):
        """为显示 Python 和 Pyinstaller 版本信息这两个耗时操作提供延迟加载的方法"""

        def do_load_version_information():
            if refresh:
                python_path = self.pyiconfig.curconfig.environ_path
                if python_path:
                    self.toolwin_pyenv = PyEnv(python_path)
                    self.pyi_tool.initialize(
                        python_path, self.pyiconfig.curconfig.project_root
                    )
            if self.toolwin_pyenv is None:
                pyinfo = ""
                pyiinfo = ""
                pbtext = "安装"
            else:
                pyiinfo = self.pyi_tool.pyi_info()
                pyinfo = self.toolwin_pyenv.py_info()
                if pyiinfo == "0.0":
                    pbtext = "安装"
                else:
                    pbtext = "重新安装"
                pyiinfo = self.PYIVER_FMT.format(pyiinfo)
            self.signal_update_pyinfo.emit(pyinfo)
            self.signal_update_pyiinfo.emit(pyiinfo)
            self.signal_update_pyipbtext.emit(pbtext)

        thread_load_info = QThreadModel(do_load_version_information)
        thread_load_info.at_start(self.importance_operation_start("正在加载配置..."))
        thread_load_info.at_finish(self.importance_operation_finish)
        thread_load_info.start()
        self.repo.put(thread_load_info, 1)


class EnvironChosenWindow(Ui_environ_chosen, QMainWindow):
    def __init__(self, parent: PyinstallerToolWindow, callback):
        super().__init__(parent)
        self.setupUi(self)
        self.__normal_size = self.size()
        self.__parent = parent
        self.__envlist = None
        self.__call_back = callback
        self.lw_env_list.clicked.connect(self.__call_environ_back)

    def __env_list_update(self):
        row_size = QSize(0, 28)
        self.lw_env_list.clear()
        for env in self.__envlist:
            item = QListWidgetItem(str(env))
            item.setSizeHint(row_size)
            self.lw_env_list.addItem(item)

    def resizeEvent(self, event: QResizeEvent):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self.__normal_size = old_size

    def closeEvent(self, event: QCloseEvent):
        self.hide()
        event.ignore()

    def __call_environ_back(self):
        self.hide()
        selected = self.lw_env_list.currentRow()
        if selected != -1:
            self.__call_back(self.__envlist[selected])

    def initialize(self):
        self.show()
        self.resize(self.__normal_size)
        self.__envlist = [PyEnv(p) for p in self.__parent.pyiconfig.pypaths]
        self.__env_list_update()


class ImportsCheckWindow(Ui_imports_check, QMainWindow):  # xxxx 改为回调函数式
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self._setup_other_widgets()
        self._normal_size = self.size()
        self.pb_confirm.clicked.connect(self.close)
        self.all_missing_modules = None

    def _setup_other_widgets(self):
        self.tw_missing_imports.setColumnWidth(0, 260)
        self.tw_missing_imports.setColumnWidth(1, 350)
        self.tw_missing_imports.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )
        self.tw_missing_imports.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.Stretch
        )

    def resizeEvent(self, event: QResizeEvent):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    def show(self):
        super().show()
        self.resize(self._normal_size)

    def checkimp_table_update(self, missing_data):
        # missing_data: [(filepath, {imps...}, {missings...})...]
        if not missing_data:
            return
        self.all_missing_modules = set()
        for *_, m in missing_data:
            self.all_missing_modules.update(m)
        self.tw_missing_imports.clearContents()
        self.tw_missing_imports.setRowCount(len(missing_data))
        for rowind, value in enumerate(missing_data):
            # value[0] 即 filepath 为 None，按 ImportInspector 类
            # missing_items 特点，可知项目内没有可以打开的文件，直接中断
            if value[0] is None:
                break
            self.tw_missing_imports.setVerticalHeaderItem(
                rowind, QTableWidgetItem(f" {rowind + 1} ")
            )
            item1 = QTableWidgetItem(os.path.basename(value[0]))
            item2 = QTableWidgetItem("，".join(value[1]))
            item3 = QTableWidgetItem("，".join(value[2]))
            item1.setToolTip(value[0])
            item2.setToolTip("\n".join(value[1]))
            item3.setToolTip("\n".join(value[2]))
            self.tw_missing_imports.setItem(rowind, 0, item1)
            self.tw_missing_imports.setItem(rowind, 1, item2)
            self.tw_missing_imports.setItem(rowind, 2, item3)
        self.show()

    def set_env_info(self, env):
        if not env:
            return
        self.le_cip_cur_env.setText(str(env))

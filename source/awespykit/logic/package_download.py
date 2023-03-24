# coding: utf-8

import os
from typing import *

from com import *
from fastpip import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from settings import *
from ui import *
from utils import *

from .messagebox import MessageBox
from .query_file_path import QueryFilePath


class PackageDownloadWindow(Ui_package_download, QMainWindow, QueryFilePath):
    set_download_table = pyqtSignal(list)
    download_completed = pyqtSignal(str)
    download_status = pyqtSignal(int, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.uiComboBox_derived_from.setView(QListView())
        self.config = PackageDownloadConfig()
        self.environments: Union[List[EnvDisplayPair], None] = None
        self.__showdl_win = ShowDownloadWindow(self)
        self.signal_slot_connection()
        self.last_path = None
        self.thread_repo = ThreadRepo(500)

    def signal_slot_connection(self):
        self.uiCheckBox_use_index_url.clicked.connect(self.change_le_index_url)
        self.uiPushButton_load_from_text.clicked.connect(self.names_from_file)
        self.uiPushButton_save_as_text.clicked.connect(self.save_names_to_file)
        self.uiPushButton_save_to.clicked.connect(self.select_saved_dir)
        self.uiPushButton_clear_package_names.clicked.connect(
            self.uiPlainTextEdit_package_names.clear
        )
        self.uiPushButton_start_download.clicked.connect(
            self.start_download_package
        )
        self.download_completed.connect(self.check_download)
        self.uiPushButton_show_dllist.clicked.connect(self.__showdl_win.display)
        self.download_status.connect(self.__showdl_win.status_changed)
        self.set_download_table.connect(self.__showdl_win.setup_table)

    def change_le_index_url(self):
        self.uiLineEdit_index_url.setEnabled(
            self.uiCheckBox_use_index_url.isChecked()
        )

    def names_from_file(self):
        text, _path = self.load_from_text(self.last_path)
        if _path:
            self.last_path = _path
        if text:
            self.uiPlainTextEdit_package_names.setPlainText(text)

    def save_names_to_file(self):
        data = self.uiPlainTextEdit_package_names.toPlainText()
        _path = self.save_as_text_file(data, self.last_path)
        if _path:
            self.last_path = _path

    def select_saved_dir(self):
        dir_path = self.get_dir_path(self.last_path)
        if dir_path:
            self.last_path = dir_path
            self.uiLineEdit_save_to.setText(dir_path)

    def __store_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.config.window_size = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        if not self.thread_repo.is_empty():
            MessageBox(
                "警告",
                "有下载任务正在运行，关闭窗口并不会结束任务。",
                QMessageBox.Warning,
            ).exec_()
        self.__store_window_size()
        self.config_widgets_to_dict()
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
        if self.thread_repo.is_empty():
            self.apply_config()

    def environs_combobox_update(self):
        if not self.config.cur_pypaths:
            return
        if self.environments:
            return
        self.uiComboBox_derived_from.clear()
        self.environments = [
            EnvDisplayPair(PyEnv(p)) for p in self.config.cur_pypaths
        ]
        item_number = len(self.environments)
        if not item_number:
            return
        for i, envp in enumerate(self.environments):
            self.uiComboBox_derived_from.addItem(envp.display)
            envp.signal_connect(self.uiComboBox_derived_from.setItemText, i)
            envp.load_real_display()
        current_index = self.config.derived_from
        if current_index < 0 or current_index >= item_number:
            self.config.derived_from = current_index = 0
        self.uiComboBox_derived_from.setCurrentIndex(current_index)

    def config_widgets_to_dict(self):
        self.config.package_names = [
            s
            for s in self.uiPlainTextEdit_package_names.toPlainText().split(
                "\n"
            )
            if s
        ]
        self.config.derived_from = self.uiComboBox_derived_from.currentIndex()
        self.config.download_deps = self.uiCheckBox_download_deps.isChecked()
        download_type = (
            "unlimited"
            if self.uiRadioButton_unlimited.isChecked()
            else "no_binary"
            if self.uiRadioButton_no_binary.isChecked()
            else "only_binary"
            if self.uiRadioButton_only_binary.isChecked()
            else "prefer_binary"
        )
        self.config.download_type = download_type
        self.config.include_pre = self.uiCheckBox_include_pre.isChecked()
        self.config.ignore_requires_python = (
            self.uiCheckBox_ignore_requires_python.isChecked()
        )
        self.config.save_path = self.uiLineEdit_save_to.text()
        self.config.platform = [
            s for s in self.uiLineEdit_platform.text().split() if s
        ]
        self.config.python_version = self.uiLineEdit_python_version.text()
        self.config.implementation = (
            self.uiComboBox_implementation.currentText()
        )
        self.config.abis = [s for s in self.uiLineEdit_abis.text().split() if s]
        self.config.index_url = self.uiLineEdit_index_url.text()
        self.config.use_index_url = self.uiCheckBox_use_index_url.isChecked()

    def apply_config(self):
        self.environs_combobox_update()
        self.uiPlainTextEdit_package_names.setPlainText(
            "\n".join(self.config.package_names)
        )
        self.uiCheckBox_download_deps.setChecked(self.config.download_deps)
        download_type = self.config.download_type
        if download_type == "unlimited":
            self.uiRadioButton_unlimited.setChecked(True)
        elif download_type == "no_binary":
            self.uiRadioButton_no_binary.setChecked(True)
        elif download_type == "only_binary":
            self.uiRadioButton_only_binary.setChecked(True)
        elif download_type == "prefer_binary":
            self.uiRadioButton_prefer_binary.setChecked(True)
        else:
            self.uiRadioButton_unlimited.setChecked(True)
        self.uiCheckBox_include_pre.setChecked(self.config.include_pre)
        self.uiCheckBox_ignore_requires_python.setChecked(
            self.config.ignore_requires_python
        )
        self.uiLineEdit_save_to.setText(self.config.save_path)
        self.uiLineEdit_platform.setText(" ".join(self.config.platform))
        self.uiLineEdit_python_version.setText(self.config.python_version)
        self.uiComboBox_implementation.setCurrentText(
            self.config.implementation
        )
        self.uiLineEdit_abis.setText(" ".join(self.config.abis))
        use_index_url = self.config.use_index_url
        self.uiCheckBox_use_index_url.setChecked(use_index_url)
        self.uiLineEdit_index_url.setEnabled(use_index_url)
        self.uiLineEdit_index_url.setText(self.config.index_url)

    @staticmethod
    def confirm_dest_path(dest):
        # 保存位置未填写时
        if not dest:
            return True
        if not os.path.exists(dest):
            if (
                MessageBox(
                    "提示",
                    "保存目录不存在，是否创建目录？",
                    QMessageBox.Warning,
                    (("accept", "是"), ("reject", "否")),
                ).exec_()
                == 0
            ):
                try:
                    os.makedirs(dest)
                    return True
                except Exception as e:
                    MessageBox("提示", f"保存目录创建失败：\n{e}。").exec_()
                    return False
            else:
                return False
        elif os.path.isfile(dest):
            MessageBox("提示", "该位置已存在同名的文件，请修改目录路径。").exec_()
            return False
        return True

    def start_download_package(self):
        if not self.environments:
            return MessageBox(
                "提示",
                "没有可用 Python 环境，请到'包管理器'中自动或手动添加环境。",
            ).exec_()
        self.config_widgets_to_dict()
        destination = self.config.save_path
        pkg_names = self.config.package_names
        if not self.confirm_dest_path(destination):
            return
        if not pkg_names:
            return MessageBox(
                "提示",
                "没有需要下载的安装包。",
            ).exec_()
        index = self.config.derived_from
        if index < 0 or index >= len(self.environments):
            index = 0
            self.uiComboBox_derived_from.setCurrentIndex(0)
        env = self.environments[index].environ
        if not env.env_path:
            return MessageBox(
                "提示",
                "无效的 Python 环境，请检查环境是否已卸载。",
            ).exec_()
        config = self.make_configure(pkg_names)
        if not isinstance(config, dict):
            return

        def do_download():
            saved_path = ""
            self.set_download_table.emit(pkg_names)
            for ind, name in enumerate(pkg_names):
                self.download_status.emit(ind, "下载中...")
                try:
                    status = env.download(name, **config)
                    if status[0]:
                        self.download_status.emit(ind, "下载完成")
                    else:
                        self.download_status.emit(ind, "下载失败")
                except Exception:
                    status = False, ""
                    self.download_status.emit(ind, "下载失败")
                if status[1]:
                    saved_path = status[1]
            self.download_completed.emit(saved_path)

        thread_download = QThreadModel(do_download)
        thread_download.before_starting(
            lambda: self.uiPushButton_start_download.setEnabled(False)
        )
        thread_download.after_completion(
            lambda: self.uiPushButton_start_download.setEnabled(True),
        )
        thread_download.start()
        self.thread_repo.put(thread_download, 0)

    @staticmethod
    def check_download(dest):
        if not dest:
            return MessageBox(
                "提示",
                f"安装包下载失败!",
                QMessageBox.Critical,
            ).exec_()
        return MessageBox(
            "下载结束",
            f"安装包保存位置：\n{dest}",
        ).exec_()

    def make_configure(self, names):
        configure = dict()

        def unqualified():
            return (
                not configure.get("no_deps", False)
                or configure.get("no_binary", False)
                or configure.get("only_binary", False)
            )

        if not self.config.download_deps:
            configure.update(no_deps=True)
        download_type = self.config.download_type
        if download_type == "no_binary":
            configure.update(no_binary=parse_package_names(names))
        elif download_type == "only_binary":
            configure.update(only_binary=parse_package_names(names))
        elif download_type == "prefer_binary":
            configure.update(prefer_binary=True)
        if self.config.include_pre:
            configure.update(pre=True)
        if self.config.ignore_requires_python:
            configure.update(ignore_requires_python=True)
        saved_path = self.config.save_path
        if saved_path:
            configure.update(dest=saved_path)
        platform_name = self.config.platform
        if platform_name:
            if unqualified():
                return MessageBox(
                    "提示",
                    "设置'兼容平台'后，不能勾选'下载需要下载的包的依赖库'，\
不能选择'仅选择源代码包'或'仅选择二进制包'。",
                    QMessageBox.Warning,
                ).exec_()
            configure.update(platform=platform_name)
        python_version = self.config.python_version
        if python_version:
            if unqualified():
                return MessageBox(
                    "提示",
                    "设置'兼容 Python 版本'后，不能勾选'下载需要下载的包的依赖库'，\
不能选择'仅选择源代码包'或'仅选择二进制包'。",
                    QMessageBox.Warning,
                ).exec_()
            configure.update(python_version=python_version)
        impl_name = self.config.implementation
        if impl_name == "无特定实现":
            impl_name = "py"
        if impl_name:
            if unqualified():
                return MessageBox(
                    "提示",
                    "设置'兼容解释器实现'后，不能勾选'下载需要下载的包的依赖库'，\
不能选择'仅选择源代码包'或'仅选择二进制包'。",
                    QMessageBox.Warning,
                ).exec_()
            configure.update(implementation=impl_name)
        abis = self.config.abis
        if abis:
            if unqualified():
                return MessageBox(
                    "提示",
                    "设置'兼容ABI'后，不能勾选'下载需要下载的包的依赖库'，\
不能选择'仅选择源代码包'或'仅选择二进制包'。",
                    QMessageBox.Warning,
                ).exec_()
            if not (platform_name and python_version and impl_name):
                return MessageBox(
                    "提示",
                    "当指定ABI时，通常需同时指定'兼容平台'、'兼容 Python 版本'、\
'兼容解释器实现'三个下载条件。",
                ).exec_()
            configure.update(abis=abis)
        index_url = self.config.index_url
        if self.config.use_index_url and index_url:
            configure.update(index_url=index_url)
        return configure


class ShowDownloadWindow(Ui_show_download, QMainWindow):
    def __init__(self, parent: PackageDownloadWindow):
        self.__parent = parent
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self._setup_other_widgets()

    def status_changed(self, index, status):
        if index >= self.uiTableWidget_downloading.rowCount():
            return False
        item = self.uiTableWidget_downloading.item(index, 1)
        if item is None:
            item = QTableWidgetItem("等待下载")
            self.uiTableWidget_downloading.setItem(index, 1, item)
        item.setText(status)
        if "下载中" in status:
            item.setData(Qt.UserRole, RoleData.Warning)
        elif "失败" in status:
            item.setData(Qt.UserRole, RoleData.Failed)
        elif "完成" in status:
            item.setData(Qt.UserRole, RoleData.Success)
        return True

    def setup_table(self, iterable):
        self.uiTableWidget_downloading.clearContents()
        self.uiTableWidget_downloading.setRowCount(len(iterable))
        for index, pkg_name in enumerate(iterable):
            item1 = QTableWidgetItem(pkg_name)
            item2 = QTableWidgetItem("等待下载")
            self.uiTableWidget_downloading.setItem(index, 0, item1)
            self.uiTableWidget_downloading.setItem(index, 1, item2)

    def _setup_other_widgets(self):
        horiz_head = self.uiTableWidget_downloading.horizontalHeader()
        horiz_head.setSectionResizeMode(0, QHeaderView.Stretch)
        horiz_head.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.uiTableWidget_downloading.setItemDelegateForColumn(
            1, ItemDelegate(self.uiTableWidget_downloading)
        )

    def __store_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__parent.config.dlstatus_winsize = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        self.__store_window_size()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

    def display(self):
        self.resize(*self.__parent.config.dlstatus_winsize)
        self.showNormal()

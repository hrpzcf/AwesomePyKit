# coding: utf-8

import os

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
        self.env_paths = None
        self.environments = None
        self.config = PackageDownloadConfig()
        self.__showdl_win = ShowDownloadWindow(self)
        self.signal_slot_connection()
        self.last_path = None
        self.thread_repo = ThreadRepo(500)

    def signal_slot_connection(self):
        self.cb_use_index_url.clicked.connect(self.change_le_index_url)
        self.pb_load_from_text.clicked.connect(self.names_from_file)
        self.pb_save_as_text.clicked.connect(self.save_names_to_file)
        self.pb_save_to.clicked.connect(self.select_saved_dir)
        self.pb_clear_package_names.clicked.connect(self.pte_package_names.clear)
        self.pb_start_download.clicked.connect(self.start_download_package)
        self.download_completed.connect(self.check_download)
        self.pb_show_dl_list.clicked.connect(self.__showdl_win.display)
        self.download_status.connect(self.__showdl_win.status_changed)
        self.set_download_table.connect(self.__showdl_win.setup_table)

    def change_le_index_url(self):
        self.le_index_url.setEnabled(self.cb_use_index_url.isChecked())

    def names_from_file(self):
        text, _path = self.load_from_text(self.last_path)
        if _path:
            self.last_path = _path
        if text:
            self.pte_package_names.setPlainText(text)

    def save_names_to_file(self):
        data = self.pte_package_names.toPlainText()
        _path = self.save_as_text_file(data, self.last_path)
        if _path:
            self.last_path = _path

    def select_saved_dir(self):
        dir_path = self.get_dir_path(self.last_path)
        if dir_path:
            self.last_path = dir_path
            self.le_save_to.setText(dir_path)

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

    def display(self):
        self.resize(*self.config.window_size)
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()
        if self.thread_repo.is_empty():
            self.apply_config()

    def update_envpaths_and_combobox(self):
        if self.env_paths is None:
            self.env_paths = list()
        else:
            self.env_paths.clear()
        self.env_paths.extend(self.config.cur_pypaths)
        self.environments = [PyEnv(p) for p in self.env_paths]
        index = self.config.derived_from
        text_list = [str(e) for e in self.environments]
        if index < 0 or index >= len(text_list):
            index = 0
        self.cmb_derived_from.clear()
        self.cmb_derived_from.addItems(text_list)
        self.cmb_derived_from.setCurrentIndex(index)

    def config_widgets_to_dict(self):
        self.config.package_names = [
            s for s in self.pte_package_names.toPlainText().split("\n") if s
        ]
        self.config.derived_from = self.cmb_derived_from.currentIndex()
        self.config.download_deps = self.cb_download_deps.isChecked()
        download_type = (
            "unlimited"
            if self.rb_unlimited.isChecked()
            else "no_binary"
            if self.rb_no_binary.isChecked()
            else "only_binary"
            if self.rb_only_binary.isChecked()
            else "prefer_binary"
        )
        self.config.download_type = download_type
        self.config.include_pre = self.cb_include_pre.isChecked()
        self.config.ignore_requires_python = (
            self.cb_ignore_requires_python.isChecked()
        )
        self.config.save_path = self.le_save_to.text()
        self.config.platform = [s for s in self.le_platform.text().split() if s]
        self.config.python_version = self.le_python_version.text()
        self.config.implementation = self.cmb_implementation.currentText()
        self.config.abis = [s for s in self.le_abis.text().split() if s]
        self.config.index_url = self.le_index_url.text()
        self.config.use_index_url = self.cb_use_index_url.isChecked()

    def apply_config(self):
        self.update_envpaths_and_combobox()
        self.pte_package_names.setPlainText("\n".join(self.config.package_names))
        self.cb_download_deps.setChecked(self.config.download_deps)
        download_type = self.config.download_type
        if download_type == "unlimited":
            self.rb_unlimited.setChecked(True)
        elif download_type == "no_binary":
            self.rb_no_binary.setChecked(True)
        elif download_type == "only_binary":
            self.rb_only_binary.setChecked(True)
        elif download_type == "prefer_binary":
            self.rb_prefer_binary.setChecked(True)
        else:
            self.rb_unlimited.setChecked(True)
        self.cb_include_pre.setChecked(self.config.include_pre)
        self.cb_ignore_requires_python.setChecked(self.config.ignore_requires_python)
        self.le_save_to.setText(self.config.save_path)
        self.le_platform.setText(" ".join(self.config.platform))
        self.le_python_version.setText(self.config.python_version)
        self.cmb_implementation.setCurrentText(self.config.implementation)
        self.le_abis.setText(" ".join(self.config.abis))
        use_index_url = self.config.use_index_url
        self.cb_use_index_url.setChecked(use_index_url)
        self.le_index_url.setEnabled(use_index_url)
        self.le_index_url.setText(self.config.index_url)

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
                "没有任何 Python 环境，请到'包管理器'中自动或手动添加 Python 环境路径。",
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
            self.cmb_derived_from.setCurrentIndex(0)
        env = self.environments[index]
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
        thread_download.at_start(lambda: self.pb_start_download.setEnabled(False))
        thread_download.at_finish(
            lambda: self.pb_start_download.setEnabled(True),
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
        if index >= self.tw_downloading.rowCount():
            return False
        color_red = QColor(255, 0, 0)
        color_green = QColor(0, 170, 0)
        item = self.tw_downloading.item(index, 1)
        if item is None:
            item = QTableWidgetItem("等待下载")
            self.tw_downloading.setItem(index, 1, item)
        item.setText(status)
        if status == "下载失败":
            item.setForeground(color_red)
        elif status == "下载完成":
            item.setForeground(color_green)
        return True

    def clear_table(self):
        self.tw_downloading.clearContents()
        self.tw_downloading.setRowCount(0)

    def setup_table(self, iterable):
        color_gray = QColor(243, 243, 243)
        self.clear_table()
        self.tw_downloading.setRowCount(len(iterable))
        for index, pkg_name in enumerate(iterable):
            item1 = QTableWidgetItem(pkg_name)
            item2 = QTableWidgetItem("等待下载")
            if not index % 2:
                item1.setBackground(color_gray)
                item2.setBackground(color_gray)
            self.tw_downloading.setItem(index, 0, item1)
            self.tw_downloading.setItem(index, 1, item2)
        return True

    def _setup_other_widgets(self):
        horiz_head = self.tw_downloading.horizontalHeader()
        horiz_head.setSectionResizeMode(0, QHeaderView.Stretch)
        horiz_head.setSectionResizeMode(1, QHeaderView.ResizeToContents)

    def __store_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__parent.config.dlstatus_winsize = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        self.__store_window_size()

    def display(self):
        self.resize(*self.__parent.config.dlstatus_winsize)
        self.showNormal()

# coding: utf-8

################################################################################
# MIT License

# Copyright (c) 2020-2022 hrp/hrpzcf

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
################################################################################
# Formatted with black
################################################################################

import os
import shutil
import sys
from platform import machine, platform

from chardet import detect
from fastpip import VERNUM, all_py_paths, cur_py_path, parse_package_names
from PyQt5.QtCore import QRegExp, QSize, Qt, pyqtSignal
from PyQt5.QtGui import (
    QCloseEvent,
    QColor,
    QFont,
    QIcon,
    QMoveEvent,
    QMovie,
    QRegExpValidator,
    QResizeEvent,
)
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QInputDialog,
    QLabel,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QWidget,
)

from com.mapping import importable_published
from info import VERSION
from res.res import *
from settings import *
from ui import *
from utils import *
from utils.cip import ImportInspector
from utils.main import PyEnv, get_res_path, open_explorer
from utils.pyi import PyiTool
from utils.qt import QLineEditMod, QTextEditMod
from utils.venv import VirtualEnv

required_fastpip_version = (1, 0, 0)

if VERNUM[0] != required_fastpip_version[0]:
    raise Exception(
        f"当前环境的 fastpip 模块主版本号({VERNUM[0]})非本程序要求的主版本号({required_fastpip_version[0]})。"
    )
if VERNUM[1] < required_fastpip_version[1]:
    raise Exception(
        f"当前环境的 fastpip 模块次版本号({VERNUM[1]})低于本程序要求的次版本号({required_fastpip_version[1]})。"
    )

QREV_NUMBER = QRegExpValidator(QRegExp(r"[0-9]*"))
QREV_FILE_NAME = QRegExpValidator(QRegExp(r'[^\\/:*?"<>|]*'))
QREV_FILE_PATH = QRegExpValidator(QRegExp(r'[^:*?"<>|]*'))


class MainEntrance(Ui_main_entrance, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"Awespykit")
        self.__pkgmgr_win = PackageManagerWindow(self)
        self.__pyitool_win = PyinstallerToolWindow(self)
        self.__indexmgr_win = IndexUrlManagerWindow(self)
        self.__pkgdl_win = PackageDownloadWindow(self)
        self.signal_slot_connection()
        self.show()

    def signal_slot_connection(self):
        self.action_about.triggered.connect(self.__show_about)
        self.pb_pkg_mgr.clicked.connect(self.__pkgmgr_win.show)
        self.pb_pyi_tool.clicked.connect(self.__pyitool_win.show)
        self.pb_index_mgr.clicked.connect(self.__indexmgr_win.show)
        self.pb_pkg_dload.clicked.connect(self.__pkgdl_win.show)

    def closeEvent(self, event: QCloseEvent):
        if (
            self.__pkgmgr_win.repo.is_empty()
            and self.__pyitool_win.repo.is_empty()
            and self.__pkgdl_win.repo.is_empty()
        ):
            event.accept()
        else:
            role = MessageBox(
                "警告",
                "有任务正在运行...",
                QMessageBox.Warning,
                (("accept", "强制退出"), ("reject", "取消")),
            ).exec_()
            if role == 0:
                self.__pkgdl_win.repo.kill_all()
                self.__pkgmgr_win.repo.kill_all()
                self.__pyitool_win.repo.kill_all()
                event.accept()
            else:
                event.ignore()

    @staticmethod
    def __show_about():
        about_path = get_res_path("help", "About.html")
        try:
            with open(about_path, encoding="utf-8") as h:
                info = h.read().replace("0.0.0", VERSION)
                icon = QMessageBox.Information
        except Exception:
            info = f"无法打开<关于>文件：{about_path}，文件已丢失或损坏。"
            icon = QMessageBox.Critical
        MessageBox("关于", info, icon).exec_()


class PackageManagerWindow(Ui_package_manager, QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self._setup_other_widgets()
        self.config = PackageManagerSettings()
        self.__output = GenericOutputWindow(self, "输出流")
        self.__ophandle = PyEnv.register(self.__output.add_line)
        self.__install_win = PackageInstallWindow(self)
        self.signal_slot_connection()
        self.env_list = get_pyenv_list(self.config.pypaths)
        self.path_list = [env.env_path for env in self.env_list]
        self.cur_pkgs_info = {}
        self.__reverseds = [True, True, True, True]
        self.selected_env_index = -1
        self.repo = ThreadRepo(500)
        self.__normal_size = self.size()

    def _setup_other_widgets(self):
        self.tw_installed_info.setColumnWidth(0, 220)
        horiz_head = self.tw_installed_info.horizontalHeader()
        horiz_head.setSectionResizeMode(0, QHeaderView.Interactive)
        horiz_head.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        horiz_head.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        horiz_head.setSectionResizeMode(3, QHeaderView.Stretch)
        self.loading_mov = QMovie(":/loading.gif")
        self.loading_mov.setScaledSize(QSize(16, 16))

    def moveEvent(self, event: QMoveEvent):
        super().moveEvent(event)
        rect = self.geometry()
        self.__output.set_pos(rect.right() + 1, rect.top(), rect.height())

    def show_hide_output(self):
        if self.__output.isHidden():
            self.__output.clear_content()
            rect = self.geometry()
            self.__output.set_pos(rect.right() + 1, rect.top(), rect.height())
            self.__output.show()
        else:
            self.__output.hide()

    def show(self):
        self.resize(self.__normal_size)
        super().show()
        self.list_widget_pyenvs_update()
        self.lw_env_list.setCurrentRow(self.selected_env_index)

    @staticmethod
    def _stop_before_close():
        return not MessageBox(
            "警告",
            "当前有任务正在运行！\n是否尝试停止所有正在运行的任务并关闭窗口？",
            QMessageBox.Question,
            (("accept", "尝试停止并关闭"), ("reject", "取消")),
        ).exec_()

    def closeEvent(self, event: QCloseEvent):
        if not self.repo.is_empty():
            if self._stop_before_close():
                self.repo.stop_all()
                self.__output.close()
                self.table_widget_clear_pkgs()
                event.accept()
            else:
                event.ignore()
        else:
            self.__output.close()
        self.config.pypaths = self.path_list.copy()
        self.config.save_config()

    def resizeEvent(self, event: QResizeEvent):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self.__normal_size = old_size

    def show_loading(self, text):
        self.lb_loading_tip.clear()
        self.lb_loading_tip.setText(text)
        self.lb_loading_gif.clear()
        self.lb_loading_gif.setMovie(self.loading_mov)
        self.loading_mov.start()

    def hide_loading(self):
        self.loading_mov.stop()
        self.lb_loading_gif.clear()
        self.lb_loading_tip.clear()

    def signal_slot_connection(self):
        self.btn_autosearch.clicked.connect(self.auto_search_env)
        self.btn_delselected.clicked.connect(self.del_selected_py_env)
        self.btn_addmanully.clicked.connect(self.add_py_path_manully)
        self.cb_check_uncheck_all.clicked.connect(self.select_all_or_cancel_all)
        self.lw_env_list.clicked.connect(lambda: self.get_pkgs_info(0))
        self.lw_env_list.currentRowChanged.connect(self.table_widget_clear_pkgs)
        self.btn_check_for_updates.clicked.connect(self.check_cur_pkgs_for_updates)
        self.btn_install_package.clicked.connect(self.set_win_install_package_envinfo)
        self.btn_uninstall_package.clicked.connect(self.uninstall_pkgs)
        self.btn_upgrade_package.clicked.connect(self.upgrade_pkgs)
        self.btn_upgrade_all.clicked.connect(self.upgrade_all_pkgs)
        self.tw_installed_info.horizontalHeader().sectionClicked[int].connect(
            self._sort_by_column
        )
        self.tw_installed_info.clicked.connect(self._show_tip_num_selected)
        self.cb_check_uncheck_all.clicked.connect(self._show_tip_num_selected)
        self.__install_win.pb_do_install.clicked.connect(self.install_pkgs)
        self.le_search_pkgs_kwd.textChanged.connect(self.search_pkg_name_by_kwd)
        self.uiPushButton_show_output.clicked.connect(self.show_hide_output)

    def set_win_install_package_envinfo(self):
        if not self.env_list:
            return MessageBox("提示", "没有可选的 Python 环境。").exec_()
        if self.selected_env_index <= -1:
            return MessageBox("提示", "没有选择任何 Python 环境。").exec_()
        if self.selected_env_index >= len(self.env_list):
            return MessageBox("错误", "异常：当前选择下标超出范围。").exec_()
        self.__install_win.show()
        self.__install_win.set_target_env(self.env_list[self.selected_env_index])

    @staticmethod
    def judging_inclusion_relationship(string_long, keyword):
        string_long = string_long.lower()
        keyword = keyword.strip().lower()
        if len(keyword) < 2:
            return string_long.startswith(keyword)
        else:
            initial = keyword[0]
            letters_following = keyword[1:].strip()
            if not string_long.startswith(initial):
                return keyword in string_long
            return letters_following in string_long[1:]

    def search_pkg_name_by_kwd(self):
        keyword = self.le_search_pkgs_kwd.text()
        if not keyword:
            for i in range(self.tw_installed_info.rowCount()):
                self.tw_installed_info.showRow(i)
        else:
            for i in range(self.tw_installed_info.rowCount()):
                if self.judging_inclusion_relationship(
                    self.tw_installed_info.item(i, 0).text(), keyword
                ):
                    self.tw_installed_info.showRow(i)
                else:
                    self.tw_installed_info.hideRow(i)
        # 搜索功能比较简单，关键字是单独一个字母时，检索以该字母开头的模块
        # 如果不是单字母，则判断包名是否以关键词首字母开头、包名是否包含后续单词
        # 因为不确定性能是否够用，所以暂时不实现更复杂的判断

    def _show_tip_num_selected(self):
        self.lb_num_selected_items.setText(
            f"当前选中数量：{len(self.indexs_of_selected_rows())}"
        )

    def list_widget_pyenvs_update(self):
        row_size = QSize(0, 28)
        cur_py_env_index = self.lw_env_list.currentRow()
        self.lw_env_list.clear()
        for env in self.env_list:
            item = QListWidgetItem(str(env))
            item.setSizeHint(row_size)
            self.lw_env_list.addItem(item)
        if cur_py_env_index != -1:
            self.lw_env_list.setCurrentRow(cur_py_env_index)

    def table_widget_pkgs_info_update(self):
        self.lb_num_selected_items.clear()
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(len(self.cur_pkgs_info))
        color_green = QColor(0, 170, 0)
        color_red = QColor(255, 0, 0)
        color_gray = QColor(243, 243, 243)
        for rowind, pkg_name in enumerate(self.cur_pkgs_info):
            self.tw_installed_info.setVerticalHeaderItem(
                rowind, QTableWidgetItem(f" {rowind + 1} ")
            )
            item0 = QTableWidgetItem(f"{pkg_name}")
            self.tw_installed_info.setItem(rowind, 0, item0)
            even_num_row = rowind % 2
            if not even_num_row:
                item0.setBackground(color_gray)
            for colind, item_text in enumerate(
                self.cur_pkgs_info.get(pkg_name, ["", "", ""])
            ):
                item = QTableWidgetItem(f" {item_text} ")
                if colind == 2:
                    if item_text in ("升级成功", "安装成功", "卸载成功"):
                        item.setForeground(color_green)
                    elif item_text in ("升级失败", "安装失败", "卸载失败"):
                        item.setForeground(color_red)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                if not even_num_row:
                    item.setBackground(color_gray)
                self.tw_installed_info.setItem(rowind, colind + 1, item)

    def _sort_by_column(self, colind):
        if colind == 0:
            self.cur_pkgs_info = dict(
                sorted(
                    self.cur_pkgs_info.items(),
                    key=lambda x: x[0].lower(),
                    reverse=self.__reverseds[colind],
                )
            )
        else:
            self.cur_pkgs_info = dict(
                sorted(
                    self.cur_pkgs_info.items(),
                    key=lambda x: x[1][colind - 1],
                    reverse=self.__reverseds[colind],
                )
            )
        self.table_widget_pkgs_info_update()
        self.__reverseds[colind] = not self.__reverseds[colind]

    def table_widget_clear_pkgs(self):
        self.lb_num_selected_items.clear()
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(0)

    def get_pkgs_info(self, no_connect):
        self.selected_env_index = self.lw_env_list.currentRow()
        if self.selected_env_index == -1:
            return None

        def do_get_pkgs_info():
            pkgs_info = self.env_list[self.selected_env_index].pkgs_info()
            self.cur_pkgs_info.clear()
            for pkg_info in pkgs_info:
                self.cur_pkgs_info[pkg_info[0]] = [pkg_info[1], "", ""]

        thread_get_pkgs_info = QThreadModel(do_get_pkgs_info)
        if not no_connect:
            thread_get_pkgs_info.at_start(
                self.lock_widgets,
                lambda: self.show_loading("正在加载包信息..."),
            )
            thread_get_pkgs_info.at_finish(
                self.table_widget_pkgs_info_update,
                self.hide_loading,
                self.release_widgets,
            )
        thread_get_pkgs_info.start()
        self.repo.put(thread_get_pkgs_info, 1)
        return thread_get_pkgs_info

    def indexs_of_selected_rows(self):
        row_indexs = []
        for item in self.tw_installed_info.selectedItems():
            row_index = item.row()
            if row_index not in row_indexs:
                row_indexs.append(row_index)
        return row_indexs

    def select_all_or_cancel_all(self):
        if self.cb_check_uncheck_all.isChecked():
            self.tw_installed_info.selectAll()
        else:
            self.tw_installed_info.clearSelection()

    def auto_search_env(self):
        def search_env():
            for _path in all_py_paths():
                if _path.lower() in path_list_lower:
                    continue
                try:
                    env = PyEnv(_path)
                except Exception:
                    continue
                self.env_list.append(env)
                self.path_list.append(env.env_path)

        path_list_lower = [p.lower() for p in self.path_list]
        thread_search_envs = QThreadModel(search_env)
        thread_search_envs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在搜索 Python 安装目录..."),
        )
        thread_search_envs.at_finish(
            self.table_widget_clear_pkgs,
            self.list_widget_pyenvs_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_search_envs.start()
        self.repo.put(thread_search_envs, 0)

    def del_selected_py_env(self):
        cur_index = self.lw_env_list.currentRow()
        if cur_index == -1:
            return
        del self.env_list[cur_index]
        del self.path_list[cur_index]
        self.lw_env_list.removeItemWidget(self.lw_env_list.takeItem(cur_index))
        self.table_widget_clear_pkgs()

    def add_py_path_manully(self):
        input_dialog = InputDialog(
            self,
            560,
            0,
            "添加 Python 目录",
            "请输入 Python 目录路径：",
        )
        _path, ok = input_dialog.get_text()
        if not (ok and _path):
            return
        if not check_py_path(_path):
            return MessageBox(
                "警告",
                "无效的 Python 目录路径！",
                QMessageBox.Warning,
            ).exec_()
        if _path.lower() in [p.lower() for p in self.path_list]:
            return MessageBox(
                "警告",
                "要添加的 Python 目录已存在。",
                QMessageBox.Warning,
            ).exec_()
        try:
            env = PyEnv(_path)
            self.env_list.append(env)
            self.path_list.append(env.env_path)
        except Exception:
            return MessageBox(
                "警告",
                "目录添加失败，路径参数类型异常，请向开发者反馈~",
                QMessageBox.Warning,
            ).exec_()
        self.list_widget_pyenvs_update()

    def check_cur_pkgs_for_updates(self):
        if self.tw_installed_info.rowCount() == 0:
            return
        cur_row = self.lw_env_list.currentRow()
        if cur_row == -1:
            return
        thread_get_info = self.get_pkgs_info(no_connect=1)

        def do_get_outdated():
            thread_get_info.wait()
            outdateds = self.env_list[cur_row].outdated()
            for outdated_info in outdateds:
                self.cur_pkgs_info.setdefault(outdated_info[0], ["", "", ""])[
                    1
                ] = outdated_info[2]

        thread_get_outdated = QThreadModel(do_get_outdated)
        thread_get_outdated.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在检查更新..."),
        )
        thread_get_outdated.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_get_outdated.start()
        self.repo.put(thread_get_outdated, 1)

    def lock_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.lw_env_list,
            self.cb_check_uncheck_all,
            self.btn_check_for_updates,
            self.btn_install_package,
            self.btn_uninstall_package,
            self.btn_upgrade_package,
            self.btn_upgrade_all,
            self.lb_num_selected_items,
        ):
            widget.setEnabled(False)

    def release_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.lw_env_list,
            self.cb_check_uncheck_all,
            self.btn_check_for_updates,
            self.btn_install_package,
            self.btn_uninstall_package,
            self.btn_upgrade_package,
            self.btn_upgrade_all,
            self.lb_num_selected_items,
        ):
            widget.setEnabled(True)

    def install_pkgs(self):
        if not self.env_list:
            return
        cur_env = self.__install_win.current_env
        tobe_installed = self.__install_win.package_names
        if not (cur_env and tobe_installed):
            return
        include_pre = self.config.include_pre
        user = self.config.install_for_user
        use_index_url = self.config.use_index_url
        index_url = self.config.index_url if use_index_url else ""

        def do_install():
            installed = [
                [name, result]
                for name, result in loop_install(
                    cur_env,
                    tobe_installed,
                    pre=include_pre,
                    user=user,
                    index_url=index_url,
                )
            ]
            separated = parse_package_names(i[0] for i in installed)
            for i, value in enumerate(installed):
                value[0] = separated[i]
            for name, result in installed:
                item = self.cur_pkgs_info.setdefault(name, ["", "", ""])
                item[0] = "N/A"
                item[2] = "安装成功" if result else "安装失败"

        thread_install_pkgs = QThreadModel(do_install)
        thread_install_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在安装..."),
        )
        thread_install_pkgs.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_install_pkgs.start()
        self.repo.put(thread_install_pkgs, 0)

    def uninstall_pkgs(self):
        pkgs_info_keys = tuple(self.cur_pkgs_info.keys())
        pkg_indexs = self.indexs_of_selected_rows()
        pkg_names = [pkgs_info_keys[index] for index in pkg_indexs]
        if not pkg_names:
            return
        cur_env = self.env_list[self.lw_env_list.currentRow()]
        names_text = (
            "\n".join(pkg_names)
            if len(pkg_names) <= 10
            else "\n".join(("\n".join(pkg_names[:10]), "......"))
        )
        uninstall_msg_box = QMessageBox(
            QMessageBox.Question, "卸载", f"确认卸载？\n{names_text}"
        )
        uninstall_msg_box.addButton("确定", QMessageBox.AcceptRole)
        reject = uninstall_msg_box.addButton("取消", QMessageBox.RejectRole)
        uninstall_msg_box.setDefaultButton(reject)
        if uninstall_msg_box.exec_() != 0:
            return

        def do_uninstall():
            for pkg_name, code in loop_uninstall(cur_env, pkg_names):
                item = self.cur_pkgs_info.setdefault(pkg_name, ["", "", ""])
                if code:
                    item[0] = "N/A"
                item[2] = "卸载成功" if code else "卸载失败"

        thread_uninstall_pkgs = QThreadModel(do_uninstall)
        thread_uninstall_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在卸载..."),
        )
        thread_uninstall_pkgs.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_uninstall_pkgs.start()
        self.repo.put(thread_uninstall_pkgs, 0)

    def upgrade_pkgs(self):
        pkgs_info_keys = tuple(self.cur_pkgs_info.keys())
        pkg_indexs = self.indexs_of_selected_rows()
        names = [pkgs_info_keys[index] for index in pkg_indexs]
        if not names:
            return
        cur_env = self.env_list[self.lw_env_list.currentRow()]
        names_text = (
            "\n".join(names)
            if len(names) <= 10
            else "\n".join(("\n".join(names[:10]), "......"))
        )
        if (
            MessageBox(
                "升级",
                f"确认升级？\n{names_text}",
                QMessageBox.Question,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            != 0
        ):
            return

        def do_upgrade():
            for pkg, res in loop_install(cur_env, names, upgrade=True):
                item = self.cur_pkgs_info.setdefault(pkg, ["", "", ""])
                if res:
                    item[2] = "升级成功"
                    if item[1]:
                        item[0] = item[1]
                    else:
                        item[0] = "N/A"
                else:
                    item[2] = "升级失败"

        thread_upgrade_pkgs = QThreadModel(do_upgrade)
        thread_upgrade_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在升级..."),
        )
        thread_upgrade_pkgs.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_upgrade_pkgs.start()
        self.repo.put(thread_upgrade_pkgs, 0)

    def upgrade_all_pkgs(self):
        upgradeable = [item[0] for item in self.cur_pkgs_info.items() if item[1][1]]
        if not upgradeable:
            MessageBox(
                "提示",
                "请检查更新确认是否有可更新的包。",
                QMessageBox.Information,
            ).exec_()
            return
        cur_env = self.env_list[self.lw_env_list.currentRow()]
        names_text = (
            "\n".join(upgradeable)
            if len(upgradeable) <= 10
            else "\n".join(("\n".join(upgradeable[:10]), "......"))
        )
        if (
            MessageBox(
                "全部升级",
                f"确认升级？\n{names_text}",
                QMessageBox.Question,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            != 0
        ):
            return

        def do_upgrade():
            for pkg_name, code in loop_install(cur_env, upgradeable, upgrade=True):
                item = self.cur_pkgs_info.setdefault(pkg_name, ["", "", ""])
                if code and item[1]:
                    item[0] = item[1]
                item[2] = "升级成功" if code else "升级失败"

        thread_upgrade_pkgs = QThreadModel(do_upgrade)
        thread_upgrade_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在升级..."),
        )
        thread_upgrade_pkgs.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_upgrade_pkgs.start()
        self.repo.put(thread_upgrade_pkgs, 0)


class AskFilePath(QWidget):
    def load_from_text(self, last_path):
        text_path, _ = QFileDialog.getOpenFileName(
            self, "选择文本文件", last_path, "文本文件 (*.txt)"
        )
        if not text_path:
            return "", ""
        try:
            with open(text_path, "rb") as fobj:
                encoding = detect(fobj.read()).get("encoding", "utf-8")
            with open(text_path, "rt", encoding=encoding) as fobj:
                return fobj.read(), os.path.dirname(text_path)
        except Exception as reason:
            MessageBox(
                "错误",
                f"文件打开失败：\n{str(reason)}",
                QMessageBox.Critical,
            ).exec_()
            return "", ""

    def save_as_text_file(self, data, last_path):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "保存文件", last_path, "文本文件 (*.txt)"
        )
        if not save_path:
            return ""
        try:
            with open(save_path, "wt", encoding="utf-8") as fobj:
                fobj.writelines(data)
        except Exception as reason:
            return MessageBox(
                "错误",
                f"文件保存失败：\n{str(reason)}",
            ).exec_()
        return os.path.dirname(save_path)

    def get_dir_path(self, last_path):
        _path = QFileDialog.getExistingDirectory(self, "选择目录", last_path)
        if _path:
            return os.path.normpath(_path)
        return ""


class PackageInstallWindow(Ui_package_install, QMainWindow, AskFilePath):
    def __init__(self, parent: PackageManagerWindow):
        super().__init__(parent)
        self.setupUi(self)
        self._setup_other_widgets()
        self.current_env = None
        self.package_names = None
        self.signal_slot_connection()
        self.__parent = parent
        self.last_path = self.__parent.config.last_path

    def _setup_other_widgets(self):
        self.pte_package_names = QTextEditMod(
            file_filter={".whl"},
        )
        self.uiHorizontalLayout_package_name.replaceWidget(
            self.pte_package_names_old, self.pte_package_names
        )
        self.pte_package_names.show()
        self.pte_package_names_old.deleteLater()

    def save_package_names(self):
        data = self.pte_package_names.toPlainText()
        if not data:
            MessageBox("提示", "要保存的内容为空！").exec_()
            return
        last_path = self.save_as_text_file(data, self.last_path)
        if last_path:
            self.last_path = last_path
            self.__parent.config.last_path = last_path

    def load_package_names(self):
        text, fpath = self.load_from_text(self.last_path)
        if text:
            self.pte_package_names.setPlainText(text)
            self.package_names = list()
            names = text.splitlines(keepends=False)
            for name in names:
                if name and (name not in self.package_names):
                    self.package_names.append(name)
        if fpath:
            self.last_path = fpath
            self.__parent.config.last_path = fpath

    def apply_default_conf(self):
        self.cb_including_pre.setChecked(self.__parent.config.include_pre)
        self.cb_install_for_user.setChecked(self.__parent.config.install_for_user)
        self.le_use_index_url.setText(self.__parent.config.index_url)
        self.cb_use_index_url.setChecked(self.__parent.config.use_index_url)
        if self.cb_use_index_url.isChecked():
            self.le_use_index_url.setEnabled(True)
        else:
            self.le_use_index_url.setEnabled(False)
        self.pte_package_names.setPlainText(
            "\n".join(self.__parent.config.package_names)
        )

    def store_default_conf(self):
        text = self.pte_package_names.toPlainText()
        if text:
            self.package_names = [
                name for name in text.splitlines(keepends=False) if name
            ]
            self.__parent.config.package_names = self.package_names.copy()
        self.__parent.config.include_pre = self.cb_including_pre.isChecked()
        self.__parent.config.install_for_user = self.cb_install_for_user.isChecked()
        self.__parent.config.index_url = self.le_use_index_url.text()
        self.__parent.config.use_index_url = self.cb_use_index_url.isChecked()

    def closeEvent(self, event: QCloseEvent):
        event.accept()
        self.store_default_conf()
        self.__parent.config.save_config()

    def show(self):
        super().show()
        self.apply_default_conf()

    def signal_slot_connection(self):
        self.pb_do_install.clicked.connect(self.store_default_conf)
        self.pb_do_install.clicked.connect(self.close)
        self.pb_save_as_text.clicked.connect(self.save_package_names)
        self.pb_load_from_text.clicked.connect(self.load_package_names)
        self.cb_use_index_url.clicked.connect(self.set_le_use_index_url)

    def set_le_use_index_url(self):
        self.le_use_index_url.setEnabled(self.cb_use_index_url.isChecked())

    def set_target_env(self, env):
        assert isinstance(env, PyEnv), "传参错误"
        self.current_env = env
        self.uiLabel_target_environment.setText(str(env))


class IndexUrlManagerWindow(Ui_index_manager, QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.__config = IndexManagerSettings()
        self.__ordered_urls = None
        self.signal_slot_connection()
        self.__normal_size = self.size()

    def show(self):
        self.resize(self.__normal_size)
        super().show()
        self.__list_widget_urls_update()

    def resizeEvent(self, event: QResizeEvent):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self.__normal_size = old_size

    @staticmethod
    def __widget_for_list_item(name, url):
        item_layout = QHBoxLayout()
        item_layout.addWidget(QLabel(name))
        item_layout.addWidget(QLabel(url))
        item_layout.setStretch(0, 2)
        item_layout.setStretch(1, 8)
        item_widget = QWidget()
        item_widget.setLayout(item_layout)
        return item_widget

    def __list_widget_urls_update(self):
        self.li_indexurls.clear()
        self.__ordered_urls = tuple(self.__config.index_urls.items())
        for name, url in self.__ordered_urls:
            item_widget = self.__widget_for_list_item(name, url)
            li_item = QListWidgetItem()
            li_item.setSizeHint(QSize(0, 32))
            self.li_indexurls.addItem(li_item)
            self.li_indexurls.setItemWidget(li_item, item_widget)

    def signal_slot_connection(self):
        self.btn_clearle.clicked.connect(self.__clear_line_edit)
        self.btn_saveurl.clicked.connect(self.__save_index_urls)
        self.btn_delurl.clicked.connect(self.__del_index_url)
        self.li_indexurls.clicked.connect(self.__set_url_line_edit)
        self.btn_setindex.clicked.connect(self.__set_global_index_url)
        self.btn_refresh_effective.clicked.connect(self.__display_effective_url)

    def __set_url_line_edit(self):
        selected = self.li_indexurls.currentRow()
        if selected == -1:
            return
        self.le_urlname.setText(self.__ordered_urls[selected][0])
        self.le_indexurl.setText(self.__ordered_urls[selected][1])

    def __clear_line_edit(self):
        self.le_urlname.clear()
        self.le_indexurl.clear()

    def __check_name_url(self, name, url):
        def error(m):
            return MessageBox("错误", m, QMessageBox.Critical)

        if not name:
            msgbox = error("名称不能为空！")
        elif not url:
            msgbox = error("地址不能为空！")
        elif not check_index_url(url):
            msgbox = error("无效的镜像源地址！")
        elif name in self.__config.index_urls:
            msgbox = error(f"名称'{name}'已存在！")
        else:
            return True
        return msgbox.exec_()  # 无论如何都返回 0

    def __save_index_urls(self):
        name = self.le_urlname.text()
        url = self.le_indexurl.text()
        if self.__check_name_url(name, url):
            self.__config.index_urls[name] = url
        self.__list_widget_urls_update()
        self.__config.save_config()

    def __del_index_url(self):
        selected = self.li_indexurls.currentRow()
        if selected == -1:
            return MessageBox(
                "提示",
                "没有选中列表内的任何条目。",
            ).exec_()
        del self.__config.index_urls[self.__ordered_urls[selected][0]]
        self.__list_widget_urls_update()
        items_count = self.li_indexurls.count()
        if items_count:
            if selected == -1:
                self.li_indexurls.setCurrentRow(0)
            else:
                should_be_selected = (
                    0
                    if selected == 0
                    else selected
                    if selected < items_count
                    else items_count - 1
                )
                self.li_indexurls.setCurrentRow(should_be_selected)
        self.__config.save_config()

    def __get_cur_environ(self):
        """
        首先使用配置文件中保存的 Python 路径实例化一个 PyEnv，如果路径为空，
        则使用系统环境变量 PATH 中第一个 Python 路径，环境变量中还未找到则返回 None。
        """
        cur_pypaths = self.__config.cur_pypaths
        if not cur_pypaths:
            return PyEnv(cur_py_path())
        for _path in cur_pypaths:
            environ = PyEnv(_path)
            if not environ.env_path:
                continue
            return environ
        else:
            MessageBox(
                "提示",
                "没有找到 Python 环境，请在<包管理器>中添加 Python 目录。",
                QMessageBox.Warning,
            ).exec_()

    def __set_global_index_url(self):
        def warning(m):
            return MessageBox("提示", m, QMessageBox.Warning)

        url = self.le_indexurl.text()
        if not url:
            warn_box = warning("要设置为全局镜像源的地址不能为空！")
        elif not check_index_url(url):
            warn_box = warning("镜像源地址不符合 pip 镜像源地址格式。")
        else:
            environ = self.__get_cur_environ()
            if not environ:
                warn_box = warning(
                    "没找到 Python 环境，全局镜像源设置失败。\n请在<包管理器>中添加 Python 环境。",
                )
            elif environ.set_global_index(url):
                warn_box = MessageBox("提示", f"全局镜像源地址设置成功：\n{url}")
            else:
                warn_box = warning(
                    "全局镜像源设置失败，请确保<包管理器>中第一个环境的 pip 可用或系统环境变量 PATH 中有可用的 Python 路径。"
                )
        warn_box.exec_()

    def __display_effective_url(self):
        environ = self.__get_cur_environ()
        if not environ:
            self.le_effectiveurl.setText("没找到 Python 环境，无法获取镜像源地址。")
            return
        self.le_effectiveurl.setText(
            environ.get_global_index() or "无效的 Python 环境或当前全局镜像源地址为空。"
        )


class PyinstallerToolWindow(Ui_pyinstaller_tool, QMainWindow):
    pyiver_fmt = "Pyinstaller - {}"
    signal_update_pyinfo = pyqtSignal(str)
    signal_update_pyiinfo = pyqtSignal(str)
    signal_update_pyipbtext = pyqtSignal(str)

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
        self.COMBOBOX_NAME = "当前打包配置"
        self.pyi_config = PyinstallerToolSettings()
        self.toolwin_venv = None
        self.toolwin_pyenv = None
        self.__handle = None
        self.pyi_tool = PyiTool()
        self.set_platform_info()
        self.__chosen_win = EnvironChosenWindow(self)
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
        self.pyi_config.save_config()

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
        self.pb_select_py_env.clicked.connect(self.__chosen_win.show)
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
        self.toolwin_venv = VirtualEnv(self.pyi_config.curconfig.project_root)
        self.toolwin_venv.find_project_venv()
        if self.pyi_config.curconfig.prioritize_venv:
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
        project_root = self.pyi_config.curconfig.project_root
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
        dist_dir = self.pyi_config.curconfig.distribution_dir
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
                self.pyi_config.curconfig.encryption_key
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
            self.pyi_config.curconfig.project_root,
            file_filter="脚本文件 (*.py *.pyc *.pyw *.spec)",
        )[0]
        if not selected_file:
            return
        self.le_program_entry.setText(selected_file)

    def set_le_project_root(self):
        root = os.path.dirname(self.le_program_entry.text())
        self.le_project_root.setText(root)
        self.pyi_config.curconfig.project_root = root

    def set_te_module_search_path(self):
        selected_dir = self.__ask_file_or_dir_path(
            "其他模块搜索目录", self.pyi_config.curconfig.project_root, cht="dir"
        )[0]
        if not selected_dir:
            return
        self.te_module_search_path.append(selected_dir)

    def set_te_other_data(self):
        selected_files = self.__ask_file_or_dir_path(
            "选择非源码资源文件", self.pyi_config.curconfig.project_root, mult=True
        )
        if not selected_files:
            return
        self.te_other_data.append("\n".join(selected_files))

    def set_le_file_icon_path(self):
        selected_file = self.__ask_file_or_dir_path(
            "选择可执行文件图标",
            self.pyi_config.curconfig.project_root,
            file_filter="图标文件 (*.ico *.icns)",
        )[0]
        if not selected_file:
            return
        self.le_file_icon_path.setText(selected_file)

    def set_le_spec_dir(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择SPEC文件储存目录",
            self.pyi_config.curconfig.project_root,
            cht="dir",
        )[0]
        if not selected_dir:
            return
        self.le_spec_dir.setText(selected_dir)

    def set_le_temp_working_dir(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择临时文件目录", self.pyi_config.curconfig.project_root, cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_temp_working_dir.setText(selected_dir)

    def set_le_output_dir(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择生成文件储存目录", self.pyi_config.curconfig.project_root, cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_output_dir.setText(selected_dir)

    def set_le_upx_search_path(self):
        selected_dir = self.__ask_file_or_dir_path(
            "选择UPX程序搜索目录", self.pyi_config.curconfig.project_root, cht="dir"
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

    def select_env_update(self):
        self.toolwin_pyenv = self.__chosen_win.envlist[
            self.__chosen_win.lw_env_list.currentRow()
        ]
        self.pyi_tool.initialize(
            self.toolwin_pyenv.env_path,
            self.pyi_config.curconfig.project_root,
        )
        self.load_version_information_lazily(refresh=False)

    def config_cfg_to_widgets(self, cfg_name):
        if cfg_name is not None:
            self.pyi_config.checkout_cfg(cfg_name)
        self.update_configure_combobox_items()
        self.load_version_information_lazily(refresh=True)
        self.le_program_entry.setText(self.pyi_config.curconfig.script_path)
        self.le_project_root.setText(self.pyi_config.curconfig.project_root)
        self.te_module_search_path.setText(
            "\n".join(self.pyi_config.curconfig.module_paths)
        )
        self.te_other_data.setText(
            "\n".join(pg[0] for pg in self.pyi_config.curconfig.other_datas)
        )
        self.le_file_icon_path.setText(self.pyi_config.curconfig.icon_path)
        if self.pyi_config.curconfig.onedir_bundle:
            self.rb_pack_to_one_dir.setChecked(True)
        else:
            self.rb_pack_to_one_file.setChecked(True)
        self.cb_execute_with_console.setChecked(
            self.pyi_config.curconfig.provide_console
        )
        self.cb_without_confirm.setChecked(self.pyi_config.curconfig.no_confirm)
        self.cb_use_upx.setChecked(not self.pyi_config.curconfig.donot_use_upx)
        self.cb_clean_before_build.setChecked(self.pyi_config.curconfig.clean_building)
        self.cb_write_info_to_exec.setChecked(self.pyi_config.curconfig.add_verfile)
        self.le_temp_working_dir.setText(self.pyi_config.curconfig.working_dir)
        self.le_output_dir.setText(self.pyi_config.curconfig.distribution_dir)
        self.le_spec_dir.setText(self.pyi_config.curconfig.spec_dir)
        self.le_upx_search_path.setText(self.pyi_config.curconfig.upx_dir)
        self.te_upx_exclude_files.setText(
            "\n".join(self.pyi_config.curconfig.upx_excludes)
        )
        self.le_output_name.setText(self.pyi_config.curconfig.bundle_spec_name)
        self.cb_log_level.setCurrentText(self.pyi_config.curconfig.log_level)
        self.set_file_ver_info_text()
        self.set_pyi_debug_options()
        self.le_runtime_tmpdir.setText(self.pyi_config.curconfig.runtime_tmpdir)
        self.cb_prioritize_venv.setChecked(self.pyi_config.curconfig.prioritize_venv)
        self.le_bytecode_encryption_key.setText(
            self.pyi_config.curconfig.encryption_key
        )
        self.cb_explorer_show.setChecked(self.pyi_config.curconfig.open_dist_folder)
        self.cb_delete_working_dir.setChecked(
            self.pyi_config.curconfig.delete_working_dir
        )
        self.cb_delete_spec_file.setChecked(self.pyi_config.curconfig.delete_spec_file)
        self.pte_hidden_imports.setPlainText(
            "\n".join(self.pyi_config.curconfig.hidden_imports)
        )
        self.pte_exclude_modules.setPlainText(
            "\n".join(self.pyi_config.curconfig.exclude_modules)
        )
        self.cb_uac_admin.setChecked(self.pyi_config.curconfig.uac_admin)

    def config_widgets_to_cfg(self):
        self.pyi_config.curconfig.script_path = self.le_program_entry.local_path
        self.pyi_config.curconfig.bundle_spec_name = self.le_output_name.text()
        project_root = self.le_project_root.text()
        self.pyi_config.curconfig.project_root = project_root
        self.pyi_config.curconfig.module_paths = self.te_module_search_path.local_paths
        self.pyi_config.curconfig.other_datas = self.__gen_abs_rel_groups(project_root)
        self.pyi_config.curconfig.icon_path = self.le_file_icon_path.local_path
        self.pyi_config.curconfig.onedir_bundle = self.rb_pack_to_one_dir.isChecked()
        self.pyi_config.curconfig.provide_console = (
            self.cb_execute_with_console.isChecked()
        )
        self.pyi_config.curconfig.no_confirm = self.cb_without_confirm.isChecked()
        self.pyi_config.curconfig.donot_use_upx = not self.cb_use_upx.isChecked()
        self.pyi_config.curconfig.clean_building = (
            self.cb_clean_before_build.isChecked()
        )
        self.pyi_config.curconfig.add_verfile = self.cb_write_info_to_exec.isChecked()
        self.pyi_config.curconfig.working_dir = self.le_temp_working_dir.text()
        self.pyi_config.curconfig.distribution_dir = self.le_output_dir.text()
        self.pyi_config.curconfig.spec_dir = self.le_spec_dir.text()
        self.pyi_config.curconfig.upx_dir = self.le_upx_search_path.text()
        self.pyi_config.curconfig.upx_excludes = [
            s for s in self.te_upx_exclude_files.toPlainText().split("\n") if s
        ]
        if self.toolwin_pyenv is not None:
            self.pyi_config.curconfig.environ_path = self.toolwin_pyenv.env_path
        self.pyi_config.curconfig.log_level = self.cb_log_level.currentText()
        self.pyi_config.curconfig.version_info = self.file_ver_info_text()
        self.pyi_config.curconfig.debug_options = self.get_pyi_debug_options()
        self.pyi_config.curconfig.runtime_tmpdir = self.le_runtime_tmpdir.text()
        self.pyi_config.curconfig.prioritize_venv = self.cb_prioritize_venv.isChecked()
        self.pyi_config.curconfig.encryption_key = (
            self.le_bytecode_encryption_key.text()
        )
        self.pyi_config.curconfig.open_dist_folder = self.cb_explorer_show.isChecked()
        self.pyi_config.curconfig.delete_working_dir = (
            self.cb_delete_working_dir.isChecked()
        )
        self.pyi_config.curconfig.delete_spec_file = (
            self.cb_delete_spec_file.isChecked()
        )
        self.pyi_config.curconfig.uac_admin = self.cb_uac_admin.isChecked()
        self.pyi_config.curconfig.hidden_imports = [
            s for s in self.pte_hidden_imports.toPlainText().split("\n") if s
        ]
        self.pyi_config.curconfig.exclude_modules = [
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
        dbo = self.pyi_config.curconfig.debug_options
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
        version_info = self.pyi_config.curconfig.version_info
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
        program_entry = self.pyi_config.curconfig.script_path
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
        icon_path = self.pyi_config.curconfig.icon_path
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
        program_name = self.pyi_config.curconfig.bundle_spec_name
        if not program_name:
            program_name = os.path.splitext(
                os.path.basename(self.pyi_config.curconfig.script_path)
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
        dist_folder = self.pyi_config.curconfig.distribution_dir
        if not dist_folder:
            dist_folder = os.path.join(self.pyi_config.curconfig.project_root, "dist")
        elif not os.path.isabs(dist_folder):
            dist_folder = os.path.join(
                self.pyi_config.curconfig.project_root, dist_folder
            )
        explorer_selected = (
            os.path.join(dist_folder, sub_directory, final_execfn) + ".exe"
        )
        open_explorer(explorer_selected, "select")

    def delete_spec_file(self):
        spec_file_dir = self.pyi_config.curconfig.spec_dir
        if not spec_file_dir:
            spec_file_dir = self.pyi_config.curconfig.project_root
        elif not os.path.isabs(spec_file_dir):
            spec_file_dir = os.path.join(
                self.pyi_config.curconfig.project_root, spec_file_dir
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
        custom_working_dir = self.pyi_config.curconfig.working_dir
        if not custom_working_dir:
            working_dir_root = os.path.join(
                self.pyi_config.curconfig.project_root, "build"
            )
        elif not os.path.isabs(custom_working_dir):
            working_dir_root = os.path.join(
                self.pyi_config.curconfig.project_root, custom_working_dir
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
        dist_dir = self.pyi_config.curconfig.distribution_dir
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
            if self.pyi_config.curconfig.encryption_key:
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
        if self.pyi_config.curconfig.prioritize_venv:
            self.toolwin_venv = VirtualEnv(self.pyi_config.curconfig.project_root)
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
                    using_py_path = self.pyi_config.curconfig.environ_path
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
                # TODO 最好能实现在此分支下做环境中模块的检查，使用 NewTask 的 at_finish
                # 重新执行 build_executable，但又不会因某模块安装失败而导致无限进入此分支
                using_py_path = self.toolwin_venv.env_path
        else:
            using_py_path = self.pyi_config.curconfig.environ_path
        self.pyi_tool.initialize(
            using_py_path,
            self.pyi_config.curconfig.project_root,
        )
        if not self.pyi_tool.pyi_ready:
            MessageBox(
                "Pyinstaller 不可用",
                "请点击右上角'选择环境'按钮选择打包环境，再点击'安装'按钮将 Pyinstaller 安装到所选的打包环境。\n"
                "如果勾选了'使用项目目录下的虚拟环境而不是以上环境'，请点击'环境检查'按钮检查环境中缺失的模块并'一键安装'。",
                QMessageBox.Warning,
            ).exec_()
            return
        self.pyi_tool.prepare_cmd(self.pyi_config.curconfig)
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
        if self.pyi_config.curconfig.prioritize_venv:
            environ = self.toolwin_venv
        else:
            environ = self.toolwin_pyenv

        def install_pkgs():
            names_for_install = set()
            for name in missings:
                if name not in importable_published:
                    names_for_install.add(name)
                else:
                    names_for_install.add(importable_published[name])
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
        self.uiComboBox_saved_config.addItem(self.COMBOBOX_NAME)
        self.uiComboBox_saved_config.addItems(self.pyi_config.multicfg)

    def store_current_config(self):
        text = self.uiLineEdit_config_remark.text()
        if not text:
            return MessageBox(
                "提示",
                "还没有输入备注名称。",
            ).exec_()
        if text == self.COMBOBOX_NAME:
            return MessageBox(
                "提示",
                f"不能用“{text}”作为备注名。",
            ).exec_()
        if text in self.pyi_config.multicfg:
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
        self.pyi_config.store_curcfg(text)
        self.update_configure_combobox_items()
        MessageBox("提示", f"配置已以此备注名保存：{text}。").exec_()

    def delete_selected_config(self):
        if not len(self.pyi_config.multicfg):
            return MessageBox("提示", "没有已保存的配置。").exec_()
        text = self.uiComboBox_saved_config.currentText()
        if not text:
            return MessageBox("提示", "没有选择任何配置。").exec_()
        if text == self.COMBOBOX_NAME:
            return
        if text not in self.pyi_config.multicfg:
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
        del self.pyi_config.multicfg[text]
        self.update_configure_combobox_items()

    def apply_selected_config(self):
        if not len(self.pyi_config.multicfg):
            return MessageBox("提示", "没有已保存的配置。").exec_()
        text = self.uiComboBox_saved_config.currentText()
        if not text:
            return MessageBox("提示", "没有选择任何配置。").exec_()
        if text == self.COMBOBOX_NAME:
            return
        self.config_cfg_to_widgets(text)
        self.uiComboBox_saved_config.setCurrentText(self.COMBOBOX_NAME)

    def load_version_information_lazily(self, refresh):
        """为显示 Python 和 Pyinstaller 版本信息这两个耗时操作提供延迟加载的方法"""

        def do_load_version_information():
            if refresh:
                python_path = self.pyi_config.curconfig.environ_path
                if python_path:
                    self.toolwin_pyenv = PyEnv(python_path)
                    self.pyi_tool.initialize(
                        python_path, self.pyi_config.curconfig.project_root
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
                pyiinfo = self.pyiver_fmt.format(pyiinfo)
            self.signal_update_pyinfo.emit(pyinfo)
            self.signal_update_pyiinfo.emit(pyiinfo)
            self.signal_update_pyipbtext.emit(pbtext)

        thread_load_info = QThreadModel(do_load_version_information)
        thread_load_info.at_start(self.importance_operation_start("正在加载配置..."))
        thread_load_info.at_finish(self.importance_operation_finish)
        thread_load_info.start()
        self.repo.put(thread_load_info, 1)


class EnvironChosenWindow(Ui_environ_chosen, QMainWindow):
    def __init__(self, parent: PyinstallerToolWindow):
        super().__init__(parent)
        self.setupUi(self)
        self.signal_slot_connection()
        self._normal_size = self.size()
        self.__parent = parent
        self.envlist = None

    def signal_slot_connection(self):
        self.lw_env_list.pressed.connect(self.close)

    def pyenv_list_update(self):
        row_size = QSize(0, 28)
        self.lw_env_list.clear()
        for env in self.envlist:
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
            self._normal_size = old_size

    def close(self):
        super().close()
        self.__parent.select_env_update()

    def show(self):
        self.resize(self._normal_size)
        self.envlist = get_pyenv_list(self.__parent.pyi_config.pypaths)
        super().show()
        self.pyenv_list_update()


class ImportsCheckWindow(Ui_imports_check, QMainWindow):
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
        self.resize(self._normal_size)
        super().show()

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
            # value[0] 即 filepath 为 None，按照 ImportInspector 类
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


class PackageDownloadWindow(Ui_package_download, QMainWindow, AskFilePath):
    set_download_table = pyqtSignal(list)
    download_completed = pyqtSignal(str)
    download_status = pyqtSignal(int, str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.env_paths = None
        self.environments = None
        self.__pdconfig = PackageDownloadSettings()
        self.__showdl_win = ShowDownloadWindow(self)
        self.signal_slot_connection()
        self.last_path = None
        self.repo = ThreadRepo(500)

    def signal_slot_connection(self):
        self.cb_use_index_url.clicked.connect(self.change_le_index_url)
        self.pb_load_from_text.clicked.connect(self.names_from_file)
        self.pb_save_as_text.clicked.connect(self.save_names_to_file)
        self.pb_save_to.clicked.connect(self.select_saved_dir)
        self.pb_clear_package_names.clicked.connect(self.pte_package_names.clear)
        self.pb_start_download.clicked.connect(self.start_download_package)
        self.download_completed.connect(self.check_download)
        self.pb_show_dl_list.clicked.connect(self.__showdl_win.show)
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

    def closeEvent(self, event: QCloseEvent):
        if not self.repo.is_empty():
            MessageBox(
                "警告",
                "有下载任务正在运行，关闭窗口并不会结束任务。",
                QMessageBox.Warning,
            ).exec_()
        super().closeEvent(event)
        self.config_widgets_to_dict()
        self.__pdconfig.save_config()

    def show(self):
        super().show()
        if self.repo.is_empty():
            self.apply_config()

    def update_envpaths_and_combobox(self):
        if self.env_paths is None:
            self.env_paths = list()
        else:
            self.env_paths.clear()
        self.env_paths.extend(self.__pdconfig.cur_pypaths)
        self.environments = get_pyenv_list(self.env_paths)
        index = self.__pdconfig.derived_from
        text_list = [str(e) for e in self.environments]
        if index < 0 or index >= len(text_list):
            index = 0
        self.cmb_derived_from.clear()
        self.cmb_derived_from.addItems(text_list)
        self.cmb_derived_from.setCurrentIndex(index)

    def config_widgets_to_dict(self):
        self.__pdconfig.package_names = [
            s for s in self.pte_package_names.toPlainText().split("\n") if s
        ]
        self.__pdconfig.derived_from = self.cmb_derived_from.currentIndex()
        self.__pdconfig.download_deps = self.cb_download_deps.isChecked()
        download_type = (
            "unlimited"
            if self.rb_unlimited.isChecked()
            else "no_binary"
            if self.rb_no_binary.isChecked()
            else "only_binary"
            if self.rb_only_binary.isChecked()
            else "prefer_binary"
        )
        self.__pdconfig.download_type = download_type
        self.__pdconfig.include_pre = self.cb_include_pre.isChecked()
        self.__pdconfig.ignore_requires_python = (
            self.cb_ignore_requires_python.isChecked()
        )
        self.__pdconfig.save_path = self.le_save_to.text()
        self.__pdconfig.platform = [s for s in self.le_platform.text().split() if s]
        self.__pdconfig.python_version = self.le_python_version.text()
        self.__pdconfig.implementation = self.cmb_implementation.currentText()
        self.__pdconfig.abis = [s for s in self.le_abis.text().split() if s]
        self.__pdconfig.index_url = self.le_index_url.text()
        self.__pdconfig.use_index_url = self.cb_use_index_url.isChecked()

    def apply_config(self):
        self.update_envpaths_and_combobox()
        self.pte_package_names.setPlainText("\n".join(self.__pdconfig.package_names))
        self.cb_download_deps.setChecked(self.__pdconfig.download_deps)
        download_type = self.__pdconfig.download_type
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
        self.cb_include_pre.setChecked(self.__pdconfig.include_pre)
        self.cb_ignore_requires_python.setChecked(
            self.__pdconfig.ignore_requires_python
        )
        self.le_save_to.setText(self.__pdconfig.save_path)
        self.le_platform.setText(" ".join(self.__pdconfig.platform))
        self.le_python_version.setText(self.__pdconfig.python_version)
        self.cmb_implementation.setCurrentText(self.__pdconfig.implementation)
        self.le_abis.setText(" ".join(self.__pdconfig.abis))
        use_index_url = self.__pdconfig.use_index_url
        self.cb_use_index_url.setChecked(use_index_url)
        self.le_index_url.setEnabled(use_index_url)
        self.le_index_url.setText(self.__pdconfig.index_url)

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
        destination = self.__pdconfig.save_path
        pkg_names = self.__pdconfig.package_names
        if not self.confirm_dest_path(destination):
            return
        if not pkg_names:
            return MessageBox(
                "提示",
                "没有需要下载的安装包。",
            ).exec_()
        index = self.__pdconfig.derived_from
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
        self.repo.put(thread_download, 0)

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

        if not self.__pdconfig.download_deps:
            configure.update(no_deps=True)
        download_type = self.__pdconfig.download_type
        if download_type == "no_binary":
            configure.update(no_binary=parse_package_names(names))
        elif download_type == "only_binary":
            configure.update(only_binary=parse_package_names(names))
        elif download_type == "prefer_binary":
            configure.update(prefer_binary=True)
        if self.__pdconfig.include_pre:
            configure.update(pre=True)
        if self.__pdconfig.ignore_requires_python:
            configure.update(ignore_requires_python=True)
        saved_path = self.__pdconfig.save_path
        if saved_path:
            configure.update(dest=saved_path)
        platform_name = self.__pdconfig.platform
        if platform_name:
            if unqualified():
                return MessageBox(
                    "提示",
                    "设置'兼容平台'后，不能勾选'下载需要下载的包的依赖库'，\
不能选择'仅选择源代码包'或'仅选择二进制包'。",
                    QMessageBox.Warning,
                ).exec_()
            configure.update(platform=platform_name)
        python_version = self.__pdconfig.python_version
        if python_version:
            if unqualified():
                return MessageBox(
                    "提示",
                    "设置'兼容 Python 版本'后，不能勾选'下载需要下载的包的依赖库'，\
不能选择'仅选择源代码包'或'仅选择二进制包'。",
                    QMessageBox.Warning,
                ).exec_()
            configure.update(python_version=python_version)
        impl_name = self.__pdconfig.implementation
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
        abis = self.__pdconfig.abis
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
        index_url = self.__pdconfig.index_url
        if self.__pdconfig.use_index_url and index_url:
            configure.update(index_url=index_url)
        return configure


class ShowDownloadWindow(Ui_show_download, QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
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


class MessageBox(QMessageBox):
    """
    点击按钮后返回该按钮在参数中的次序值

    多按钮：关闭窗口返回值跟随'reject'按钮次序值

    只有一个按钮：直接关闭窗口返回 0

    多按钮的情况下，'reject'按钮在最右侧

    有'destructive'按钮，无'reject'按钮，窗口不可关闭
    """

    def __init__(
        self,
        title,
        message,
        icon=QMessageBox.Information,
        buttons=(("accept", "确定"),),
    ):
        super().__init__(icon, title, message)
        self._buttons = buttons
        self._set_push_buttons()

    def _set_push_buttons(self):
        for btn in self._buttons:
            role, text = btn
            if role == "accept":
                self.addButton(text, QMessageBox.AcceptRole)
            elif role == "destructive":
                self.addButton(text, QMessageBox.DestructiveRole)
            elif role == "reject":
                self.setDefaultButton(self.addButton(text, QMessageBox.RejectRole))

    def get_role(self):
        return self.exec_()


class InputDialog(QInputDialog):
    def __init__(self, parent, sw=560, sh=0, title="", label=""):
        super().__init__(parent)
        self.resize(sw, sh)
        self.setFont(QFont("Microsoft YaHei UI"))
        self.setWindowTitle(title)
        self.setLabelText(label)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setOkButtonText("确定")
        self.setCancelButtonText("取消")
        self._confirm = self.exec_()

    def get_text(self):
        return self.textValue(), self._confirm


class GenericOutputWindow(Ui_generic_output, QMainWindow):
    signal_clear_content = pyqtSignal()
    signal_append_line = pyqtSignal(str)

    def __init__(self, parent, title):
        super().__init__(parent)
        self.setupUi(self)
        self.signal_slot_connection()
        self.setWindowTitle(title)
        self._width = self.width()

    def signal_slot_connection(self):
        self.signal_append_line.connect(
            self.uiPlainTextEdit_generic_output.appendPlainText
        )
        self.uiPushButton_clear_content.clicked.connect(
            self.uiPlainTextEdit_generic_output.clear
        )
        self.signal_clear_content.connect(self.uiPlainTextEdit_generic_output.clear)

    def clear_content(self):
        self.signal_clear_content.emit()

    def add_line(self, string):
        self.signal_append_line.emit(string)

    def resizeEvent(self, event: QResizeEvent):
        self._width = self.width()
        super().resizeEvent(event)

    def set_pos(self, x, y, h):
        self.setGeometry(x, y, self._width, h)


if __name__ == "__main__":
    awespykit = QApplication(sys.argv)
    awespykit.setStyle("fusion")
    awespykit.setWindowIcon(QIcon(":/icon.ico"))
    main_entrance_window = MainEntrance()
    sys.exit(awespykit.exec_())

# coding: utf-8

################################################################################
# MIT License

# Copyright (c) 2020 hrp/hrpzcf <hrpzcf@foxmail.com>

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
# Formatted with black 20.8b1.
################################################################################

import os
import sys
from platform import machine, platform

from PyQt5.QtCore import (
    QRegExp,
    QSize,
    Qt,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QIcon,
    QMovie,
    QRegExpValidator,
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

from interface import *
from library import *
from library.libcip import ImportInspector
from library.libm import PyEnv
from library.libpyi import PyiTool
from library.libqt import QLineEditMod, QTextEditMod

PYKIT_VERSION = "0.4.1"


class MainInterface(Ui_main_interface, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f"AwesomePyKit - {PYKIT_VERSION}")
        self.action_about.triggered.connect(self._show_about)
        self.pb_pkg_mgr.clicked.connect(win_pkg_mgr.show)
        self.pb_pyi_tool.clicked.connect(win_pyi_tool.show)
        self.pb_index_mgr.clicked.connect(win_index_mgr.show)

    def closeEvent(self, event):
        if win_pkg_mgr.thread_repo.is_empty() and win_pyi_tool.thread_repo.is_empty():
            event.accept()
        else:
            role = NewMessageBox(
                "警告",
                "有任务尚未完成，请耐心等待...",
                QMessageBox.Warning,
                (("accept", "强制退出"), ("reject", "取消")),
            ).exec_()
            if role == 0:
                win_pkg_mgr.thread_repo.kill_all()
                win_pyi_tool.thread_repo.kill_all()
                event.accept()
            else:
                event.ignore()

    @staticmethod
    def _show_about():
        try:
            with open("help/About.html", encoding="utf-8") as help_html:
                info = help_html.read().replace("0.0.0", PYKIT_VERSION)
                icon = QMessageBox.Information
        except Exception:
            info = '"关于"信息文件(help/About.html)已丢失。'
            icon = QMessageBox.Critical
        about_panel = NewMessageBox("关于", info, icon)
        about_panel.exec_()


class PackageManagerWindow(Ui_package_manager, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._setup_others()
        self._connect_signal_and_slot()
        self.env_list = get_pyenv_list(load_conf("pths"))
        self.path_list = [env.path for env in self.env_list]
        self.cur_pkgs_info = {}
        self._reverseds = [True, True, True, True]
        self.cur_selected_env = 0
        self.thread_repo = ThreadRepo(500)
        self._normal_size = self.size()

    def _setup_others(self):
        self.tw_installed_info.setColumnWidth(0, 220)
        self.tw_installed_info.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.tw_installed_info.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.Interactive
        )
        self.tw_installed_info.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeToContents
        )
        self.tw_installed_info.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeToContents
        )
        self.loading_mov = QMovie(os.path.join(resources_path, "loading.gif"))
        self.loading_mov.setScaledSize(QSize(18, 18))

    def show(self):
        self.resize(self._normal_size)
        super().show()
        self.list_widget_pyenvs_update()
        self.lw_env_list.setCurrentRow(self.cur_selected_env)

    @staticmethod
    def _stop_before_close():
        return not NewMessageBox(
            "警告",
            "当前有任务正在运行！\n是否安全停止所有正在运行的任务并关闭窗口？",
            QMessageBox.Question,
            (("accept", "安全停止并关闭"), ("reject", "取消")),
        ).exec_()

    def closeEvent(self, event):
        if not self.thread_repo.is_empty():
            if self._stop_before_close():
                self.thread_repo.stop_all()
                self._clear_pkgs_table_widget()
                save_conf(self.path_list, "pths")
                event.accept()
            else:
                event.ignore()

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

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

    def _connect_signal_and_slot(self):
        self.btn_autosearch.clicked.connect(self.auto_search_env)
        self.btn_delselected.clicked.connect(self.del_selected_py_env)
        self.btn_addmanully.clicked.connect(self.add_py_path_manully)
        self.cb_check_uncheck_all.clicked.connect(self.select_all_or_cancel_all)
        self.lw_env_list.itemPressed.connect(lambda: self.get_pkgs_info(0))
        self.btn_check_for_updates.clicked.connect(self.check_cur_pkgs_for_updates)
        self.btn_install_package.clicked.connect(self.install_pkgs)
        self.btn_uninstall_package.clicked.connect(self.uninstall_pkgs)
        self.btn_upgrade_package.clicked.connect(self.upgrade_pkgs)
        self.btn_upgrade_all.clicked.connect(self.upgrade_all_pkgs)
        self.tw_installed_info.horizontalHeader().sectionClicked[int].connect(
            self._sort_by_column
        )
        self.tw_installed_info.clicked.connect(self._show_tip_num_selected)
        self.cb_check_uncheck_all.clicked.connect(self._show_tip_num_selected)

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
            even_num_row = rowind % 2
            item = QTableWidgetItem(pkg_name)
            self.tw_installed_info.setItem(rowind, 0, item)
            if not even_num_row:
                item.setBackground(color_gray)
            for colind, item_text in enumerate(
                self.cur_pkgs_info.get(pkg_name, ["", "", ""])
            ):
                item = QTableWidgetItem(item_text)
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
                    reverse=self._reverseds[colind],
                )
            )
        else:
            self.cur_pkgs_info = dict(
                sorted(
                    self.cur_pkgs_info.items(),
                    key=lambda x: x[1][colind - 1],
                    reverse=self._reverseds[colind],
                )
            )
        self.table_widget_pkgs_info_update()
        self._reverseds[colind] = not self._reverseds[colind]

    def _clear_pkgs_table_widget(self):
        self.lb_num_selected_items.clear()
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(0)

    def get_pkgs_info(self, no_connect):
        self.cur_selected_env = self.lw_env_list.currentRow()
        if self.cur_selected_env == -1:
            return None

        def do_get_pkgs_info():
            pkgs_info = self.env_list[self.cur_selected_env].pkgs_info()
            self.cur_pkgs_info.clear()
            for pkg_info in pkgs_info:
                self.cur_pkgs_info[pkg_info[0]] = [pkg_info[1], "", ""]

        thread_get_pkgs_info = NewTask(do_get_pkgs_info)
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
        self.thread_repo.put(thread_get_pkgs_info, 1)
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
                self.path_list.append(env.path)

        path_list_lower = [p.lower() for p in self.path_list]
        thread_search_envs = NewTask(search_env)
        thread_search_envs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在搜索PYTHON安装目录..."),
        )
        thread_search_envs.at_finish(
            self._clear_pkgs_table_widget,
            self.list_widget_pyenvs_update,
            self.hide_loading,
            self.release_widgets,
            lambda: save_conf(self.path_list, "pths"),
        )
        thread_search_envs.start()
        self.thread_repo.put(thread_search_envs, 0)

    def del_selected_py_env(self):
        cur_index = self.lw_env_list.currentRow()
        if cur_index == -1:
            return
        del self.env_list[cur_index]
        del self.path_list[cur_index]
        self.lw_env_list.removeItemWidget(self.lw_env_list.takeItem(cur_index))
        self._clear_pkgs_table_widget()
        save_conf(self.path_list, "pths")

    def add_py_path_manully(self):
        input_dialog = NewInputDialog(
            self,
            560,
            0,
            "添加Python目录",
            "请输入Python目录路径：",
        )
        _path, ok = input_dialog.get_text()
        if not (ok and _path):
            return
        if not check_py_path(_path):
            return NewMessageBox(
                "警告",
                "无效的Python目录路径！",
                QMessageBox.Warning,
            ).exec_()
        _path = os.path.normpath(_path)
        if _path.lower() in [p.lower() for p in self.path_list]:
            return NewMessageBox(
                "警告",
                "要添加的Python目录已存在。",
                QMessageBox.Warning,
            ).exec_()
        try:
            env = PyEnv(_path)
            self.env_list.append(env)
            self.path_list.append(env.path)
        except Exception:
            return NewMessageBox(
                "警告",
                "目录添加失败，路径参数类型异常，请向开发者反馈，谢谢~",
                QMessageBox.Warning,
            ).exec_()
        self.list_widget_pyenvs_update()
        save_conf(self.path_list, "pths")

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

        thread_get_outdated = NewTask(do_get_outdated)
        thread_get_outdated.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在检查更新，请耐心等待..."),
        )
        thread_get_outdated.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_get_outdated.start()
        self.thread_repo.put(thread_get_outdated, 1)

    def lock_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.lw_env_list,
            self.tw_installed_info,
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
            self.tw_installed_info,
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
        cur_env = self.env_list[self.lw_env_list.currentRow()]
        pkgs_to_install = NewInputDialog(
            self,
            title="安装",
            label=f"注意，多个名称请用空格隔开。\n安装目标：{cur_env}",
        )
        names, ok = pkgs_to_install.get_text()
        names = [name for name in names.split() if name]
        if not (names and ok):
            return

        def do_install():
            for name, code in loop_install(cur_env, names):
                item = self.cur_pkgs_info.setdefault(name, ["", "", ""])
                if not item[0]:
                    item[0] = "- N/A -"
                item[2] = "安装成功" if code else "安装失败"

        thread_install_pkgs = NewTask(do_install)
        thread_install_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在安装，请稍候..."),
        )
        thread_install_pkgs.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_install_pkgs.start()
        self.thread_repo.put(thread_install_pkgs, 0)

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
                    item[0] = "- N/A -"
                item[2] = "卸载成功" if code else "卸载失败"

        thread_uninstall_pkgs = NewTask(do_uninstall)
        thread_uninstall_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在卸载，请稍候..."),
        )
        thread_uninstall_pkgs.at_finish(
            self.table_widget_pkgs_info_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_uninstall_pkgs.start()
        self.thread_repo.put(thread_uninstall_pkgs, 0)

    def upgrade_pkgs(self):
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
        if (
            NewMessageBox(
                "升级",
                f"确认升级？\n{names_text}",
                QMessageBox.Question,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            != 0
        ):
            return

        def do_upgrade():
            for pkg_name, code in loop_install(cur_env, pkg_names, upgrade=1):
                item = self.cur_pkgs_info.setdefault(pkg_name, ["", "", ""])
                if code and item[1]:
                    item[0] = item[1]
                item[2] = "升级成功" if code else "升级失败"

        thread_upgrade_pkgs = NewTask(do_upgrade)
        thread_upgrade_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在升级，请稍候..."),
        )
        thread_upgrade_pkgs.at_finish(
            self.table_widget_pkgs_info_update, self.hide_loading, self.release_widgets
        )
        thread_upgrade_pkgs.start()
        self.thread_repo.put(thread_upgrade_pkgs, 0)

    def upgrade_all_pkgs(self):
        upgradeable = [item[0] for item in self.cur_pkgs_info.items() if item[1][1]]
        if not upgradeable:
            NewMessageBox(
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
            NewMessageBox(
                "全部升级",
                f"确认升级？\n{names_text}",
                QMessageBox.Question,
                (("accept", "确定"), ("reject", "取消")),
            ).exec_()
            != 0
        ):
            return

        def do_upgrade():
            for pkg_name, code in loop_install(cur_env, upgradeable, upgrade=1):
                item = self.cur_pkgs_info.setdefault(pkg_name, ["", "", ""])
                if code and item[1]:
                    item[0] = item[1]
                item[2] = "升级成功" if code else "升级失败"

        thread_upgrade_pkgs = NewTask(do_upgrade)
        thread_upgrade_pkgs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在升级，请稍候..."),
        )
        thread_upgrade_pkgs.at_finish(
            self.table_widget_pkgs_info_update, self.hide_loading, self.release_widgets
        )
        thread_upgrade_pkgs.start()
        self.thread_repo.put(thread_upgrade_pkgs, 0)


class IndexUrlManagerWindow(Ui_index_url_manager, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._urls_dict = load_conf("urls")
        self._connect_signal_and_slot()
        self._normal_size = self.size()

    def show(self):
        self.resize(self._normal_size)
        super().show()
        self._list_widget_urls_update()

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    @staticmethod
    def _widget_for_list_item(url):
        item_layout = QHBoxLayout()
        item_layout.addWidget(QLabel(""))
        item_layout.addWidget(QLabel(url))
        item_layout.setStretch(0, 2)
        item_layout.setStretch(1, 8)
        item_widget = QWidget()
        item_widget.setLayout(item_layout)
        return item_widget

    def _list_widget_urls_update(self):
        self.li_indexurls.clear()
        for name, url in self._urls_dict.items():
            item_widget = self._widget_for_list_item(url)
            li_item = QListWidgetItem()
            li_item.setSizeHint(QSize(560, 42))
            li_item.setText(name)
            self.li_indexurls.addItem(li_item)
            self.li_indexurls.setItemWidget(li_item, item_widget)
        if self.li_indexurls.count():
            self.li_indexurls.setCurrentRow(0)

    def _connect_signal_and_slot(self):
        self.btn_clearle.clicked.connect(self._clear_line_edit)
        self.btn_saveurl.clicked.connect(self._save_index_urls)
        self.btn_delurl.clicked.connect(self._del_index_url)
        self.li_indexurls.clicked.connect(self._set_url_line_edit)
        self.btn_setindex.clicked.connect(self._set_global_index_url)
        self.btn_refresh_effective.clicked.connect(self._display_effective_url)

    def _set_url_line_edit(self):
        item = self.li_indexurls.currentItem()
        if (self.li_indexurls.currentRow() == -1) or (not item):
            return
        text = item.text()
        self.le_urlname.setText(text)
        self.le_indexurl.setText(self._urls_dict.get(text, ""))

    def _clear_line_edit(self):
        self.le_urlname.clear()
        self.le_indexurl.clear()

    def _check_name_url(self, name, url):
        error = lambda m: NewMessageBox("错误", m, QMessageBox.Critical)
        if not name:
            error = error("名称不能为空！")
        elif not url:
            error = error("地址不能为空！")
        elif not check_index_url(url):
            error = error("无效的镜像源地址！")
        elif name in self._urls_dict:
            error = error(f"名称'{name}'已存在！")
        else:
            return True
        # exec_返回信息窗口的关闭方式数字
        # 信息提示窗口默认只有确定按钮
        # 只有1个按钮情况下点击按钮和直接关闭窗口都返回0
        # 所以只要触发提示信息窗口，肯定返回0
        return error.exec_()

    def _save_index_urls(self):
        name = self.le_urlname.text()
        url = self.le_indexurl.text()
        if self._check_name_url(name, url):
            self._urls_dict[name] = url
        self._list_widget_urls_update()
        save_conf(self._urls_dict, "urls")

    def _del_index_url(self):
        last_selected = self.li_indexurls.currentRow()
        item = self.li_indexurls.currentItem()
        if (self.li_indexurls.currentRow() == -1) or (not item):
            NewMessageBox(
                "提示",
                "没有选中列表内的任何条目。",
            ).exec_()
            return
        del self._urls_dict[item.text()]
        self._list_widget_urls_update()
        items_num = self.li_indexurls.count()
        if items_num:  # 判断item数量是否为0
            if last_selected == -1:
                self.li_indexurls.setCurrentRow(0)
            else:
                should_be_selected = (
                    0
                    if last_selected - 1 < 0
                    else last_selected
                    if last_selected < items_num
                    else last_selected - 1
                )
                self.li_indexurls.setCurrentRow(should_be_selected)
        save_conf(self._urls_dict, "urls")

    @staticmethod
    def _get_cur_env():
        """
        首先使用配置文件中保存的Python路径实例化一个PyEnv，如果路径为空，
        则使用系统环境变量PATH中第一个Python路径，环境变量中还未找到则返回None。
        """
        saved_paths = load_conf("pths")
        warn_box = lambda m: NewMessageBox(
            "提示",
            m,
            QMessageBox.Warning,
        ).exec_()
        if not saved_paths:
            return PyEnv(cur_py_path())
        for _path in saved_paths:
            try:
                return PyEnv(_path)
            except Exception:
                continue
        else:
            warn_box("没有找到PYTHON环境，请在'包管理器'中添加PYTHON目录。")
        return

    def _set_global_index_url(self):
        url = self.le_indexurl.text()
        warn_box = lambda m: NewMessageBox("提示", m, QMessageBox.Warning)
        if not url:
            warn_box = warn_box("要设置为全局镜像源的地址不能为空！")
        elif not check_index_url(url):
            warn_box = warn_box("镜像源地址不符合pip镜像源地址格式。")
        else:
            env = self._get_cur_env()
            if not env:
                warn_box = warn_box(
                    "未找到PYTHON环境，全局镜像源启用失败。\n请在'包管理器'中添加PYTHON目录。",
                )
            elif env.set_global_index(url):
                warn_box = NewMessageBox("提示", f"全局镜像源地址设置成功：\n{url}")
            else:
                warn_box = warn_box(
                    "未找到PYTHON环境，全局镜像源地址启用失败。\n请在'包管理器'中添加PYTHON目录。",
                )
        warn_box.exec_()

    def _display_effective_url(self):
        env = self._get_cur_env()
        if not env:
            self.le_effectiveurl.setText(
                "未找到PYTHON环境，无法获取当前全局镜像源地址。",
            )
            return
        self.le_effectiveurl.setText(
            env.get_global_index() or "无效的PYTHON环境或当前全局镜像源地址为空。"
        )


class PyinstallerToolWindow(Ui_pyinstaller_tool, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.widget_group = (
            self.tab_project_files,
            self.tab_build_control,
            self.tab_file_ver_info,
            self.tab_advanced_setup,
            self.pb_select_py_env,
            self.pb_reinstall_pyi,
            self.cb_log_level,
            self.le_exefile_specfile_name,
            self.pb_check_imports,
            self.pb_gen_executable,
        )
        self.le_group_vers = (
            self.le_file_version_0,
            self.le_file_version_1,
            self.le_file_version_2,
            self.le_file_version_3,
            self.le_product_version_0,
            self.le_product_version_1,
            self.le_product_version_2,
            self.le_product_version_3,
        )
        self._setup_others()
        self.thread_repo = ThreadRepo(500)
        self._stored_conf = {}
        self.toolwin_cur_env = None
        self.pyi_tool = PyiTool()
        self.set_platform_info()
        self.pyi_running_mov = QMovie(os.path.join(resources_path, "loading.gif"))
        self.pyi_running_mov.setScaledSize(QSize(18, 18))
        self._connect_signal_slot()
        self._normal_size = self.size()

    def closeEvent(self, event):
        if not self.thread_repo.is_empty():
            NewMessageBox(
                "提醒",
                "任务正在运行中，关闭此窗口后任务将在后台运行。\n请勿对相关目录进行任何操作，否则可能会造成打包失败！",
                QMessageBox.Warning,
            ).exec_()
        self.store_state_of_widgets()
        save_conf(self._stored_conf, "pyic")
        event.accept()

    def show(self):
        self.resize(self._normal_size)
        super().show()
        if self.thread_repo.is_empty():
            self.apply_stored_config()
            self.pyi_tool.initialize(
                self._stored_conf.get("env_path", ""),
                self._stored_conf.get("project_root", os.getcwd()),
            )
            self._set_pyi_info()

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    def _setup_others(self):
        # 替换“主程序”LineEdit控件
        self.le_program_entry = QLineEditMod("file", {".py", ".pyc", ".pyw", ".spec"})
        self.le_program_entry.setToolTip(
            "要打包的程序的启动入口脚本(*.py *.pyw *.pyc *.spec)，此项必填。\n"
            "如果指定了SPEC文件，则以下绝大部分项目文件及生成控制都将不生效。\n"
            "可将格式正确的文件拖放到此处。"
        )
        self.horizontalLayout_3.replaceWidget(
            self.le_program_entry_old, self.le_program_entry
        )
        self.le_program_entry_old.deleteLater()
        # 替换“其他模块搜索路径”TextEdit控件
        self.te_module_search_path = QTextEditMod("dir")
        self.te_module_search_path.setToolTip(
            "程序的其他模块的搜索路径，此项可留空。\n仅当PYINSTALLER无法自动找到时使用，支持将文件夹直接拖放到此处。"
        )
        self.verticalLayout_3.replaceWidget(
            self.te_module_search_path_old, self.te_module_search_path
        )
        self.te_module_search_path_old.deleteLater()
        # 替换“非源代码资源文件”LineEdit控件
        self.te_other_data = QTextEditMod("file")
        self.te_other_data.setToolTip(
            """非源代码性质的其他资源文件，例如一些图片、配置文件等，此项可留空。\n"""
            """注意资源文件要在项目根目录范围内，否则打包后程序可能无法运行。可将文件或者文件夹直接拖到此处。"""
        )
        self.verticalLayout_4.replaceWidget(self.te_other_data_old, self.te_other_data)
        self.te_other_data_old.deleteLater()
        # 替换“文件图标路径”LineEdit控件
        self.le_file_icon_path = QLineEditMod("file", {".ico", ".icns"})
        self.le_file_icon_path.setToolTip(
            "生成的exe可执行文件的图标。\n支持.ico、.icns图标文件，可将格式正确的文件拖放到此处。"
        )
        self.horizontalLayout_11.replaceWidget(
            self.le_file_icon_path_old, self.le_file_icon_path
        )
        self.le_file_icon_path_old.deleteLater()
        reg_exp_val1 = QRegExpValidator(QRegExp(r'[^\\/:*?"<>|]*'))
        self.le_exefile_specfile_name.setValidator(reg_exp_val1)
        reg_exp_val2 = QRegExpValidator(QRegExp(r"[0-9]*"))
        for line_edit in self.le_group_vers:
            line_edit.setValidator(reg_exp_val2)
        self.le_runtime_tmpdir.setValidator(reg_exp_val1)

    def _connect_signal_slot(self):
        self.pyi_tool.completed.connect(self.task_completion_tip)
        self.pyi_tool.stdout.connect(self.te_pyi_out_stream.append)
        self.pb_select_py_env.clicked.connect(win_ch_env.show)
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
        self.pb_reinstall_pyi.clicked.connect(self.reinstall_pyi)
        self.pb_check_imports.clicked.connect(self._check_project_imports)
        win_check_imp.pb_install_all_missing.clicked.connect(
            lambda: self.install_missings(win_check_imp.all_missings)
        )

    def _check_project_imports(self):
        self.store_state_of_widgets()
        if not self.toolwin_cur_env:
            NewMessageBox(
                "提示",
                "还没有选择PYTHON环境！",
                QMessageBox.Warning,
            ).exec_()
            return
        project_root = self._stored_conf.get("project_root", None)
        if not project_root:
            NewMessageBox(
                "提示",
                "项目根目录未填写！",
                QMessageBox.Warning,
            ).exec_()
            return
        if not os.path.isdir(project_root):
            NewMessageBox(
                "提示",
                "项目根目录不存在！",
                QMessageBox.Warning,
            ).exec_()
            return
        missings = []

        def get_missing_imps():
            missings.append(
                tuple(
                    ImportInspector(
                        self.toolwin_cur_env.path, project_root
                    ).missing_items()
                )
            )

        thread_check_imp = NewTask(get_missing_imps)
        thread_check_imp.at_start(
            self.lock_widgets, lambda: self.show_running("正在分析环境中导入项安装信息...")
        )
        thread_check_imp.at_finish(
            self.hide_running,
            self.release_widgets,
            lambda: win_check_imp.set_cur_env_info(self.toolwin_cur_env),
            lambda: win_check_imp.table_update(missings),
            win_check_imp.show,
        )
        thread_check_imp.start()
        self.thread_repo.put(thread_check_imp, 1)

    def set_le_program_entry(self):
        selected_file = self._select_file_dir(
            "选择主程序",
            self._stored_conf.get("project_root", ""),
            file_filter="脚本文件 (*.py *.pyc *.pyw *.spec)",
        )[0]
        if not selected_file:
            return
        self.le_program_entry.setText(selected_file)

    def set_le_project_root(self):
        root = os.path.dirname(self.le_program_entry.text())
        self.le_project_root.setText(root)
        self._stored_conf["project_root"] = root

    def set_te_module_search_path(self):
        selected_dir = self._select_file_dir(
            "其他模块搜索目录", self._stored_conf.get("project_root", ""), cht="dir"
        )[0]
        if not selected_dir:
            return
        self.te_module_search_path.append(selected_dir)

    def set_te_other_data(self):
        selected_files = self._select_file_dir(
            "选择非源码资源文件", self._stored_conf.get("project_root", ""), mult=True
        )
        if not selected_files:
            return
        self.te_other_data.append("\n".join(selected_files))

    def set_le_file_icon_path(self):
        selected_file = self._select_file_dir(
            "选择可执行文件图标",
            self._stored_conf.get("project_root", ""),
            file_filter="图标文件 (*.ico *.icns)",
        )[0]
        if not selected_file:
            return
        self.le_file_icon_path.setText(selected_file)

    def set_le_spec_dir(self):
        selected_dir = self._select_file_dir(
            "选择SPEC文件储存目录",
            self._stored_conf.get("project_root", ""),
            cht="dir",
        )[0]
        if not selected_dir:
            return
        self.le_spec_dir.setText(selected_dir)

    def set_le_temp_working_dir(self):
        selected_dir = self._select_file_dir(
            "选择临时文件目录", self._stored_conf.get("project_root", ""), cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_temp_working_dir.setText(selected_dir)

    def set_le_output_dir(self):
        selected_dir = self._select_file_dir(
            "选择打包文件储存目录", self._stored_conf.get("project_root", ""), cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_output_dir.setText(selected_dir)

    def set_le_upx_search_path(self):
        selected_dir = self._select_file_dir(
            "选择UPX程序搜索目录", self._stored_conf.get("project_root", ""), cht="dir"
        )[0]
        if not selected_dir:
            return
        self.le_upx_search_path.setText(selected_dir)

    def _select_file_dir(
        self,
        title="",
        start="",
        cht="file",
        mult=False,
        file_filter="所有文件 (*)",
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

    def set_env_update_info(self):
        self.toolwin_cur_env = win_ch_env.chwin_env_list[
            win_ch_env.lw_env_list.currentRow()
        ]
        self.lb_py_info.setText(self.toolwin_cur_env.py_info())
        self.pyi_tool.initialize(
            self.toolwin_cur_env.env_path,
            self._stored_conf.get("program_entry", os.getcwd()),
        )
        self._set_pyi_info()

    def apply_stored_config(self):
        if not self._stored_conf:
            self._stored_conf.update(load_conf("pyic"))
        self.le_program_entry.setText(self._stored_conf.get("program_entry", ""))
        self.le_project_root.setText(self._stored_conf.get("project_root", ""))
        self.te_module_search_path.setText(
            "\n".join(self._stored_conf.get("module_search_path", []))
        )
        self.te_other_data.setText(
            "\n".join(
                path_group[0] for path_group in self._stored_conf.get("other_data", [])
            )
        )
        self.le_file_icon_path.setText(self._stored_conf.get("file_icon_path", ""))
        pack_to_one = self._stored_conf.get("pack_to_one", "dir")
        if pack_to_one == "file":
            self.rb_pack_to_one_file.setChecked(True)
        else:
            self.rb_pack_to_one_dir.setChecked(True)
        self.cb_execute_with_console.setChecked(
            self._stored_conf.get("execute_with_console", True)
        )
        self.cb_without_confirm.setChecked(
            self._stored_conf.get("without_confirm", False)
        )
        self.cb_use_upx.setChecked(self._stored_conf.get("use_upx", False))
        self.cb_clean_before_build.setChecked(
            self._stored_conf.get("clean_before_build", True)
        )
        self.cb_write_info_to_exec.setChecked(
            self._stored_conf.get("write_file_info", False)
        )
        self.le_temp_working_dir.setText(self._stored_conf.get("temp_working_dir", ""))
        self.le_output_dir.setText(self._stored_conf.get("output_dir", ""))
        self.le_spec_dir.setText(self._stored_conf.get("spec_dir", ""))
        self.le_upx_search_path.setText(self._stored_conf.get("upx_search_path", ""))
        self.te_upx_exclude_files.setText(
            "\n".join(self._stored_conf.get("upx_exclude_files", []))
        )
        _path = self._stored_conf.get("env_path", "")
        if _path:
            try:
                self.toolwin_cur_env = PyEnv(_path)
                self.lb_py_info.setText(self.toolwin_cur_env.py_info())
            except Exception:
                pass
        self.le_exefile_specfile_name.setText(
            self._stored_conf.get("exefile_specfile_name", "")
        )
        self.cb_log_level.setCurrentText(self._stored_conf.get("log_level", "INFO"))
        self.set_file_ver_info_text()
        self._change_debug_options("set")
        self.le_runtime_tmpdir.setText(self._stored_conf.get("runtime_tmpdir", ""))

    def store_state_of_widgets(self):
        self._stored_conf["program_entry"] = self.le_program_entry.local_path
        self._stored_conf[
            "exefile_specfile_name"
        ] = self.le_exefile_specfile_name.text()
        project_root = self.le_project_root.text()
        self._stored_conf["project_root"] = project_root
        self._stored_conf["module_search_path"] = self.te_module_search_path.local_paths
        self._stored_conf["other_data"] = self._abs_rel_groups(project_root)
        self._stored_conf["file_icon_path"] = self.le_file_icon_path.local_path
        if self.rb_pack_to_one_file.isChecked():
            self._stored_conf["pack_to_one"] = "file"
        else:
            self._stored_conf["pack_to_one"] = "dir"
        self._stored_conf[
            "execute_with_console"
        ] = self.cb_execute_with_console.isChecked()
        self._stored_conf["without_confirm"] = self.cb_without_confirm.isChecked()
        self._stored_conf["use_upx"] = self.cb_use_upx.isChecked()
        self._stored_conf["clean_before_build"] = self.cb_clean_before_build.isChecked()
        self._stored_conf["write_file_info"] = self.cb_write_info_to_exec.isChecked()
        self._stored_conf["temp_working_dir"] = self.le_temp_working_dir.text()
        self._stored_conf["output_dir"] = self.le_output_dir.text()
        self._stored_conf["spec_dir"] = self.le_spec_dir.text()
        self._stored_conf["upx_search_path"] = self.le_upx_search_path.text()
        self._stored_conf["upx_exclude_files"] = [
            string
            for string in self.te_upx_exclude_files.toPlainText().split("\n")
            if string
        ]
        if self.toolwin_cur_env is None:
            self._stored_conf["env_path"] = ""
        else:
            self._stored_conf["env_path"] = self.toolwin_cur_env.path
        self._stored_conf["log_level"] = self.cb_log_level.currentText()
        self._stored_conf["file_ver_info"] = self._file_ver_info_text()
        self._stored_conf["debug_options"] = self._change_debug_options("get")
        self._stored_conf["runtime_tmpdir"] = self.le_runtime_tmpdir.text()

    def _abs_rel_groups(self, starting_point):
        """ 获取其他要打包的文件的本地路径和与项目根目录的相对位置。"""
        other_data_local_paths = self.te_other_data.local_paths
        abs_rel_path_groups = []
        for abs_path in other_data_local_paths:
            try:
                rel_path = os.path.relpath(os.path.dirname(abs_path), starting_point)
            except Exception:
                continue
            abs_rel_path_groups.append((abs_path, rel_path))
        return abs_rel_path_groups

    def _change_debug_options(self, opt):
        """ 从关于"以调试模式打包"的控件获取状态或设置这些控件的状态。"""
        if opt == "get":
            return {
                "imports": self.cb_db_imports.isChecked(),
                "bootloader": self.cb_db_bootloader.isChecked(),
                "noarchive": self.cb_db_noarchive.isChecked(),
            }
        elif opt == "set":
            db = self._stored_conf.get("debug_options", {})
            self.cb_db_imports.setChecked(db.get("imports", False))
            self.cb_db_bootloader.setChecked(db.get("bootloader", False))
            self.cb_db_noarchive.setChecked(db.get("noarchive", False))

    def _file_ver_info_text(self):
        file_vers = tuple(int(x.text() or 0) for x in self.le_group_vers[:4])
        prod_vers = tuple(int(x.text() or 0) for x in self.le_group_vers[4:])
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
        info = self._stored_conf.get("file_ver_info", {})
        self.le_file_description.setText(info.get("$FileDescription$", ""))
        self.le_company_name.setText(info.get("$CompanyName$", ""))
        for ind, val in enumerate(info.get("$FileVersion$", "0.0.0.0").split(".")):
            self.le_group_vers[ind].setText(val)
        self.le_product_name.setText(info.get("$ProductName$", ""))
        for ind, val in enumerate(info.get("$ProductVersion$", "0.0.0.0").split(".")):
            self.le_group_vers[ind + 4].setText(val)
        self.le_legal_copyright.setText(info.get("$LegalCopyright$", ""))
        self.le_legal_trademarks.setText(info.get("$LegalTrademarks$", ""))
        self.le_original_filename.setText(info.get("$OriginalFilename$", ""))

    def _set_pyi_info(self, dont_set_enable=False):
        # 此处不能用 self.pyi_tool，因为 self.pyi_tool 总有一个空实例
        if self.toolwin_cur_env:
            if not dont_set_enable:
                self.pb_reinstall_pyi.setEnabled(True)
            pyi_info = self.pyi_tool.pyi_info()
            if pyi_info == "0.0.0":
                self.pb_reinstall_pyi.setText("安装")
            else:
                self.pb_reinstall_pyi.setText("重新安装")
            self.lb_pyi_info.setText(f"PYINSTALLER - {pyi_info}")
        else:
            self.lb_pyi_info.clear()
            self.pb_reinstall_pyi.setEnabled(False)

    def reinstall_pyi(self):
        # NewMessageBox的exec_方法返回0才是选择"确定"按钮
        if NewMessageBox(
            "安装",
            "确定安装PYINSTALLER吗？",
            QMessageBox.Question,
            (("accept", "确定"), ("reject", "取消")),
        ).exec_():
            return
        if not self.toolwin_cur_env:
            NewMessageBox(
                "提示",
                "当前未选择任何PYTHON环境。",
                QMessageBox.Warning,
            ).exec_()
            return

        def do_reinstall_pyi():
            self.toolwin_cur_env.uninstall("pyinstaller")
            self.toolwin_cur_env.install("pyinstaller", upgrade=1)
            self._set_pyi_info(dont_set_enable=True)

        thread_reinstall = NewTask(target=do_reinstall_pyi)
        thread_reinstall.at_start(
            self.lock_widgets,
            lambda: self.show_running("正在安装PYINSTALLER..."),
        )
        thread_reinstall.at_finish(
            self.hide_running,
            self.release_widgets,
        )
        thread_reinstall.start()
        self.thread_repo.put(thread_reinstall, 0)

    def set_platform_info(self):
        self.lb_platform_info.setText(f"{platform()}-{machine()}")

    def project_root_level(self, opt):
        if opt not in ("up", "reset"):
            return
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

    def _check_requireds(self):
        self.store_state_of_widgets()
        program_entry = self._stored_conf.get("program_entry", "")
        if not program_entry:
            NewMessageBox(
                "错误",
                "主程序未填写！",
                QMessageBox.Critical,
            ).exec_()
            return False
        if not os.path.isfile(program_entry):
            NewMessageBox(
                "错误",
                "主程序文件不存在！",
                QMessageBox.Critical,
            ).exec_()
            return False
        icon_path = self._stored_conf.get("file_icon_path", "")
        if icon_path != "" and not os.path.isfile(icon_path):
            NewMessageBox(
                "错误",
                "程序图标文件不存在！",
                QMessageBox.Critical,
            ).exec_()
            return False
        return True

    def show_running(self, msg):
        self.lb_running_tip.setText(msg)
        self.lb_running_gif.setMovie(self.pyi_running_mov)
        self.pyi_running_mov.start()

    def hide_running(self):
        self.pyi_running_mov.stop()
        self.lb_running_gif.clear()
        self.lb_running_tip.clear()

    def lock_widgets(self):
        for widget in self.widget_group:
            widget.setEnabled(False)

    def release_widgets(self):
        for widget in self.widget_group:
            widget.setEnabled(True)
        self.hide_running()

    @staticmethod
    def task_completion_tip(retcode):
        if retcode == 0:
            NewMessageBox(
                "任务结束",
                "可执行文件已打包完成！",
            ).exec_()
        else:
            NewMessageBox(
                "任务结束",
                "可执行文件生成失败，请检查错误信息！",
                QMessageBox.Critical,
            ).exec_()

    def build_executable(self):
        if not self._check_requireds():
            return
        self.te_pyi_out_stream.clear()
        self.pyi_tool.initialize(
            self._stored_conf.get("env_path", ""),
            self._stored_conf.get("project_root", os.getcwd()),
        )
        if not self.pyi_tool.pyi_ready:
            NewMessageBox(
                "提示",
                "PYINSTALLER不可用，请将PYINSTALLER安装到所选环境。",
                QMessageBox.Warning,
            ).exec_()
            return
        self.pyi_tool.prepare_cmd(self._stored_conf)
        self.handle = self.pyi_tool.handle()
        thread_build = NewTask(self.pyi_tool.execute_cmd)
        thread_build.at_start(
            self.lock_widgets,
            lambda: self.show_running("正在生成可执行文件..."),
        )
        thread_build.at_finish(self.hide_running, self.release_widgets)
        thread_build.start()
        self.thread_repo.put(thread_build, 0)

    def install_missings(self, missings):
        if not missings:
            NewMessageBox(
                "提示",
                "没有缺失的模块，无需安装。",
            ).exec_()
            win_check_imp.close()
            return
        if NewMessageBox(
            "安装",
            "确定将所有缺失模块安装至所选PYTHON环境中吗？",
            QMessageBox.Question,
            (("accept", "确定"), ("reject", "取消")),
        ).exec_():
            return

        def install_mis():
            for name in missings:
                self.toolwin_cur_env.install(name)

        thread_ins_mis = NewTask(install_mis)
        thread_ins_mis.at_start(
            self.lock_widgets,
            lambda: self.show_running("正在安装缺失模块..."),
            win_check_imp.close,
        )
        thread_ins_mis.at_finish(
            self.hide_running,
            self.release_widgets,
            lambda: NewMessageBox(
                "完成",
                "已完成安装流程，请重新检查是否安装成功。",
                QMessageBox.Information,
            ).exec_(),
        )
        thread_ins_mis.start()
        self.thread_repo.put(thread_ins_mis, 0)


class ChooseEnvWindow(Ui_choose_env, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._connect_signal_slot()
        self._normal_size = self.size()

    def _connect_signal_slot(self):
        self.lw_env_list.pressed.connect(self.close)

    def pyenv_list_update(self):
        row_size = QSize(0, 28)
        self.lw_env_list.clear()
        for env in self.chwin_env_list:
            item = QListWidgetItem(str(env))
            item.setSizeHint(row_size)
            self.lw_env_list.addItem(item)

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    def close(self):
        super().close()
        win_pyi_tool.set_env_update_info()

    def show(self):
        self.resize(self._normal_size)
        self.chwin_env_list = get_pyenv_list(load_conf("pths"))
        super().show()
        self.pyenv_list_update()


class CheckImportsWindow(Ui_check_imports, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._setup_others()
        self._normal_size = self.size()
        self._connect_signal_slot()
        self.all_missings = None

    def _setup_others(self):
        self.tw_missing_imports.setColumnWidth(0, 260)
        self.tw_missing_imports.setColumnWidth(1, 350)
        self.tw_missing_imports.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive
        )
        self.tw_missing_imports.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.Stretch
        )

    def _connect_signal_slot(self):
        self.pb_confirm.clicked.connect(self.close)

    def resizeEvent(self, event):
        old_size = event.oldSize()
        if (
            not self.isMaximized()
            and not self.isMinimized()
            and (old_size.width(), old_size.height()) != (-1, -1)
        ):
            self._normal_size = old_size

    def close(self):
        super().close()

    def show(self):
        self.resize(self._normal_size)
        super().show()

    def table_update(self, missing_data):
        # missing_data: ((filepath, {imps...}, {missings...})...)
        if not missing_data:
            return
        missing_data, *_ = missing_data
        self.all_missings = []
        for _, _, m in missing_data:
            self.all_missings.extend(m)
        self.tw_missing_imports.clearContents()
        self.tw_missing_imports.setRowCount(len(missing_data))
        for rowind, value in enumerate(missing_data):
            # value[0]即filepath为None，按照ImportInspector类
            # missing_items特点，可知项目内一个可以打开的文件都没有，直接中断
            if value[0] is None:
                break
            item0 = QTableWidgetItem(os.path.basename(value[0]))
            item1 = QTableWidgetItem("，".join(value[1]))
            item2 = QTableWidgetItem("，".join(value[2]))
            item0.setToolTip(value[0])
            item1.setToolTip("\n".join(value[1]))
            item2.setToolTip("\n".join(value[2]))
            self.tw_missing_imports.setItem(rowind, 0, item0)
            self.tw_missing_imports.setItem(rowind, 1, item1)
            self.tw_missing_imports.setItem(rowind, 2, item2)
        self.show()

    def set_cur_env_info(self, env):
        if not env:
            return
        self.le_cip_cur_env.setText(str(env))


class NewMessageBox(QMessageBox):
    """
    只有一个按钮，点击按钮和直接关闭窗口都返回0(默认)
    有'reject'按钮，无'destructive'按钮，关闭窗口和点击'reject'返回1
    无'reject'按钮，有'destructive'按钮，窗口不可关闭，'destructive'返回1
    有'accept'按钮和'reject'按钮，点击'accept'返回0，'reject'和关闭窗口返回1
    有'reject'和'destructive'按钮，'reject'和关闭窗口返回0，'destructive'返回1
    有3个按钮，'accept'返回0，'reject'和关闭窗口返回1，'destructive'返回2
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


class NewInputDialog(QInputDialog):
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


def main():
    # 把 global声明写一行里不美观，犯强迫症
    global win_pkg_mgr
    global win_ch_env
    global win_pyi_tool
    global win_index_mgr
    global win_check_imp
    app_awesomepykit = QApplication(sys.argv)
    app_awesomepykit.setWindowIcon(QIcon(os.path.join(resources_path, "icon.ico")))
    win_pkg_mgr = PackageManagerWindow()
    win_ch_env = ChooseEnvWindow()
    win_check_imp = CheckImportsWindow()
    win_pyi_tool = PyinstallerToolWindow()
    win_index_mgr = IndexUrlManagerWindow()
    win_main_interface = MainInterface()
    win_main_interface.show()
    sys.exit(app_awesomepykit.exec_())


if __name__ == "__main__":
    main()

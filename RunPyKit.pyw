# -*- coding: utf-8 -*-

import os
import re
import sys

from PyQt5.QtCore import (
    QSize,
    Qt,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QIcon,
    QMovie,
)
from PyQt5.QtWidgets import (
    QApplication,
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
from library.libm import PyEnv

__VERSION__ = '0.1.7'


class MainInterfaceWindow(Ui_MainInterface, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._connect_signal_and_slot()

    def _connect_signal_and_slot(self):
        self.about.triggered.connect(self._show_about)
        self.description.triggered.connect(self._show_usinghelp)
        self.btn_manPacks.clicked.connect(self._show_pkgmgr)
        self.btn_setIndex.clicked.connect(self._show_indexmgr)

    def closeEvent(self, event):
        if package_manager_window._threads.is_empty():
            event.accept()
        else:
            msg_box = NewMessageBox('警告', '任务尚未完全安全退出，请稍等...')
            msg_box.exec()
            event.ignore()

    @staticmethod
    def _show_about():
        try:
            with open('help/About.html', encoding='utf-8') as help_html:
                info = re.sub(
                    r'(?<=\>)0.0.0(?=\<)', __VERSION__, help_html.read()
                )
                icon = QMessageBox.Information
        except Exception:
            info = '"关于"信息文件(help/About.html)已丢失。'
            icon = QMessageBox.Critical
        about_panel = NewMessageBox('关于', info, icon)
        about_panel.get_role()

    @staticmethod
    def _show_usinghelp():
        information_panel_window.setWindowTitle('使用帮助')
        try:
            with open('help/UsingHelp.html', encoding='utf-8') as using_html:
                information_panel_window.help_panel.setText(using_html.read())
        except Exception:
            information_panel_window.help_panel.setText(
                '"使用帮助"文件(help/UsingHelp.html)已丢失。'
            )
        information_panel_window.setGeometry(430, 100, 0, 0)
        information_panel_window.show()

    @staticmethod
    def _show_pkgmgr():
        package_manager_window.show()

    @staticmethod
    def _show_indexmgr():
        mirror_source_manager_window.show()


class PackageManagerWindow(Ui_PackageManager, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._setup_others()
        self._connect_signal_and_slot()
        self._py_envs_list = get_pyenv_list(load_conf('pths'))
        self._py_paths_list = [
            py_env.env_path for py_env in self._py_envs_list
        ]
        self.cur_pkgs_info = {}
        self._reverseds = [True, True, True, True]
        self.cur_selected_env = 0
        self._threads = ThreadRepo(300)

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
        self.loading_mov = QMovie(os.path.join(sources_path, 'loading.gif'))
        self.loading_mov.setScaledSize(QSize(15, 15))

    def show(self):
        super().show()
        self.list_widget_pyenvs_update()
        self.lw_py_envs.setCurrentRow(self.cur_selected_env)

    @staticmethod
    def stop_threads_before_close():
        msg_if_stop_threads = NewMessageBox(
            '警告',
            '当前有任务正在运行！\n是否安全停止所有正在运行的任务并关闭窗口？',
            QMessageBox.Question,
            (('accept', '安全停止并关闭'), ('reject', '取消')),
        )
        return not msg_if_stop_threads.exec()

    def closeEvent(self, event):
        if not self._threads.is_empty():
            if self.stop_threads_before_close():
                self._threads.stop_all()
                self.clear_table_widget()
                save_conf(self._py_paths_list, 'pths')
                event.accept()
            else:
                event.ignore()

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

    def show_message(self, text):
        self.lb_loading_gif.setText(text)

    def _connect_signal_and_slot(self):
        self.btn_autosearch.clicked.connect(self.auto_search_py_envs)
        self.btn_delselected.clicked.connect(self.del_selected_py_env)
        self.btn_addmanully.clicked.connect(self.add_py_path_manully)
        self.cb_check_uncheck_all.clicked.connect(
            self.select_all_or_cancel_all
        )
        self.lw_py_envs.itemPressed.connect(lambda: self.get_pkgs_info(0))
        self.btn_check_for_updates.clicked.connect(
            self.check_cur_pkgs_for_updates
        )
        self.btn_install_package.clicked.connect(self.install_pkgs)
        self.btn_uninstall_package.clicked.connect(self.uninstall_pkgs)
        self.btn_upgrade_package.clicked.connect(self.upgrade_pkgs)
        self.btn_upgrade_all.clicked.connect(self.upgrade_all_pkgs)
        self.tw_installed_info.horizontalHeader().sectionClicked[int].connect(
            self.sort_by_column
        )
        self.tw_installed_info.clicked.connect(self.show_tip_num_selected)
        self.cb_check_uncheck_all.clicked.connect(self.show_tip_num_selected)

    def show_tip_num_selected(self):
        self.lb_num_selected_items.setText(
            f'当前选中数量：{len(self.indexs_of_selected_rows())}'
        )

    def list_widget_pyenvs_update(self):
        row_size = QSize(0, 28)
        cur_py_env_index = self.lw_py_envs.currentRow()
        self.lw_py_envs.clear()
        for py_env in self._py_envs_list:
            item = QListWidgetItem(str(py_env))
            item.setSizeHint(row_size)
            self.lw_py_envs.addItem(item)
        if cur_py_env_index != -1:
            self.lw_py_envs.setCurrentRow(cur_py_env_index)

    def table_widget_pkgs_info_update(self):
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(len(self.cur_pkgs_info))
        self.lb_num_selected_items.clear()
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
                self.cur_pkgs_info.get(pkg_name, ['', '', ''])
            ):
                item = QTableWidgetItem(item_text)
                if colind == 2:
                    if item_text in ('升级成功', '安装成功', '卸载成功'):
                        item.setForeground(color_green)
                    elif item_text in ('升级失败', '安装失败', '卸载失败'):
                        item.setForeground(color_red)
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                if not even_num_row:
                    item.setBackground(color_gray)
                self.tw_installed_info.setItem(rowind, colind + 1, item)

    def sort_by_column(self, colind):
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

    def clear_table_widget(self):
        self.lb_num_selected_items.clear()
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(0)

    def get_pkgs_info(self, no_connect):
        self.cur_selected_env = self.lw_py_envs.currentRow()
        if self.cur_selected_env == -1:
            return

        def do_get_pkgs_info():
            pkgs_info = self._py_envs_list[self.cur_selected_env].pkgs_info()
            self.cur_pkgs_info.clear()
            for pkg_info in pkgs_info:
                self.cur_pkgs_info[pkg_info[0]] = [pkg_info[1], '', '']

        thread_get_pkgs_info = NewTask(do_get_pkgs_info)
        if not no_connect:
            thread_get_pkgs_info.started.connect(self.lock_widgets)
            thread_get_pkgs_info.started.connect(
                lambda: self.show_loading('正在加载包信息...')
            )
            thread_get_pkgs_info.finished.connect(
                self.table_widget_pkgs_info_update
            )
            thread_get_pkgs_info.finished.connect(self.hide_loading)
            thread_get_pkgs_info.finished.connect(self.release_widgets)
        thread_get_pkgs_info.start()
        self._threads.put(thread_get_pkgs_info)
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

    def auto_search_py_envs(self):
        def search_envs():
            for py_path in all_py_paths():
                if py_path in self._py_paths_list:
                    continue
                try:
                    py_env = PyEnv(py_path)
                except Exception:
                    continue
                self._py_envs_list.append(py_env)
                self._py_paths_list.append(py_env.env_path)

        thread_search_envs = NewTask(search_envs)
        thread_search_envs.started.connect(self.lock_widgets)
        thread_search_envs.started.connect(
            lambda: self.show_loading('正在搜索Python目录...')
        )
        thread_search_envs.finished.connect(self.clear_table_widget)
        thread_search_envs.finished.connect(self.list_widget_pyenvs_update)
        thread_search_envs.finished.connect(self.hide_loading)
        thread_search_envs.finished.connect(self.release_widgets)
        thread_search_envs.finished.connect(
            lambda: save_conf(self._py_paths_list, 'pths')
        )
        thread_search_envs.start()
        self._threads.put(thread_search_envs)

    def del_selected_py_env(self):
        cur_index = self.lw_py_envs.currentRow()
        if cur_index == -1:
            return
        del self._py_envs_list[cur_index]
        del self._py_paths_list[cur_index]
        self.lw_py_envs.removeItemWidget(self.lw_py_envs.takeItem(cur_index))
        self.clear_table_widget()
        save_conf(self._py_paths_list, 'pths')

    def add_py_path_manully(self):
        input_dialog = NewInputDialog(
            self, 560, 0, '添加Python目录', '请输入Python目录路径：'
        )
        py_path, ok = input_dialog.getText()
        if not (ok and py_path):
            return
        if not check_py_path(py_path):
            self.show_message('无效的Python目录路径！')
            return
        py_path = os.path.join(py_path, '')
        if py_path in self._py_paths_list:
            self.show_message('要添加的Python目录已存在。')
            return
        py_env = PyEnv(py_path)
        self._py_envs_list.append(py_env)
        self._py_paths_list.append(py_env.env_path)
        self.list_widget_pyenvs_update()
        save_conf(self._py_paths_list, 'pths')

    def check_cur_pkgs_for_updates(self):
        if self.tw_installed_info.rowCount() == 0:
            return
        cur_row = self.lw_py_envs.currentRow()
        if cur_row == -1:
            return
        thread_get_info = self.get_pkgs_info(no_connect=1)

        def do_get_outdated():
            thread_get_info.wait()
            outdateds = self._py_envs_list[cur_row].outdated()
            for outdated_info in outdateds:
                self.cur_pkgs_info.setdefault(outdated_info[0], ['', '', ''])[
                    1
                ] = outdated_info[2]

        thread_get_outdated = NewTask(do_get_outdated)
        thread_get_outdated.started.connect(self.lock_widgets)
        thread_get_outdated.started.connect(
            lambda: self.show_loading('正在检查更新，请耐心等待...')
        )
        thread_get_outdated.finished.connect(
            self.table_widget_pkgs_info_update
        )
        thread_get_outdated.finished.connect(self.hide_loading)
        thread_get_outdated.finished.connect(self.release_widgets)
        thread_get_outdated.start()
        self._threads.put(thread_get_outdated)

    def lock_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.lw_py_envs,
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
            self.lw_py_envs,
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
        cur_py_env = self._py_envs_list[self.lw_py_envs.currentRow()]
        pkgs_to_install = NewInputDialog(
            self, title='安装', label=f'注意，多个名称请用空格隔开。\n安装目标：{cur_py_env}',
        )
        names, ok = pkgs_to_install.getText()
        names = [name for name in names.split() if name]
        if not (names and ok):
            return

        def do_install():
            for name, code in loop_install(cur_py_env, names):
                item = self.cur_pkgs_info.setdefault(name, ['', '', ''])
                if not item[0]:
                    item[0] = '————'
                if code:
                    item[2] = '安装成功'
                else:
                    item[2] = '安装失败'

        thread_install_pkgs = NewTask(do_install)
        thread_install_pkgs.started.connect(self.lock_widgets)
        thread_install_pkgs.started.connect(
            lambda: self.show_loading('正在安装，请稍候...')
        )
        thread_install_pkgs.finished.connect(
            self.table_widget_pkgs_info_update
        )
        thread_install_pkgs.finished.connect(self.hide_loading)
        thread_install_pkgs.finished.connect(self.release_widgets)
        thread_install_pkgs.start()
        self._threads.put(thread_install_pkgs)

    def uninstall_pkgs(self):
        cur_pkgs_info_keys = tuple(self.cur_pkgs_info.keys())
        pkg_indexs = self.indexs_of_selected_rows()
        pkg_names = [cur_pkgs_info_keys[index] for index in pkg_indexs]
        if not pkg_names:
            return
        cur_py_env = self._py_envs_list[self.lw_py_envs.currentRow()]
        len_pkgs = len(pkg_names)
        names_text = (
            '\n'.join(pkg_names)
            if len_pkgs <= 10
            else '\n'.join(('\n'.join(pkg_names[:10]), '......'))
        )
        uninstall_msg_box = QMessageBox(
            QMessageBox.Question, '卸载', f'确认卸载？\n{names_text}'
        )
        uninstall_msg_box.addButton('确定', QMessageBox.AcceptRole)
        reject = uninstall_msg_box.addButton('取消', QMessageBox.RejectRole)
        uninstall_msg_box.setDefaultButton(reject)
        if uninstall_msg_box.exec() != 0:
            return

        def do_uninstall():
            for pkg_name, code in loop_uninstall(cur_py_env, pkg_names):
                item = self.cur_pkgs_info.setdefault(pkg_name, ['', '', ''])
                item[0] = '————'
                if code:
                    item[2] = '卸载成功'
                else:
                    item[2] = '卸载失败'

        thread_uninstall_pkgs = NewTask(do_uninstall)
        thread_uninstall_pkgs.started.connect(self.lock_widgets)
        thread_uninstall_pkgs.started.connect(
            lambda: self.show_loading('正在卸载，请稍候...')
        )
        thread_uninstall_pkgs.finished.connect(
            self.table_widget_pkgs_info_update
        )
        thread_uninstall_pkgs.finished.connect(self.hide_loading)
        thread_uninstall_pkgs.finished.connect(self.release_widgets)
        thread_uninstall_pkgs.start()
        self._threads.put(thread_uninstall_pkgs)

    def upgrade_pkgs(self):
        cur_pkgs_info_keys = tuple(self.cur_pkgs_info.keys())
        pkg_indexs = self.indexs_of_selected_rows()
        pkg_names = [cur_pkgs_info_keys[index] for index in pkg_indexs]
        if not pkg_names:
            return
        cur_py_env = self._py_envs_list[self.lw_py_envs.currentRow()]
        len_pkgs = len(pkg_names)
        names_text = (
            '\n'.join(pkg_names)
            if len_pkgs <= 10
            else '\n'.join(('\n'.join(pkg_names[:10]), '......'))
        )
        uninstall_msg_box = QMessageBox(
            QMessageBox.Question, '升级', f'确认升级？\n{names_text}'
        )
        uninstall_msg_box.addButton('确定', QMessageBox.AcceptRole)
        reject = uninstall_msg_box.addButton('取消', QMessageBox.RejectRole)
        uninstall_msg_box.setDefaultButton(reject)
        if uninstall_msg_box.exec() != 0:
            return

        def do_upgrade():
            for pkg_name, code in loop_install(
                cur_py_env, pkg_names, upgrade=1
            ):
                item = self.cur_pkgs_info.setdefault(pkg_name, ['', '', ''])
                if code:
                    item[0] = item[1]
                    item[2] = '升级成功'
                else:
                    item[2] = '升级失败'

        thread_upgrade_pkgs = NewTask(do_upgrade)
        thread_upgrade_pkgs.started.connect(self.lock_widgets)
        thread_upgrade_pkgs.started.connect(
            lambda: self.show_loading('正在升级，请稍候...')
        )
        thread_upgrade_pkgs.finished.connect(
            self.table_widget_pkgs_info_update
        )
        thread_upgrade_pkgs.finished.connect(self.hide_loading)
        thread_upgrade_pkgs.finished.connect(self.release_widgets)
        thread_upgrade_pkgs.start()
        self._threads.put(thread_upgrade_pkgs)

    def upgrade_all_pkgs(self):
        upgradeable = [
            item[0] for item in self.cur_pkgs_info.items() if item[1][1]
        ]
        if not upgradeable:
            msg_box = QMessageBox(
                QMessageBox.Information, '提示', '请先检查更新确认是否有可更新的包。'
            )
            msg_box.addButton('确定', QMessageBox.AcceptRole)
            msg_box.exec()
            return
        cur_py_env = self._py_envs_list[self.lw_py_envs.currentRow()]
        len_pkgs = len(upgradeable)
        names_text = (
            '\n'.join(upgradeable)
            if len_pkgs <= 10
            else '\n'.join(('\n'.join(upgradeable[:10]), '......'))
        )
        upgrade_all_msg_box = QMessageBox(
            QMessageBox.Question, '全部升级', f'确认升级？\n{names_text}'
        )
        upgrade_all_msg_box.addButton('确定', QMessageBox.AcceptRole)
        reject = upgrade_all_msg_box.addButton('取消', QMessageBox.RejectRole)
        upgrade_all_msg_box.setDefaultButton(reject)
        if upgrade_all_msg_box.exec() != 0:
            return

        def do_upgrade():
            for pkg_name, code in loop_install(
                cur_py_env, upgradeable, upgrade=1
            ):
                item = self.cur_pkgs_info.setdefault(pkg_name, ['', '', ''])
                if code:
                    item[2] = '升级成功'
                else:
                    item[2] = '升级失败'

        thread_upgrade_pkgs = NewTask(do_upgrade)
        thread_upgrade_pkgs.started.connect(self.lock_widgets)
        thread_upgrade_pkgs.started.connect(
            lambda: self.show_loading('正在升级，请稍候...')
        )
        thread_upgrade_pkgs.finished.connect(
            self.table_widget_pkgs_info_update
        )
        thread_upgrade_pkgs.finished.connect(self.hide_loading)
        thread_upgrade_pkgs.finished.connect(self.release_widgets)
        thread_upgrade_pkgs.start()
        self._threads.put(thread_upgrade_pkgs)


class MirrorSourceManagerWindow(Ui_MirrorSourceManager, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._urls_dict = load_conf('urls')
        self._connect_signal_and_slot()

    def show(self):
        super().show()
        self._list_widget_urls_update()

    @staticmethod
    def _widget_for_list_item(url):
        item_layout = QHBoxLayout()
        item_layout.addWidget(QLabel(''))
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
        self.le_indexurl.setText(self._urls_dict.get(text, ''))

    def _clear_line_edit(self):
        self.le_urlname.clear()
        self.le_indexurl.clear()

    def _check_name_url(self, name, url):
        if not name:
            self.statusbar.showMessage('名称不能为空！')
            return False
        if not url:
            self.statusbar.showMessage('地址不能为空！')
            return False
        if not check_index_url(url):
            self.statusbar.showMessage('无效的镜像源地址！')
            return False
        if name in self._urls_dict:
            self.statusbar.showMessage(f'名称<{name}>已存在！')
            return False
        return True

    def _save_index_urls(self):
        name = self.le_urlname.text()
        url = self.le_indexurl.text()
        if self._check_name_url(name, url):
            self._urls_dict[name] = url
        self._list_widget_urls_update()
        save_conf(self._urls_dict, 'urls')

    def _del_index_url(self):
        item = self.li_indexurls.currentItem()
        if (self.li_indexurls.currentRow() == -1) or (not item):
            self.statusbar.showMessage('没有选中列表内的任何条目。')
            return
        del self._urls_dict[item.text()]
        self._list_widget_urls_update()
        save_conf(self._urls_dict, 'urls')

    def _get_cur_pyenv(self):
        '''使用系统环境变量PATH中第一个Python路径生成一个PyEnv实例。'''
        py_paths = load_conf('pths')
        if not py_paths:
            try:
                return PyEnv(cur_py_path())
            except Exception:
                self.statusbar.showMessage(
                    '没有找到pip可执行文件，请在"包管理器"界面添加任意Python目录到列表。'
                )
        else:
            for py_path in py_paths:
                try:
                    return PyEnv(py_path)
                except Exception:
                    continue
            else:
                self.statusbar.showMessage(
                    '没有找到pip可执行程序，请在"包管理器"界面添加Python目录到列表。'
                )

    def _set_global_index_url(self):
        url = self.le_indexurl.text()
        if not url:
            self.statusbar.showMessage('要设置为全局镜像源的地址不能为空！')
            return
        if not check_index_url(url):
            self.statusbar.showMessage('镜像源地址不符合pip镜像源地址格式。')
            return
        pyenv = self._get_cur_pyenv()
        if not pyenv:
            self.statusbar.showMessage('镜像源启用失败，未找到pip可执行文件。')
            return
        pyenv.set_global_index(url)
        self.statusbar.showMessage(f'已将"{url}"设置为全局镜像源地址。')

    def _display_effective_url(self):
        pyenv = self._get_cur_pyenv()
        if pyenv:
            self.le_effectiveurl.setText(
                pyenv.get_global_index() or '当前全局镜像源地址为空。'
            )
        else:
            self.le_effectiveurl.setText('无法获取当前全局镜像源地址。')


class InformationPanelWindow(Ui_InformationPanel, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    def closeEvent(self, event):
        self.resize(1, 1)


class NewInputDialog(QInputDialog):
    def __init__(self, parent, sw=560, sh=0, title='', label=''):
        super().__init__(parent)
        self.resize(sw, sh)
        self.setFont(QFont('Microsoft YaHei UI'))
        self.setWindowTitle(title)
        self.setLabelText(label)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.setOkButtonText('确定')
        self.setCancelButtonText('取消')
        self._confirm = self.exec()

    def getText(self):
        return self.textValue(), self._confirm


class NewMessageBox(QMessageBox):
    def __init__(
        self,
        title,
        message,
        icon=QMessageBox.Information,
        buttons=(('accept', '确定'),),
    ):
        super().__init__(icon, title, message)
        for btn in buttons:
            role, text = btn
            if role == 'accept':
                self.addButton(text, QMessageBox.AcceptRole)
            elif role == 'destructive':
                self.addButton(text, QMessageBox.DestructiveRole)
            elif role == 'reject':
                self.addButton(text, QMessageBox.RejectRole)

    def get_role(self):
        return self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(sources_path, 'icon.ico')))
    information_panel_window = InformationPanelWindow()
    main_interface_window = MainInterfaceWindow()
    package_manager_window = PackageManagerWindow()
    mirror_source_manager_window = MirrorSourceManagerWindow()
    main_interface_window.show()
    sys.exit(app.exec_())

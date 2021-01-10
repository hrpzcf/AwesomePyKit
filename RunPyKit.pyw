# coding: utf-8

import os
import re
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
from library.libm import PyEnv
from library.libpyi import PyiTool
from library.libqt import QLineEditMod, QTextEditMod

__VERSION__ = '0.2.0'


class MainInterfaceWindow(Ui_MainInterface, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(f'AwesomePyKit - {__VERSION__}')
        self._connect_signal_and_slot()

    def _connect_signal_and_slot(self):
        self.about.triggered.connect(self._show_about)
        self.description.triggered.connect(self._show_usinghelp)
        self.btn_manPacks.clicked.connect(self._show_pkgmgr)
        self.btn_setIndex.clicked.connect(self._show_indexmgr)
        self.pb_pyi_tool.clicked.connect(self._show_pyinstaller_tool)

    @staticmethod
    def _show_pkgmgr():
        win_package_mgr.show()

    @staticmethod
    def _show_indexmgr():
        win_mirror_mgr.show()

    @staticmethod
    def _show_pyinstaller_tool():
        win_pyi_tool.show()

    def closeEvent(self, event):
        if (
            win_package_mgr._threads.is_empty()
            and win_pyi_tool._threads.is_empty()
        ):
            event.accept()
        else:
            role = NewMessageBox(
                '警告',
                '有任务尚未完成，请耐心等待...',
                QMessageBox.Warning,
                (('accept', '强制退出'), ('reject', '取消')),
            ).exec()
            if role == 0:
                win_package_mgr._threads.kill_all()
                win_pyi_tool._threads.kill_all()
                event.accept()
            else:
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
        win_info_panel.setWindowTitle('使用帮助')
        try:
            with open('help/UsingHelp.html', encoding='utf-8') as using_html:
                win_info_panel.help_panel.setText(using_html.read())
        except Exception:
            win_info_panel.help_panel.setText(
                '"使用帮助"文件(help/UsingHelp.html)已丢失。'
            )
        win_info_panel.setGeometry(430, 100, 0, 0)
        win_info_panel.show()


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
    def _stop_threads_before_close():
        msg_if_stop_threads = NewMessageBox(
            '警告',
            '当前有任务正在运行！\n是否安全停止所有正在运行的任务并关闭窗口？',
            QMessageBox.Question,
            (('accept', '安全停止并关闭'), ('reject', '取消')),
        )
        return not msg_if_stop_threads.exec()

    def closeEvent(self, event):
        if not self._threads.is_empty():
            if self._stop_threads_before_close():
                self._threads.stop_all()
                self._clear_table_widget()
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
            self._sort_by_column
        )
        self.tw_installed_info.clicked.connect(self._show_tip_num_selected)
        self.cb_check_uncheck_all.clicked.connect(self._show_tip_num_selected)

    def _show_tip_num_selected(self):
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

    def _clear_table_widget(self):
        self.lb_num_selected_items.clear()
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(0)

    def get_pkgs_info(self, no_connect):
        self.cur_selected_env = self.lw_py_envs.currentRow()
        if self.cur_selected_env == -1:
            return None

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
        self._threads.put(thread_get_pkgs_info, 1)
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
        thread_search_envs.finished.connect(self._clear_table_widget)
        thread_search_envs.finished.connect(self.list_widget_pyenvs_update)
        thread_search_envs.finished.connect(self.hide_loading)
        thread_search_envs.finished.connect(self.release_widgets)
        thread_search_envs.finished.connect(
            lambda: save_conf(self._py_paths_list, 'pths')
        )
        thread_search_envs.start()
        self._threads.put(thread_search_envs, 0)

    def del_selected_py_env(self):
        cur_index = self.lw_py_envs.currentRow()
        if cur_index == -1:
            return
        del self._py_envs_list[cur_index]
        del self._py_paths_list[cur_index]
        self.lw_py_envs.removeItemWidget(self.lw_py_envs.takeItem(cur_index))
        self._clear_table_widget()
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
        self._threads.put(thread_get_outdated, 1)

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
        self._threads.put(thread_install_pkgs, 0)

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
        self._threads.put(thread_uninstall_pkgs, 0)

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
        self._threads.put(thread_upgrade_pkgs, 0)

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
        self._threads.put(thread_upgrade_pkgs, 0)


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


class PyInstallerToolWindow(Ui_PyInstallerTool, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._setup_others()
        self._threads = ThreadRepo(300)
        self._task_retcode = None
        self._def_conf = {}
        self._pyitool_pyenv = None
        self._pyi_tool = PyiTool()
        self.widget_group = (
            self.tabWidget,
            self.pb_select_py_env,
            self.pb_reinstall_pyi,
            self.cb_log_level,
            self.le_exefile_specfile_name,
            self.pb_gen_executable,
        )
        self.set_platform_info()
        self.pyi_running_mov = QMovie(
            os.path.join(sources_path, 'loading.gif')
        )
        self.pyi_running_mov.setScaledSize(QSize(16, 16))
        self._connect_signal_slot()

    def closeEvent(self, event):
        if not self._threads.is_empty():
            NewMessageBox(
                '提醒',
                '生成任务正在运行中，关闭界面后任务将在后台运行，请勿对相关储存目录进行任何操作，否则可能会破坏生成的文件！',
                QMessageBox.Warning,
            ).exec()
        self.get_last_status()
        save_conf(self._def_conf, 'pyic')
        event.accept()

    def show(self):
        super().show()
        self._apply_def_conf()
        self._pyi_tool.initialize(
            self._def_conf.get('py_info', ''),
            self._def_conf.get('project_root', os.getcwd()),
        )
        self.set_pyi_info()

    def _setup_others(self):
        # 替换“主程序”LineEdit控件
        self.le_program_entry = QLineEditMod('file', {'.py', '.pyc', '.pyw'})
        self.le_program_entry.setPlaceholderText('程序启动入口，可将格式正确的文件拖到此处')
        self.horizontalLayout_3.replaceWidget(
            self.le_program_entry_old, self.le_program_entry
        )
        self.le_program_entry_old.deleteLater()
        # 替换“其他模块搜索路径”TextEdit控件
        self.te_module_search_path = QTextEditMod('dir')
        self.te_module_search_path.setPlaceholderText(
            '其他模块搜索目录，可留空，仅在PyInstaller无法自动搜索到模块时使用。可将格式正确的文件夹直接拖到此处。'
        )
        self.verticalLayout_3.replaceWidget(
            self.te_module_search_path_old, self.te_module_search_path
        )
        self.te_module_search_path_old.deleteLater()
        # 替换“非源代码资源文件”LineEdit控件
        self.te_other_data = QTextEditMod('file')
        self.te_other_data.setPlaceholderText(
            '其他需要一起打包的非源代码资源文件，可留空。注意资源文件要在项目'
            '根目录范围内，否则打包后程序可能无法运行。可将格式正确的文件直接拖到此处。'
        )
        self.verticalLayout_4.replaceWidget(
            self.te_other_data_old, self.te_other_data
        )
        self.te_other_data_old.deleteLater()
        # 替换“文件图标路径”LineEdit控件
        self.le_file_icon_path = QLineEditMod('file', {'.ico', '.icns'})
        self.le_file_icon_path.setPlaceholderText('可执行文件图标，可将格式正确的文件拖到此处')
        self.horizontalLayout_11.replaceWidget(
            self.le_file_icon_path_old, self.le_file_icon_path
        )
        self.le_file_icon_path_old.deleteLater()
        self.le_exefile_specfile_name.setValidator(
            QRegExpValidator(QRegExp(r'[^\\/:*?"<>|]*'))
        )

    def _connect_signal_slot(self):
        self._pyi_tool.executed.connect(self.task_completion_tip)
        self._pyi_tool.readline.connect(self.te_pyi_out_stream.append)
        self.pb_select_py_env.clicked.connect(win_ch_pyenv.show)
        self.le_program_entry.textChanged.connect(self.set_le_project_root)
        self.pb_select_module_search_path.clicked.connect(
            self.set_te_module_search_path
        )
        self.pb_select_program_entry.clicked.connect(self.set_le_program_entry)
        self.pb_up_level_root.clicked.connect(
            lambda: self.project_root_level('up')
        )
        self.pb_reset_root_level.clicked.connect(
            lambda: self.project_root_level('reset')
        )
        self.pb_clear_module_search_path.clicked.connect(
            self.te_module_search_path.clear
        )
        self.pb_select_other_data.clicked.connect(self.set_te_other_data)
        self.pb_clear_other_data.clicked.connect(self.te_other_data.clear)
        self.pb_select_file_icon.clicked.connect(self.set_le_file_icon_path)
        self.pb_select_spec_dir.clicked.connect(self.set_le_spec_dir)
        self.pb_select_temp_working_dir.clicked.connect(
            self.set_le_temp_working_dir
        )
        self.pb_select_output_dir.clicked.connect(self.set_le_output_dir)
        self.pb_select_upx_search_path.clicked.connect(
            self.set_le_upx_search_path
        )
        self.pb_select_version_file.clicked.connect(self.set_le_version_file)
        self.pb_gen_executable.clicked.connect(self.build_executable)

    def set_le_program_entry(self):
        selected_file = self._select_file_dir(
            '选择主程序',
            self._def_conf.get('project_root', ''),
            file_filter='脚本文件 (*.py *.pyc *.pyw)',
        )[0]
        if not selected_file:
            return
        self.le_program_entry.setText(selected_file)

    def set_le_project_root(self):
        self.le_project_root.setText(
            os.path.dirname(self.le_program_entry.text())
        )

    def set_te_module_search_path(self):
        selected_dir = self._select_file_dir(
            '其他模块搜索目录', self._def_conf.get('project_root', ''), cht='dir'
        )[0]
        if not selected_dir:
            return
        self.te_module_search_path.append(selected_dir)

    def set_te_other_data(self):
        selected_files = self._select_file_dir(
            '选择非源码资源文件', self._def_conf.get('project_root', ''), mult=True
        )
        if not selected_files:
            return
        self.te_other_data.append('\n'.join(selected_files))

    def set_le_file_icon_path(self):
        selected_file = self._select_file_dir(
            '选择可执行文件图标',
            self._def_conf.get('project_root', ''),
            file_filter='图标文件 (*.ico *.icns)',
        )[0]
        if not selected_file:
            return
        self.le_file_icon_path.setText(selected_file)

    def set_le_spec_dir(self):
        selected_dir = self._select_file_dir(
            '选择SPEC文件储存目录', self._def_conf.get('project_root', ''), cht='dir'
        )[0]
        if not selected_dir:
            return
        self.le_spec_dir.setText(selected_dir)

    def set_le_temp_working_dir(self):
        selected_dir = self._select_file_dir(
            '选择临时文件目录', self._def_conf.get('project_root', ''), cht='dir'
        )[0]
        if not selected_dir:
            return
        self.le_temp_working_dir.setText(selected_dir)

    def set_le_output_dir(self):
        selected_dir = self._select_file_dir(
            '选择打包文件储存目录', self._def_conf.get('project_root', ''), cht='dir'
        )[0]
        if not selected_dir:
            return
        self.le_output_dir.setText(selected_dir)

    def set_le_upx_search_path(self):
        selected_dir = self._select_file_dir(
            '选择UPX程序搜索目录', self._def_conf.get('project_root', ''), cht='dir'
        )[0]
        if not selected_dir:
            return
        self.le_upx_search_path.setText(selected_dir)

    def set_le_version_file(self):
        pass

    def _select_file_dir(
        self,
        title='',
        start='',
        cht='file',
        mult=False,
        file_filter='所有文件 (*)',
    ):
        file_dir_paths = []
        if cht == 'file' and mult:
            if not title:
                title = '选择多文件'
            path_getter = QFileDialog.getOpenFileNames
        elif cht == 'file' and not mult:
            if not title:
                title = '选择文件'
            path_getter = QFileDialog.getOpenFileName
        elif cht == 'dir':
            if not title:
                title = '选择文件夹'
            path_getter = QFileDialog.getExistingDirectory
        else:
            return file_dir_paths
        if cht == 'file' and not mult:
            path = path_getter(self, title, start, file_filter)[0]
            if not path:
                file_dir_paths.append('')
            else:
                file_dir_paths.append(os.path.realpath(path))
        elif cht == 'file' and mult:
            paths = path_getter(self, title, start, file_filter)[0]
            file_dir_paths.extend(
                os.path.realpath(path) for path in paths if path
            )
            if not file_dir_paths:
                file_dir_paths.append('')
        elif cht == 'dir':
            path = path_getter(self, title, start)
            if not path:
                file_dir_paths.append('')
            else:
                file_dir_paths.append(os.path.realpath(path))
        return file_dir_paths

    def _set_pyenv_and_update_info(self):
        self._pyitool_pyenv = win_ch_pyenv.pyenvs[
            win_ch_pyenv.lw_py_envs.currentRow()
        ]
        self.lb_py_info.setText(self._pyitool_pyenv.py_info())
        self._pyi_tool.initialize(
            self._pyitool_pyenv.env_path,
            self._def_conf.get('program_entry', os.getcwd()),
        )
        self.set_pyi_info()

    def _apply_def_conf(self):
        if not self._def_conf:
            self._def_conf.update(load_conf('pyic'))
        self.le_program_entry.setText(self._def_conf.get('program_entry', ''))
        self.le_project_root.setText(self._def_conf.get('project_root', ''))
        self.te_module_search_path.setText(
            '\n'.join(self._def_conf.get('module_search_path', []))
        )
        self.te_other_data.setText(
            '\n'.join(otp[0] for otp in self._def_conf.get('other_data', []))
        )
        self.le_file_icon_path.setText(
            self._def_conf.get('file_icon_path', '')
        )
        pack_to_one = self._def_conf.get('pack_to_one', 'dir')
        if pack_to_one == 'file':
            self.rb_pack_to_one_file.setChecked(True)
        else:
            self.rb_pack_to_one_dir.setChecked(True)
        self.cb_execute_with_console.setChecked(
            self._def_conf.get('execute_with_console', True)
        )
        self.cb_without_confirm.setChecked(
            self._def_conf.get('without_confirm', False)
        )
        self.cb_use_upx.setChecked(self._def_conf.get('use_upx', False))
        self.cb_clean_before_build.setChecked(
            self._def_conf.get('clean_before_build', True)
        )
        self.le_temp_working_dir.setText(
            self._def_conf.get('temp_working_dir', '')
        )
        self.le_output_dir.setText(self._def_conf.get('output_dir', ''))
        self.le_spec_dir.setText(self._def_conf.get('spec_dir', ''))
        self.le_upx_search_path.setText(
            self._def_conf.get('upx_search_path', '')
        )
        self.le_version_file.setText(self._def_conf.get('version_file', ''))
        self.te_upx_exclude_files.setText(
            '\n'.join(self._def_conf.get('upx_exclude_files', []))
        )
        py_path = self._def_conf.get('py_info', '')
        if py_path:
            try:
                self._pyitool_pyenv = PyEnv(py_path)
                self.lb_py_info.setText(self._pyitool_pyenv.py_info())
            except Exception:
                pass
        self.le_exefile_specfile_name.setText(
            self._def_conf.get('exefile_specfile_name', '')
        )
        self.cb_log_level.setCurrentText(
            self._def_conf.get('log_level', 'INFO')
        )

    def get_last_status(self):
        project_root = self.le_project_root.text()
        self._def_conf['project_root'] = project_root
        self._def_conf['program_entry'] = self.le_program_entry.local_path
        self._def_conf[
            'module_search_path'
        ] = self.te_module_search_path.local_paths
        # 其他要打包的文件的本地路径和与项目根目录的相对位置：
        other_data_local_paths = self.te_other_data.local_paths
        other_data_relative_paths = []
        for other_data_path in other_data_local_paths:
            other_data_path = os.path.dirname(other_data_path)
            try:
                other_data_relative_paths.append(
                    os.path.relpath(other_data_path, project_root)
                )
            except Exception:
                continue
        self._def_conf['other_data'] = list(
            zip(other_data_local_paths, other_data_relative_paths)
        )
        self._def_conf['file_icon_path'] = self.le_file_icon_path.local_path
        if self.rb_pack_to_one_file.isChecked():
            self._def_conf['pack_to_one'] = 'file'
        else:
            self._def_conf['pack_to_one'] = 'dir'
        self._def_conf[
            'execute_with_console'
        ] = self.cb_execute_with_console.isChecked()
        self._def_conf['without_confirm'] = self.cb_without_confirm.isChecked()
        self._def_conf['use_upx'] = self.cb_use_upx.isChecked()
        self._def_conf[
            'clean_before_build'
        ] = self.cb_clean_before_build.isChecked()
        self._def_conf['temp_working_dir'] = self.le_temp_working_dir.text()
        self._def_conf['output_dir'] = self.le_output_dir.text()
        self._def_conf['spec_dir'] = self.le_spec_dir.text()
        self._def_conf['upx_search_path'] = self.le_upx_search_path.text()
        self._def_conf['version_file'] = self.le_version_file.text()
        self._def_conf['upx_exclude_files'] = [
            string
            for string in self.te_upx_exclude_files.toPlainText().split(' ')
            if string
        ]
        if self._pyitool_pyenv is None:
            self._def_conf['py_info'] = ''
        else:
            self._def_conf['py_info'] = self._pyitool_pyenv.env_path
        self._def_conf[
            'exefile_specfile_name'
        ] = self.le_exefile_specfile_name.text()
        self._def_conf['log_level'] = self.cb_log_level.currentText()

    def set_pyi_info(self):
        if self._pyitool_pyenv:
            self.lb_pyi_info.setText(
                f'PyInstaller - {self._pyi_tool.pyi_info()}'
            )
        else:
            self.lb_pyi_info.clear()

    def set_platform_info(self):
        self.lb_platform_info.setText(f'{platform()}-{machine()}')

    def project_root_level(self, opt):
        if opt not in ('up', 'reset'):
            return
        root = self.le_project_root.text()
        if not root:
            return
        if opt == 'up':
            self.le_project_root.setText(os.path.dirname(root))
        elif opt == 'reset':
            deep = self.le_program_entry.text()
            if not deep:
                return
            self.le_project_root.setText(os.path.dirname(deep))

    def _check_requireds(self):
        self.get_last_status()
        program_entry = self._def_conf.get('program_entry', '')
        if not program_entry:
            NewMessageBox('错误', '主程序未填写！', QMessageBox.Critical).exec()
            return False
        if not os.path.isfile(program_entry):
            NewMessageBox('错误', '主程序文件不存在！', QMessageBox.Critical).exec()
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
            NewMessageBox('任务结束', '可执行文件已打包完成！').exec()
        else:
            NewMessageBox(
                '任务结束', '可执行文件生成失败，请检查错误信息！', QMessageBox.Critical
            ).exec()

    def build_executable(self):
        if not self._check_requireds():
            return
        self.te_pyi_out_stream.clear()
        self._pyi_tool.initialize(
            self._def_conf.get('py_info', ''),
            self._def_conf.get('project_root', os.getcwd()),
        )
        if not self._pyi_tool.pyi_ready:
            NewMessageBox(
                '提示', '打包库不可用，请将PYINSTALLER安装到所选环境。', QMessageBox.Warning
            ).exec()
            return
        self._pyi_tool.prepare_cmd(self._def_conf)
        self.handle = self._pyi_tool.handle()
        build = NewTask(self._pyi_tool.execute_cmd)
        build.started.connect(self.lock_widgets)
        build.started.connect(lambda: self.show_running('正在生成可执行文件...'))
        build.finished.connect(self.hide_running)
        build.finished.connect(self.release_widgets)
        build.start()
        self._threads.put(build, 0)


class PyiToolChoosePyEnvWindow(Ui_PyiToolChoosePyEnv, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self._connect_signal_slot()

    def _connect_signal_slot(self):
        self.lw_py_envs.pressed.connect(self.close)

    def pyenv_list_update(self):
        row_size = QSize(0, 28)
        self.lw_py_envs.clear()
        for py_env in self.pyenvs:
            item = QListWidgetItem(str(py_env))
            item.setSizeHint(row_size)
            self.lw_py_envs.addItem(item)

    def close(self):
        super().close()
        win_pyi_tool._set_pyenv_and_update_info()

    def show(self):
        self.pyenvs = get_pyenv_list(load_conf('pths'))
        super().show()
        self.pyenv_list_update()


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
    app_awesomepykit = QApplication(sys.argv)
    app_awesomepykit.setWindowIcon(
        QIcon(os.path.join(sources_path, 'icon.ico'))
    )
    win_info_panel = InformationPanelWindow()
    win_main_interface = MainInterfaceWindow()
    win_package_mgr = PackageManagerWindow()
    win_ch_pyenv = PyiToolChoosePyEnvWindow()
    win_pyi_tool = PyInstallerToolWindow()
    win_mirror_mgr = MirrorSourceManagerWindow()
    win_main_interface.show()
    sys.exit(app_awesomepykit.exec())

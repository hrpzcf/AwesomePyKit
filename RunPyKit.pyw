# -*- coding: utf-8 -*-

import os
import sys

from PyQt5.QtCore import QSize, QThread, Qt
from PyQt5.QtGui import QFont, QMovie
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

from AwesomePyKit.interface import *
from AwesomePyKit.library import *
from AwesomePyKit.library.libm import PyEnv


class MainWindow(Ui_MainWin, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self._binding()

    def _binding(self):
        self.about.triggered.connect(self._show_about)
        self.description.triggered.connect(self._show_usinghelp)
        self.btn_manPacks.clicked.connect(self._show_pkgmgr)
        self.btn_setIndex.clicked.connect(self._show_indexmgr)

    @staticmethod
    def _show_about():
        try:
            with open(
                'AwesomePyKit/help/About.html', encoding='utf-8'
            ) as help_html:
                info = help_html.read()
                icon = QMessageBox.Information
        except Exception:
            info = '"关于"信息文件(./AwesomePyKit/help/About.html)已丢失。'
            icon = QMessageBox.Critical
        about_panel = QMessageBox(icon, '关于', info)
        about_panel.addButton('确定', QMessageBox.AcceptRole)
        about_panel.exec()

    @staticmethod
    def _show_usinghelp():
        help_panel_window.setWindowTitle('使用帮助')
        try:
            with open(
                'AwesomePyKit/help/UsingHelp.html', encoding='utf-8'
            ) as using_html:
                help_panel_window.help_panel.setText(using_html.read())
        except Exception:
            help_panel_window.help_panel.setText(
                '"使用帮助"文件(./AwesomePyKit/help/UsingHelp.html)已丢失。'
            )
        help_panel_window.show()

    @staticmethod
    def _show_pkgmgr():
        pkg_manager_window.show()

    @staticmethod
    def _show_indexmgr():
        index_manager_window.show()


class PkgMgrWindow(Ui_PkgMgr, QMainWindow):
    def __init__(self):
        super(PkgMgrWindow, self).__init__()
        self.setupUi(self)
        self._setupOthers()
        self._py_paths_list = load_conf('pths')
        self._py_envs_list = get_pyenv_list(self._py_paths_list)
        self._running_threads = []
        self._cur_pkgs_info_list = []

    def _setupOthers(self):
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
        self.loading_mov.setScaledSize(QSize(20, 20))
        self.lb_loading_gif = QLabel()
        self.lb_loading_tips = QLabel()
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.lb_loading_gif)
        hlayout.addWidget(self.lb_loading_tips)
        hlayout.setStretch(0, 1)
        hlayout.setStretch(1, 9)
        self.glo_table_btns.addLayout(hlayout, 0, 0, 1, 2)

    def show(self):
        super(PkgMgrWindow, self).show()
        self.list_widget_pyenvs_update()
        self.li_py_env_list.setCurrentRow(0)
        self._binding()

    def closeEvent(self, event):
        self._stop_running_thread()
        event.accept()

    def start_waiting(self, text):
        self.lb_loading_tips.setText(text)
        self.lb_loading_gif.setMovie(self.loading_mov)
        self.loading_mov.start()

    def stop_waiting(self):
        self.loading_mov.stop()
        self.lb_loading_gif.clear()
        self.lb_loading_tips.clear()

    def clean_finished_thread(self):
        for index, running_thread in enumerate(self._running_threads):
            if running_thread.isFinished():
                self._running_threads.pop(index)

    def _stop_running_thread(self):
        for running_thread in self._running_threads:
            running_thread.exit()

    def _binding(self):
        self.btn_autosearch.clicked.connect(self._auto_search_py_envs)
        self.btn_clearexpired.clicked.connect(self._clear_expired)
        self.btn_delselected.clicked.connect(self._del_selected)
        self.btn_addmanully.clicked.connect(self._add_py_path_manully)
        self.cb_check_uncheck_all.clicked.connect(self._select_all_none)
        self.li_py_env_list.clicked.connect(self._get_pkgs_info)
        self.btn_check_for_updates.clicked.connect(self._check_for_updates)

    def list_widget_pyenvs_update(self):
        cur_py_env_index = self.li_py_env_list.currentRow()
        self.li_py_env_list.clear()
        for py_env in self._py_envs_list:
            self.li_py_env_list.addItem(str(py_env))
        if cur_py_env_index != -1:
            self.li_py_env_list.setCurrentRow(cur_py_env_index)

    def _table_widget_pkgs_info_update(self):
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(len(self._cur_pkgs_info_list))
        cur_row = self.li_py_env_list.currentRow()
        if cur_row != -1:
            self.lb_installed_pkgs_info.setText(
                f'【{str(self._py_envs_list[cur_row])}】:'
            )
        for rowind, info in enumerate(self._cur_pkgs_info_list):
            for colind, info_item in enumerate(info):
                self.tw_installed_info.setItem(
                    rowind, colind, QTableWidgetItem(info_item)
                )

    def clear_table_widget(self):
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(0)

    def _get_pkgs_info(self):
        index_selected = self.li_py_env_list.currentRow()
        if index_selected == -1:
            return

        def get_pkgs_info():
            pkgs_info = self._py_envs_list[index_selected].pkgs_info()
            self._cur_pkgs_info_list.clear()
            for pkg_info in pkgs_info:
                pkg_info = list(pkg_info)
                pkg_info.extend(('', ''))
                self._cur_pkgs_info_list.append(pkg_info)

        thread_get_pkgs_info = NewTask(get_pkgs_info)
        thread_get_pkgs_info.started.connect(self.lock_widgets)
        thread_get_pkgs_info.started.connect(
            lambda: self.start_waiting('正在加载模块信息...')
        )
        thread_get_pkgs_info.finished.connect(
            self._table_widget_pkgs_info_update
        )
        thread_get_pkgs_info.finished.connect(self.stop_waiting)
        thread_get_pkgs_info.finished.connect(self.release_widgets)
        thread_get_pkgs_info.finished.connect(self.clean_finished_thread)
        thread_get_pkgs_info.start()
        self._running_threads.append(thread_get_pkgs_info)

    def _index_selected_rows(self):
        row_indexs = []
        for item in self.tw_installed_info.selectedItems():
            row_index = item.row()
            if row_index not in row_indexs:
                row_indexs.append(row_index)
        return row_indexs

    def _select_all_none(self):
        is_checked = self.cb_check_uncheck_all.isChecked()
        if is_checked:
            self.tw_installed_info.selectAll()
        else:
            self.tw_installed_info.clearSelection()

    def _auto_search_py_envs(self):
        def search_envs():
            for py_path in all_py_paths():
                if py_path in self._py_paths_list:
                    continue
                try:
                    self._py_paths_list.append(py_path)
                    self._py_envs_list.append(PyEnv(py_path))
                except Exception:
                    continue

        thread_search_envs = NewTask(search_envs)
        thread_search_envs.started.connect(self.lock_widgets)
        thread_search_envs.started.connect(
            lambda: self.start_waiting('正在搜索Python目录...')
        )
        thread_search_envs.finished.connect(self.clear_table_widget)
        thread_search_envs.finished.connect(self.list_widget_pyenvs_update)
        thread_search_envs.finished.connect(self.stop_waiting)
        thread_search_envs.finished.connect(self.release_widgets)
        thread_search_envs.finished.connect(self.clean_finished_thread)
        thread_search_envs.finished.connect(
            lambda: save_conf(self._py_paths_list, 'pths')
        )
        thread_search_envs.start()
        self._running_threads.append(thread_search_envs)

    def _clear_expired(self):
        cleaned_py_paths = clean_py_paths(self._py_paths_list)
        self._py_paths_list.clear()
        self._py_paths_list.extend(cleaned_py_paths)
        self._py_envs_list.clear()
        self._py_envs_list.extend(get_pyenv_list(self._py_paths_list))
        self.list_widget_pyenvs_update()
        save_conf(self._py_paths_list, 'pths')

    def _del_selected(self):
        cur_index = self.li_py_env_list.currentRow()
        if cur_index == -1:
            return
        del self._py_envs_list[cur_index]
        del self._py_paths_list[cur_index]
        self.li_py_env_list.removeItemWidget(
            self.li_py_env_list.takeItem(cur_index)
        )
        save_conf(self._py_paths_list, 'pths')
        self.clear_table_widget()

    def _add_py_path_manully(self):
        input_dialog = MyInputDialog(
            self, 560, 0, '添加Python环境', '请输入有效的Python目录路径：'
        )
        py_path, ok = input_dialog.getText()
        if not (ok and py_path):
            return
        if not check_py_path(py_path):
            return self.statusbar.showMessage('无效的Python目录路径！')
        py_path = os.path.join(py_path, '')
        if py_path in self._py_paths_list:
            return self.statusbar.showMessage('要添加的Python目录已存在。')
        self._py_paths_list.append(py_path)
        self._py_envs_list.append(PyEnv(py_path))
        self.list_widget_pyenvs_update()
        save_conf(self._py_paths_list, 'pths')

    def _check_for_updates(self):
        if self.tw_installed_info.rowCount() == 0:
            return
        cur_row = self.li_py_env_list.currentRow()
        if cur_row == -1:
            return

        def get_outdated():
            outdateds = self._py_envs_list[cur_row].outdated()
            for outdated_info in outdateds:
                for row in self._cur_pkgs_info_list:
                    if outdated_info[0] == row[0]:
                        row[2] = outdated_info[2]

        thread_get_outdated = NewTask(get_outdated)
        thread_get_outdated.started.connect(self.lock_widgets)
        thread_get_outdated.started.connect(
            lambda: self.start_waiting('正在检查更新，请耐心等待...')
        )
        thread_get_outdated.finished.connect(
            self._table_widget_pkgs_info_update
        )
        thread_get_outdated.finished.connect(self.stop_waiting)
        thread_get_outdated.finished.connect(self.release_widgets)
        thread_get_outdated.finished.connect(self.clean_finished_thread)
        thread_get_outdated.start()
        self._running_threads.append(thread_get_outdated)

    def lock_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.btn_clearexpired,
            self.li_py_env_list,
            self.te_info_stream,
            self.tw_installed_info,
            self.cb_check_uncheck_all,
            self.btn_check_for_updates,
            self.btn_install_package,
            self.btn_uninstall_package,
            self.btn_up_grade_package,
            self.btn_up_grade_all,
        ):
            widget.setEnabled(False)

    def release_widgets(self):
        for widget in (
            self.btn_autosearch,
            self.btn_addmanully,
            self.btn_delselected,
            self.btn_clearexpired,
            self.li_py_env_list,
            self.te_info_stream,
            self.tw_installed_info,
            self.cb_check_uncheck_all,
            self.btn_check_for_updates,
            self.btn_install_package,
            self.btn_uninstall_package,
            self.btn_up_grade_package,
            self.btn_up_grade_all,
        ):
            widget.setEnabled(True)


class MyInputDialog(QInputDialog):
    def __init__(self, parent, sw=560, sh=0, title='', label=''):
        super(MyInputDialog, self).__init__(parent)
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


class IndexMgrWindow(Ui_IndexMgr, QMainWindow):
    def __init__(self):
        super(IndexMgrWindow, self).__init__()
        self.setupUi(self)
        self._urls_dict = load_conf('urls')
        self._binding()

    def show(self):
        super(IndexMgrWindow, self).show()
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

    def _binding(self):
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
                    '没有找到pip可执行程序，请在"Python包管理"界面添加Python目录到列表。'
                )
        else:
            for py_path in py_paths:
                try:
                    return PyEnv(py_path)
                except Exception:
                    continue
            else:
                self.statusbar.showMessage(
                    '没有找到pip可执行程序，请在"Python包管理"界面添加Python目录到列表。'
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


class HelpPanelWindow(Ui_ImPanel, QWidget):
    def __init__(self):
        super(HelpPanelWindow, self).__init__()
        self.setupUi(self)

    def closeEvent(self, *args, **kwargs):
        self.resize(1, 1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_interface_window = MainWindow()
    pkg_manager_window = PkgMgrWindow()
    index_manager_window = IndexMgrWindow()
    help_panel_window = HelpPanelWindow()
    main_interface_window.show()
    sys.exit(app.exec_())

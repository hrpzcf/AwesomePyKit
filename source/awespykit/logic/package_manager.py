# coding: utf-8

from os import path
from typing import Union

from com import *
from fastpip import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from settings import *
from ui import *
from utils import *
from utils.widgets import TextEdit

from .generic_output import GenericOutputWindow
from .messagebox import MessageBox
from .query_file_path import QueryFilePath


class PackageManagerWindow(Ui_package_manager, QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.config = PackageManagerConfig()
        self.__output = GenericOutputWindow(self)
        self.__handle = PyEnv.register(self.__output.add_line)
        self.__setup_other_widgets()
        self.signal_slot_connection()
        self.env_list = [PyEnv(p) for p in self.config.pypaths]
        self.__cur_pkgs_info = dict()
        self.__reverseds = [True, True, True, True]
        self.selected_index = -1
        self.__is_busy = False
        self.thread_repo = ThreadRepo(500)

    def __setup_other_widgets(self):
        self.tw_installed_info.setColumnWidth(0, 220)
        horiz_head = self.tw_installed_info.horizontalHeader()
        horiz_head.setSectionResizeMode(0, QHeaderView.Interactive)
        horiz_head.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        horiz_head.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        horiz_head.setSectionResizeMode(3, QHeaderView.Stretch)
        self.loading_mov = QMovie(":/loading.gif")
        self.loading_mov.setScaledSize(QSize(16, 16))

    def __move_output(self):
        if self.__output.isHidden() or self.__output.linkage == Linkage.NoLink:
            return
        fgeo = self.frameGeometry()
        geo = self.geometry()
        if self.__output.linkage == Linkage.Top:
            point = fgeo.bottomLeft()
            width = geo.width()
            height = None
        elif self.__output.linkage == Linkage.Left:
            point = fgeo.topRight()
            width = None
            height = geo.height()
        elif self.__output.linkage == Linkage.Right:
            point = fgeo.topLeft()
            width = None
            height = geo.height()
        else:
            return
        self.__output.set_geometry(point, width, height)

    def moveEvent(self, event: QMoveEvent):
        self.__move_output()

    def resizeEvent(self, event: QResizeEvent):
        self.__move_output()

    def display(self):
        self.resize(*self.config.window_size)
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()
        self.list_widget_pyenvs_update()
        self.lw_env_list.setCurrentRow(self.selected_index)

    def show_hide_output(self):
        if self.__output.isHidden():
            if self.__output.not_shown_yet():
                self.__output.resize(*self.config.output_winsize)
                self.__output.showNormal()
                self.__output.linkage = Linkage(self.config.output_side)
                if self.__output.linkage != Linkage.NoLink:
                    self.__move_output()
            else:
                self.__output.showNormal()
                self.__move_output()
            self.__output.clear_content()
        else:
            self.__output.hide()

    @staticmethod
    def __stop_before_close():
        return not MessageBox(
            "警告",
            "当前有任务正在运行！\n是否尝试停止所有正在运行的任务并关闭窗口？",
            QMessageBox.Question,
            (("accept", "尝试停止并关闭"), ("reject", "取消")),
        ).exec_()

    def __save_window_size(self):
        if not (self.isMaximized() or self.isMinimized()):
            self.config.window_size = self.width(), self.height()
        if not (self.__output.isMaximized() or self.__output.isMinimized()):
            self.config.output_winsize = self.__output.width(), self.__output.height()

    def closeEvent(self, event: QCloseEvent):
        if not self.thread_repo.is_empty():
            if self.__stop_before_close():
                self.thread_repo.stop_all()
                self.__output.close()
                self.environ_changed_clear_pkgs()
                event.accept()
            else:
                event.ignore()
        else:
            self.__output.close()
        self.__save_window_size()
        if not self.__output.not_shown_yet():
            self.config.output_side = self.__output.linkage
        self.config.save_config()

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
        self.btn_autosearch.clicked.connect(self.auto_search_environ)
        self.btn_delselected.clicked.connect(self.del_selected_environ)
        self.btn_addmanully.clicked.connect(self.add_environ_manully)
        self.cb_check_uncheck_all.clicked.connect(self.selectall_unselectall)
        self.lw_env_list.clicked.connect(lambda: self.get_pkgs_info(0))
        self.lw_env_list.currentRowChanged.connect(self.environ_changed_clear_pkgs)
        self.btn_check_for_updates.clicked.connect(self.check_cur_pkgs_for_updates)
        self.btn_install_package.clicked.connect(self.set_win_install_package_envinfo)
        self.btn_uninstall_package.clicked.connect(self.uninstall_packages)
        self.btn_upgrade_package.clicked.connect(self.upgrade_packages)
        self.btn_upgrade_all.clicked.connect(self.upgrade_all_packages)
        self.tw_installed_info.horizontalHeader().sectionClicked[int].connect(
            self.__sort_by_column
        )
        self.tw_installed_info.clicked.connect(self.__show_label_selected_num)
        self.le_search_pkgs_kwd.textChanged.connect(self.search_pkg_name_by_kwd)
        self.lw_env_list.customContextMenuRequested.connect(
            self.environlist_contextmenu
        )
        self.tw_installed_info.customContextMenuRequested.connect(
            self.packagesinfo_contextmenu
        )
        self.uiPushButton_show_output.clicked.connect(self.show_hide_output)

    def selected_envfolder(self):
        index = self.lw_env_list.currentRow()
        environ_path = self.env_list[index].env_path
        if not path.isdir(environ_path):
            return MessageBox("提示", "所选环境目录不存在！").exec_()
        launch_explorer(environ_path)

    def export_packages_info(self):
        index = self.lw_env_list.currentRow()
        if index == -1:
            return
        environ = self.env_list[index]
        if not environ.pip_ready:
            return MessageBox("提示", "所选环境不是有效环境！").exec_()
        fullpath = QFileDialog.getSaveFileName(
            self,
            "选择文件夹",
            path.join(self.config.last_path, "requirements.txt"),
            "文本文件 (*.txt)",
        )[0]
        if not fullpath:
            return
        dir_path, name = path.split(fullpath)
        self.config.last_path = dir_path
        self.setCursor(Qt.WaitCursor)
        thread_export = QThreadModel(environ.freeze, dir_path, name, no_path=True)
        thread_export.at_finish(lambda: self.setCursor(Qt.ArrowCursor))
        thread_export.start()
        self.thread_repo.put(thread_export, 1)

    def query_names(self):
        if self.selected_index == -1:
            return MessageBox("提示", "还没有选中任何环境！").exec_()
        pkg_names = self.package_names_selected()
        if not pkg_names:
            pkg_name = None
            mode = QMode.NotSPCF
        else:
            pkg_name = pkg_names[0]
            mode = QMode.Pkg2Imp
        environ = self.env_list[self.selected_index]
        query_window = NameQueryPanel(self)
        query_window.initialize(environ, pkg_name, mode=mode)
        query_window.display()
        if pkg_name is not None:
            query_window.start_query_name()

    def environlist_contextmenu(self):
        contextmenu = QMenu(self)

        action = QAction(QIcon(":/openfd.png"), "打开目录", self)
        action.triggered.connect(self.selected_envfolder)
        contextmenu.addAction(action)

        action = QAction(QIcon(":/export.png"), "导出包列表", self)
        action.triggered.connect(self.export_packages_info)
        contextmenu.addAction(action)

        contextmenu.addSeparator()

        action = QAction(QIcon(":/search.png"), "自动搜索", self)
        action.triggered.connect(self.auto_search_environ)
        contextmenu.addAction(action)

        action = QAction(QIcon(":/add.png"), "手动添加", self)
        action.triggered.connect(self.add_environ_manully)
        contextmenu.addAction(action)

        action = QAction(QIcon(":/delete.png"), "移除环境", self)
        action.triggered.connect(self.del_selected_environ)
        contextmenu.addAction(action)

        contextmenu.setStyleSheet("QMenu {padding: 10px; border: 1px solid black}")
        contextmenu.exec_(QCursor.pos())

    def packagesinfo_contextmenu(self):
        contextmenu = QMenu(self)
        action_list = list()

        action = QAction(QIcon(":/upgrade.png"), "升级", self)
        action.triggered.connect(self.upgrade_packages)
        action_list.append(action)
        contextmenu.addAction(action)

        action = QAction(QIcon(":/uninstall.png"), "卸载", self)
        action.triggered.connect(self.uninstall_packages)
        action_list.append(action)
        contextmenu.addAction(action)

        action = QAction(QIcon(":/query.png"), "查询", self)
        action.triggered.connect(self.query_names)
        action_list.append(action)
        contextmenu.addAction(action)

        action = QAction(QIcon(":/refresh.png"), "刷新", self)
        action.triggered.connect(lambda: self.get_pkgs_info(0))
        action_list.append(action)
        contextmenu.addAction(action)

        for action in action_list:
            if self.__is_busy:
                action.setEnabled(False)
            else:
                action.setEnabled(True)

        contextmenu.setStyleSheet("QMenu {padding: 10px; border: 1px solid black}")
        contextmenu.exec_(QCursor.pos())

    def set_win_install_package_envinfo(self):
        if not self.env_list:
            return MessageBox("提示", "没有可选的 Python 环境。").exec_()
        if self.selected_index <= -1:
            return MessageBox("提示", "没有选择任何 Python 环境。").exec_()
        if self.selected_index >= len(self.env_list):
            return MessageBox("错误", "异常：当前选择下标超出范围。").exec_()
        PackageInstallWindow(self, self.install_packages).set_target_environ(
            self.env_list[self.selected_index]
        )

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
        self.__show_label_selected_num(False)
        # 搜索功能比较简单，关键字是单独一个字母时，检索以该字母开头的模块
        # 如果不是单字母，则判断包名是否以关键词首字母开头、包名是否包含后续单词

    def __show_label_selected_num(self, clear=True):
        selected = len(self.indexs_of_selected_rows())
        if selected != len(self.__cur_pkgs_info):
            self.cb_check_uncheck_all.setChecked(False)
        else:
            self.cb_check_uncheck_all.setChecked(True)
        if clear and selected == 0:
            self.lb_num_selected_items.clear()
            return
        self.lb_num_selected_items.setText(f"选中数量：{selected}")

    def list_widget_pyenvs_update(self):
        row_size = QSize(0, 28)
        cur_py_env_index = self.lw_env_list.currentRow()
        self.lw_env_list.clear()
        for env in self.env_list:
            item = QListWidgetItem(QIcon(":/python.png"), str(env))
            item.setSizeHint(row_size)
            self.lw_env_list.addItem(item)
        if cur_py_env_index != -1:
            self.lw_env_list.setCurrentRow(cur_py_env_index)

    def table_widget_pkgs_info_update(self):
        self.lb_num_selected_items.clear()
        self.tw_installed_info.clearContents()
        self.tw_installed_info.setRowCount(len(self.__cur_pkgs_info))
        color_green = QColor(0, 170, 0)
        color_red = QColor(255, 0, 0)
        color_gray = QColor(243, 243, 243)
        for rowind, pkg_name in enumerate(self.__cur_pkgs_info):
            self.tw_installed_info.setVerticalHeaderItem(
                rowind, QTableWidgetItem(f" {rowind + 1} ")
            )
            item0 = QTableWidgetItem(f"{pkg_name}")
            self.tw_installed_info.setItem(rowind, 0, item0)
            even_num_row = rowind % 2
            if not even_num_row:
                item0.setBackground(color_gray)
            for colind, item_text in enumerate(
                self.__cur_pkgs_info.get(pkg_name, ["", "", ""])
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
        self.__is_busy = False

    def __sort_by_column(self, colind):
        if colind == 0:
            self.__cur_pkgs_info = dict(
                sorted(
                    self.__cur_pkgs_info.items(),
                    key=lambda x: x[0].lower(),
                    reverse=self.__reverseds[colind],
                )
            )
        else:
            self.__cur_pkgs_info = dict(
                sorted(
                    self.__cur_pkgs_info.items(),
                    key=lambda x: x[1][colind - 1],
                    reverse=self.__reverseds[colind],
                )
            )
        self.table_widget_pkgs_info_update()
        self.__reverseds[colind] = not self.__reverseds[colind]

    def environ_changed_clear_pkgs(self):
        if self.tw_installed_info.rowCount():
            self.lb_num_selected_items.clear()
            self.tw_installed_info.clearContents()
            self.tw_installed_info.setRowCount(0)
        self.__cur_pkgs_info.clear()
        self.selected_index = self.lw_env_list.currentRow()

    def get_pkgs_info(self, no_connect):
        if self.__is_busy:
            return
        self.__is_busy = True
        self.selected_index = self.lw_env_list.currentRow()
        if self.selected_index == -1:
            return None

        def do_get_pkgs_info():
            pkgs_info = self.env_list[self.selected_index].pkgs_info()
            self.__cur_pkgs_info.clear()
            for pkg_info in pkgs_info:
                self.__cur_pkgs_info[pkg_info[0]] = [pkg_info[1], "", ""]

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
        self.thread_repo.put(thread_get_pkgs_info, 1)
        return thread_get_pkgs_info

    def indexs_of_selected_rows(self):
        selected_row_indexs = [
            item.row() for item in self.tw_installed_info.selectedItems()[::4]
        ]
        selected_row_indexs.sort()
        return selected_row_indexs

    def package_names_selected(self):
        pkg_keys = tuple(self.__cur_pkgs_info.keys())
        return [pkg_keys[i] for i in self.indexs_of_selected_rows()]

    def selectall_unselectall(self):
        if self.cb_check_uncheck_all.isChecked():
            self.tw_installed_info.selectAll()
        else:
            self.tw_installed_info.clearSelection()
        self.__show_label_selected_num()

    def auto_search_environ(self):
        def search_environ():
            for _path in all_py_paths():
                if _path.lower() in path_list_lower:
                    continue
                try:
                    env = PyEnv(_path)
                except Exception:
                    continue
                self.env_list.append(env)
                self.config.pypaths.append(env.env_path)

        path_list_lower = [p.lower() for p in self.config.pypaths]
        thread_search_envs = QThreadModel(search_environ)
        thread_search_envs.at_start(
            self.lock_widgets,
            lambda: self.show_loading("正在搜索 Python 安装目录..."),
        )
        thread_search_envs.at_finish(
            self.environ_changed_clear_pkgs,
            self.list_widget_pyenvs_update,
            self.hide_loading,
            self.release_widgets,
        )
        thread_search_envs.start()
        self.thread_repo.put(thread_search_envs, 0)

    def del_selected_environ(self):
        cur_index = self.lw_env_list.currentRow()
        if cur_index == -1:
            return
        del self.env_list[cur_index]
        del self.config.pypaths[cur_index]
        self.lw_env_list.removeItemWidget(self.lw_env_list.takeItem(cur_index))
        self.environ_changed_clear_pkgs()

    def add_path_callback(self, _path):
        if not _path:
            return
        if not check_py_path(_path):
            return MessageBox(
                "警告",
                "无效的 Python 目录路径！",
                QMessageBox.Warning,
            ).exec_()
        if _path.lower() in [p.lower() for p in self.config.pypaths]:
            return MessageBox(
                "警告",
                "要添加的 Python 目录已存在。",
                QMessageBox.Warning,
            ).exec_()
        try:
            env = PyEnv(_path)
            self.env_list.append(env)
            self.config.pypaths.append(env.env_path)
        except Exception:
            return MessageBox(
                "警告",
                "目录添加失败，路径参数类型异常，请向开发者反馈~",
                QMessageBox.Warning,
            ).exec_()
        self.list_widget_pyenvs_update()

    def add_environ_manully(self):
        AddEnvironDialog(self, self.add_path_callback, "添加环境")

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
                self.__cur_pkgs_info.setdefault(outdated_info[0], ["", "", ""])[
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
        self.thread_repo.put(thread_get_outdated, 1)

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

    def install_packages(self, cur_env, tobe_installed):
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
                item = self.__cur_pkgs_info.setdefault(name, ["", "", ""])
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
        self.thread_repo.put(thread_install_pkgs, 0)

    def uninstall_packages(self):
        pkgs_info_keys = tuple(self.__cur_pkgs_info.keys())
        pkg_indexs = self.indexs_of_selected_rows()
        pkg_names = [pkgs_info_keys[index] for index in pkg_indexs]
        if not pkg_names:
            return MessageBox("提示", "没有选中任何项！").exec_()
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
                item = self.__cur_pkgs_info.setdefault(pkg_name, ["", "", ""])
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
        self.thread_repo.put(thread_uninstall_pkgs, 0)

    def upgrade_packages(self):
        pkgs_info_keys = tuple(self.__cur_pkgs_info.keys())
        pkg_indexs = self.indexs_of_selected_rows()
        names = [pkgs_info_keys[index] for index in pkg_indexs]
        if not names:
            return MessageBox("提示", "没有选中任何项！").exec_()
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
                item = self.__cur_pkgs_info.setdefault(pkg, ["", "", ""])
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
        self.thread_repo.put(thread_upgrade_pkgs, 0)

    def upgrade_all_packages(self):
        upgradeable = [i[0] for i in self.__cur_pkgs_info.items() if i[1][1]]
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
                item = self.__cur_pkgs_info.setdefault(pkg_name, ["", "", ""])
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
        self.thread_repo.put(thread_upgrade_pkgs, 0)


class PackageInstallWindow(Ui_package_install, QMainWindow, QueryFilePath):
    def __init__(self, parent: PackageManagerWindow, back):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.__setup_other_widgets()
        self.environment = None
        self.package_names = list()
        self.signal_slot_connection()
        self.__parent = parent
        self.__callback = back
        self.last_path = self.__parent.config.last_path

    def __setup_other_widgets(self):
        self.pte_package_names = TextEdit(ext_filter={".whl"})
        self.uiHorizontalLayout_package_name.replaceWidget(
            self.pte_package_names_old, self.pte_package_names
        )
        self.pte_package_names.show()
        self.pte_package_names_old.deleteLater()

    def display(self):
        self.resize(*self.__parent.config.install_winsize)
        self.showNormal()

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
        if text and fpath:
            self.__parent.config.last_path = fpath
            self.last_path = fpath
            self.pte_package_names.setPlainText(text)

    def config_dict_to_widgets(self):
        self.pte_package_names.setPlainText(
            "\n".join(self.__parent.config.package_names)
        )
        self.cb_including_pre.setChecked(self.__parent.config.include_pre)
        self.cb_install_for_user.setChecked(self.__parent.config.install_for_user)
        self.le_use_index_url.setText(self.__parent.config.index_url)
        self.cb_use_index_url.setChecked(self.__parent.config.use_index_url)
        if self.cb_use_index_url.isChecked():
            self.le_use_index_url.setEnabled(True)
        else:
            self.le_use_index_url.setEnabled(False)

    def config_widgets_to_dict(self):
        self.package_names.extend(
            s for s in self.pte_package_names.toPlainText().splitlines() if s
        )
        self.__parent.config.package_names = self.package_names.copy()
        self.__parent.config.include_pre = self.cb_including_pre.isChecked()
        self.__parent.config.install_for_user = self.cb_install_for_user.isChecked()
        self.__parent.config.index_url = self.le_use_index_url.text()
        self.__parent.config.use_index_url = self.cb_use_index_url.isChecked()

    def call_installpkg_back(self):
        self.close()  # 触发 closeEvent 更新配置
        self.__callback(self.environment, self.package_names)

    def set_target_environ(self, env):
        self.environment = env
        self.config_dict_to_widgets()
        self.uiLabel_target_environment.setText(str(env))
        self.display()

    def __save_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__parent.config.install_winsize = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        self.__save_window_size()
        self.config_widgets_to_dict()

    def signal_slot_connection(self):
        self.pb_do_install.clicked.connect(self.call_installpkg_back)
        self.pb_save_as_text.clicked.connect(self.save_package_names)
        self.pb_load_from_text.clicked.connect(self.load_package_names)
        self.cb_use_index_url.clicked.connect(self.set_le_use_index_url)

    def set_le_use_index_url(self):
        self.le_use_index_url.setEnabled(self.cb_use_index_url.isChecked())


class AddEnvironDialog(Ui_input_dialog, QMainWindow):
    def __init__(self, parent: PackageManagerWindow, back, title=""):
        self.__parent = parent
        super().__init__(parent)
        self.setupUi(self)
        self.initialize()
        if title:
            self.setWindowTitle(title)
        self.__callback = back
        self.last_path = parent.config.last_path
        self.display()

    def display(self):
        self.resize(*self.__parent.config.input_winsize)
        self.showNormal()

    def initialize(self):
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.uiPushButton_confirm.clicked.connect(self.__text_back)
        self.uiPushButton_select_envdir.clicked.connect(self.__select_envdir)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.__text_back()

    def __text_back(self):
        self.close()
        self.__callback(self.uiLineEdit_input_content.text())

    def __save_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__parent.config.input_winsize = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        self.__save_window_size()

    def __select_envdir(self):
        _path = QFileDialog.getExistingDirectory(self, "选择文件夹", self.last_path)
        if not _path:
            return
        interpreter_directory = path.normpath(_path)
        self.__parent.config.last_path = interpreter_directory
        self.uiLineEdit_input_content.setText(interpreter_directory)


class NameQueryPanel(Ui_query_panel, QMainWindow):
    signal_result = pyqtSignal(str)

    def __init__(self, parent: PackageManagerWindow):
        self.__parent = parent
        super().__init__(parent)
        self.setupUi(self)
        self.__initialize_widgets()
        self.__environ: Union[PyEnv, None] = None

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj == self.uiLineEdit_input_name:
            if event.type() == QEvent.FocusIn:
                QTimer.singleShot(10, self.uiLineEdit_input_name.selectAll)
            elif event.type() == QEvent.FocusOut:
                self.uiLineEdit_input_name.deselect()
        return super().eventFilter(obj, event)

    def display(self):
        self.resize(*self.__parent.config.query_winsize)
        self.showNormal()

    def __initialize_widgets(self):
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.uiLineEdit_input_name.installEventFilter(self)
        self.signal_result.connect(self.uiPlainTextEdit_query_result.appendPlainText)
        self.uiPushButton_query.clicked.connect(self.start_query_name)

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key == Qt.Key_Escape:
            self.close()
        elif key == Qt.Key_Enter or key == Qt.Key_Return:
            self.start_query_name()

    def __save_query_configure(self):
        self.__parent.config.query_name = self.uiLineEdit_input_name.text()
        if self.uiRadioButton_pkg2import.isChecked():
            self.__parent.config.query_mode = QMode.Pkg2Imp
        elif self.uiRadioButton_import2pkg.isChecked():
            self.__parent.config.query_mode = QMode.Imp2Pkg
        self.__parent.config.query_case = self.uiCheckBox_case_sensitive.isChecked()
        if self.isMaximized() or self.isMinimized():
            return
        self.__parent.config.query_winsize = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        self.__save_query_configure()

    def __start_querying(self):
        self.uiPushButton_query.setEnabled(False)
        self.uiRadioButton_pkg2import.setEnabled(False)
        self.uiRadioButton_import2pkg.setEnabled(False)
        self.uiLabel_query_result.setText("正在查询...")

    def __end_of_query(self):
        self.uiPushButton_query.setEnabled(True)
        self.uiRadioButton_pkg2import.setEnabled(True)
        self.uiRadioButton_import2pkg.setEnabled(True)
        self.uiLabel_query_result.setText("查询结果：")

    def start_query_name(self):
        name = self.uiLineEdit_input_name.text()
        if self.__environ is None:
            return MessageBox("提示", "没有选择任何 Python 环境。").exec_()
        if not name:
            return
        self.uiPlainTextEdit_query_result.clear()
        case = self.uiCheckBox_case_sensitive.isChecked()
        self.__start_querying()

        def do_query():
            if self.uiRadioButton_pkg2import.isChecked():
                result = self.__environ.query_for_import(name, case=case)
                for res in result:
                    self.signal_result.emit(res)
            elif self.uiRadioButton_import2pkg.isChecked():
                result = self.__environ.query_for_install(name, case=case)
                self.signal_result.emit(result)

        thread_query = QThreadModel(do_query)
        thread_query.at_finish(self.__end_of_query)
        thread_query.start()
        self.__parent.thread_repo.put(thread_query, 1)

    def initialize(self, env: PyEnv, name: str = None, mode=QMode.NotSPCF):
        assert isinstance(env, PyEnv)
        assert isinstance(name, str) or name is None
        assert isinstance(mode, QMode)
        self.__environ = env
        self.uiLabel_query_environ.setText(str(env))
        self.uiCheckBox_case_sensitive.setChecked(self.__parent.config.query_case)
        if name is None:
            name = self.__parent.config.query_name
        self.uiLineEdit_input_name.setText(name)
        if mode == QMode.NotSPCF:
            if self.__parent.config == QMode.NotSPCF:
                mode = QMode.Pkg2Imp
            else:
                mode = self.__parent.config.query_mode
        if mode == QMode.Pkg2Imp:
            self.uiRadioButton_pkg2import.setChecked(True)
        elif mode == QMode.Imp2Pkg:
            self.uiRadioButton_import2pkg.setChecked(True)

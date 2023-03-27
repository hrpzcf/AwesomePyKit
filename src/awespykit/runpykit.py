# coding: utf-8

__license__ = "GNU General Public License v3 (GPLv3)"

import sys
from functools import partial
from os import path

from fastpip import VERNUM
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

sys.path.append(path.dirname(__file__))  # rpk.exe 入口点所需

from __info__ import *
from com import *
from logic import *
from res.res import *
from settings import *
from ui import *
from utils.thmt import *

if VERNUM[0] != REQ_FPVER[0]:
    raise Exception(f"当前环境的 fastpip 主版本号({VERNUM[0]})非本程序要求：{REQ_FPVER[0]}")
if VERNUM[1] < REQ_FPVER[1]:
    raise Exception(f"当前环境的 fastpip 次版本号({VERNUM[1]})低于本程序要求：{REQ_FPVER[1]}")
elif VERNUM[1] == REQ_FPVER[1] and VERNUM[2] < REQ_FPVER[2]:
    raise Exception(f"当前环境的 fastpip 修订号({VERNUM[2]})低于本程序要求：{REQ_FPVER[2]}")
################################################################
# 版本号的定义：主版本号.次版本号.修订号，对 fastpip 的版本号要求：
# 1. 主版本号必须与要求一致，次版本号必须大于等于要求的次版本号
# 2. 如次版本号等于要求的次版本号，则修订号必须大于等于要求的修订号
################################################################

_IS_MAIN_MODULE = False


class MainEntrance(Ui_main_entrance, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint
        )
        self.__config = MainEntranceConfig()
        self.__themes: Themes[ThemeData] = PreThemeList
        self.setWindowTitle(APP_NAME)
        self.__about_window = AboutWindow(
            self, PRE_VER if _IS_MAIN_MODULE else VERSION
        )
        self.__pkgmgr_win = PackageManagerWindow(self)
        self.__pyitool_win = PyinstallerToolWindow(self)
        self.__indexmgr_win = IndexUrlManagerWindow(self)
        self.__pkgdl_win = PackageDownloadWindow(self)
        self.__cloudfunction_win = CloudFunctionWindow(self)
        self.__setup_other_widgets()
        self.__theme_action(self.__config.selected_thm)

    def display(self):
        self.resize(*self.__config.window_size)
        self.showNormal()

    def __store_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__config.window_size = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        if (
            self.__pkgmgr_win.thread_repo.is_empty()
            and self.__pyitool_win.thread_repo.is_empty()
            and self.__pkgdl_win.thread_repo.is_empty()
            and self.__cloudfunction_win.thread_repo.is_empty()
        ):
            event.accept()
        else:
            user_messagebox_role = MessageBox(
                "警告",
                "有后台任务正在运行，是否强制结束任务？",
                QMessageBox.Warning,
                (("accept", "强制退出"), ("reject", "取消")),
                self,
            ).exec_()
            if user_messagebox_role == 0:
                self.__pkgdl_win.thread_repo.kill_all()
                self.__pkgmgr_win.thread_repo.kill_all()
                self.__pyitool_win.thread_repo.kill_all()
                self.__cloudfunction_win.thread_repo.kill_all()
                event.accept()
            else:
                event.ignore()
        self.__store_window_size()
        self.__config.save_config()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

    def _show_about(self):
        self.__about_window.display()

    def __setup_other_widgets(self):
        self.uiPushButton_pkg_mgr.setIcon(QIcon(":/manage.png"))
        self.uiPushButton_pkg_mgr.clicked.connect(self.__pkgmgr_win.display)
        self.uiPushButton_pyi_tool.setIcon(QIcon(":/bundle.png"))
        self.uiPushButton_pyi_tool.clicked.connect(self.__pyitool_win.display)
        self.uiPushButton_index_mgr.setIcon(QIcon(":/indexurl2.png"))
        self.uiPushButton_index_mgr.clicked.connect(self.__indexmgr_win.display)
        self.uiPushButton_pkg_dload.setIcon(QIcon(":/download.png"))
        self.uiPushButton_pkg_dload.clicked.connect(self.__pkgdl_win.display)
        self.uiPushButton_cloudfunction.setIcon(QIcon(":/cloudfunction.png"))
        self.uiPushButton_cloudfunction.clicked.connect(
            self.__cloudfunction_win.display
        )
        self.uiPushButton_settings.setIcon(QIcon(":/settings.png"))
        # noinspection PyTypeChecker
        menu_setstyle = QMenu("主题", self)
        for theme in self.__themes:
            action = QAction(theme.name, self)
            action.triggered.connect(partial(self.__theme_action, theme.index))
            menu_setstyle.addAction(action)
        menu_main_settings = QMenu(self)
        menu_main_settings.setObjectName("settings_menu")
        menu_main_settings.addMenu(menu_setstyle)
        menu_main_settings.addAction("关于", self._show_about)
        self.uiPushButton_settings.setMenu(menu_main_settings)

    def __theme_action(self, index: int):
        self.__config.selected_thm = self.__themes.apply_theme(index)


def runpykit_and_sysexit():
    translator = QTranslator()
    translator.load(":/trans/widgets_zh-CN.qm")
    _App.installTranslator(translator)
    _App.setWindowIcon(QIcon(":/icon2_64.png"))
    main = MainEntrance()
    main.display()
    sys.exit(_App.exec_())


if __name__ == "__main__":
    _IS_MAIN_MODULE = True
    runpykit_and_sysexit()

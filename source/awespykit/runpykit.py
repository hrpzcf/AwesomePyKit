# coding: utf-8

__license__ = "GNU General Public License v3 (GPLv3)"

import sys
from functools import partial
from os import path
from typing import *

from fastpip import *
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
from utils.thmt import ThemeData, Themes

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

_awespykit: Union[QApplication, None] = None
_stylesheet = "*{font-size:12px;font-family:'Microsoft YaHei UI';}"


class MainEntrance(Ui_main_entrance, QMainWindow):
    def __init__(self, config: MainEntranceConfig):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint
        )
        self.setWindowTitle(NAME)
        self.__config = config
        self.__themes: List[ThemeData] = Themes()
        self.__pkgmgr_win = PackageManagerWindow(self)
        self.__pyitool_win = PyinstallerToolWindow(self)
        self.__indexmgr_win = IndexUrlManagerWindow(self)
        self.__pkgdl_win = PackageDownloadWindow(self)
        self.__setup_other_widgets()
        self.__theme_action(self.__config.selected_thm)

    def change_appstyle(self, style: AppStyle):
        self.__config.app_style = style
        MessageBox("提示", "界面风格设置成功，重启程序生效！").exec_()

    def display(self):
        self.resize(*self.__config.window_size)
        self.showNormal()

    def __theme_action(self, thm: Union[int, ThemeData]):
        if _awespykit is None:
            return
        if isinstance(thm, ThemeData):
            self.__config.selected_thm = thm.index
            if thm.index != -1:
                sheet = thm.sheet
            else:
                sheet = _stylesheet
            _awespykit.setStyleSheet(sheet)
        elif isinstance(thm, int):
            for theme in self.__themes:
                if theme.index == thm:
                    _awespykit.setStyleSheet(theme.sheet)
                    return
            _awespykit.setStyleSheet(_stylesheet)

    def __setup_other_widgets(self):
        self.uiPushButton_pkg_mgr.setIcon(QIcon(":/manage.png"))
        self.uiPushButton_pkg_mgr.clicked.connect(self.__pkgmgr_win.display)
        self.uiPushButton_pyi_tool.setIcon(QIcon(":/bundle.png"))
        self.uiPushButton_pyi_tool.clicked.connect(self.__pyitool_win.display)
        self.uiPushButton_index_mgr.setIcon(QIcon(":/indexurl2.png"))
        self.uiPushButton_index_mgr.clicked.connect(self.__indexmgr_win.display)
        self.uiPushButton_pkg_dload.setIcon(QIcon(":/download.png"))
        self.uiPushButton_pkg_dload.clicked.connect(self.__pkgdl_win.display)
        self.uiPushButton_settings.setIcon(QIcon(":/settings.png"))
        # noinspection PyTypeChecker
        menu_setstyle = QMenu("主题", self)
        native_style = QAction("原生风格", self)
        native_style.triggered.connect(
            partial(self.__theme_action, ThemeData())
        )
        menu_setstyle.addAction(native_style)
        for theme in self.__themes:
            action = QAction(theme.name, self)
            action.triggered.connect(partial(self.__theme_action, theme))
            menu_setstyle.addAction(action)
        menu_main_settings = QMenu(self)
        menu_main_settings.setObjectName("settings_menu")
        menu_main_settings.addMenu(menu_setstyle)
        menu_main_settings.addAction("关于", self._show_about)
        self.uiPushButton_settings.setMenu(menu_main_settings)

    def __store_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__config.window_size = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        if (
            self.__pkgmgr_win.thread_repo.is_empty()
            and self.__pyitool_win.thread_repo.is_empty()
            and self.__pkgdl_win.thread_repo.is_empty()
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
                self.__pkgdl_win.thread_repo.kill_all()
                self.__pkgmgr_win.thread_repo.kill_all()
                self.__pyitool_win.thread_repo.kill_all()
                event.accept()
            else:
                event.ignore()
        self.__store_window_size()
        self.__config.save_config()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

    @staticmethod
    def _show_about():
        about_path = generate_respath("help", "About.html")
        try:
            with open(about_path, encoding="utf-8") as h:
                info = h.read().replace("0.0.0", VERSION)
                icon = QMessageBox.Information
        except Exception:
            info = f"无法打开<关于>文件：{about_path}，文件已丢失或损坏。"
            icon = QMessageBox.Critical
        MessageBox("关于", info, icon).exec_()


def run_pykit_sysexit_when_close():
    global _awespykit
    _awespykit = QApplication(sys.argv)
    translator = QTranslator()
    translator.load(":/trans/widgets_zh-CN.qm")
    _awespykit.installTranslator(translator)
    config = MainEntranceConfig()
    _awespykit.setWindowIcon(QIcon(":/icon2_64.png"))
    _awespykit.setStyle(AppStyle(config.app_style).name)
    main_entrance = MainEntrance(config)
    main_entrance.display()
    sys.exit(_awespykit.exec_())


if __name__ == "__main__":
    run_pykit_sysexit_when_close()

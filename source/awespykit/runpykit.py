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

import sys
from os import path

from fastpip import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

sys.path.append(path.dirname(__file__))  # rpk.exe 入口点所需

from __info__ import *
from logic import *
from res.res import *
from settings import *
from ui import *

required_for_fastpip = (1, 0, 0)  # 对 fastpip 版本号的要求
if VERNUM[0] != required_for_fastpip[0]:
    raise Exception(
        f"当前环境的 fastpip 模块主版本号({VERNUM[0]})非本程序要求的主版本号({required_for_fastpip[0]})。"
    )
if VERNUM[1] < required_for_fastpip[1]:
    raise Exception(
        f"当前环境的 fastpip 模块次版本号({VERNUM[1]})低于本程序要求的次版本号({required_for_fastpip[1]})。"
    )
# 版本号：主版本号.次版本号.修订号
# 主版本号必须与要求一致，次版本号必须大于等于要求的次版本号，不限制修订号


class MainEntrance(Ui_main_entrance, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle(NAME)
        self.__pkgmgr_win = PackageManagerWindow(self)
        self.__pyitool_win = PyinstallerToolWindow(self)
        self.__indexmgr_win = IndexUrlManagerWindow(self)
        self.__pkgdl_win = PackageDownloadWindow(self)
        self.signal_slot_connection()

    def signal_slot_connection(self):
        self.action_about.triggered.connect(self.__show_about)
        self.pb_pkg_mgr.clicked.connect(self.__pkgmgr_win.display)
        self.pb_pyi_tool.clicked.connect(self.__pyitool_win.display)
        self.pb_index_mgr.clicked.connect(self.__indexmgr_win.display)
        self.pb_pkg_dload.clicked.connect(self.__pkgdl_win.display)

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
    awespykit = QApplication(sys.argv)
    awespykit.setStyle("fusion")
    awespykit.setWindowIcon(QIcon(":/icon.ico"))
    main_entrance_window = MainEntrance()
    main_entrance_window.show()
    sys.exit(awespykit.exec_())


if __name__ == "__main__":
    run_pykit_sysexit_when_close()

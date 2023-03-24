# coding: utf-8

from fastpip import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from settings import *
from ui import *
from utils import *

from .messagebox import MessageBox


class IndexUrlManagerWindow(Ui_index_manager, QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.__config = IndexManagerConfig()
        self.indexurls_model = QStandardItemModel()
        self.__setup_indexurl_table()
        self.signal_slot_connection()

    def __setup_indexurl_table(self):
        self.uiTableView_indexurls.setModel(self.indexurls_model)
        self.indexurls_model.setHorizontalHeaderLabels(("名称", "地址"))
        horiz_header = self.uiTableView_indexurls.horizontalHeader()
        horiz_header.setSectionResizeMode(0, QHeaderView.Interactive)
        horiz_header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.uiTableView_indexurls.verticalHeader().setVisible(False)
        for (index, (name, url)) in enumerate(self.__config.index_urls.items()):
            self.indexurls_model.setItem(index, 0, QStandardItem(name))
            self.indexurls_model.setItem(index, 1, QStandardItem(url))
        if self.indexurls_model.rowCount() > 0:
            self.uiTableView_indexurls.setCurrentIndex(
                self.indexurls_model.index(0, 1)
            )

    def display(self):
        # 首先 resize 为普通大小的窗口不可少，因为：
        # 如果用户关闭最大化状态窗口，我们希望再次打开窗口也是最大化
        # 但是如果再次打开窗口立即以最大化状态显示
        # 那么将缺一个普通大小状态的窗口的尺寸记录
        # 最大化状态窗口的还原按钮将无法把窗口还原为普通大小
        self.resize(*self.__config.window_size)
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()

    def __store_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__config.window_size = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        self.__store_window_size()
        self.__config.save_config()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

    def signal_slot_connection(self):
        self.uiPushButton_clear_edit.clicked.connect(self.__clear_line_edit)
        self.uiPushButton_save_url.clicked.connect(self.__save_index_urls)
        self.uiPushButton_delete_url.clicked.connect(self.__del_index_url)
        self.uiTableView_indexurls.clicked.connect(self.__set_url_line_edit)
        self.uiPushButton_set_index.clicked.connect(self.__set_global_index_url)
        self.uiPushButton_refresh_effective.clicked.connect(
            self.__display_effective_url
        )

    def __set_url_line_edit(self):
        model_index = self.uiTableView_indexurls.currentIndex()
        selected_row = model_index.row()
        if selected_row == -1:
            return
        selected_name = self.indexurls_model.item(selected_row)
        selected_url = self.indexurls_model.item(selected_row, 1)
        self.uiLineEdit_url_name.setText(selected_name.text())
        self.uiLineEdit_index_url.setText(selected_url.text())

    def __clear_line_edit(self):
        self.uiLineEdit_url_name.clear()
        self.uiLineEdit_index_url.clear()

    def __check_name_url(self, name, url):
        def error(m):
            return MessageBox("错误", m, QMessageBox.Critical)

        if not name:
            msgbox = error("名称不能为空！")
        elif not url:
            msgbox = error("地址不能为空！")
        elif name in self.__config.index_urls:
            msgbox = error(f"名称 '{name}' 已存在！")
        elif not check_index_url(url):
            msgbox = error("无效的镜像源地址！")
        else:
            return True
        return msgbox.exec_()  # 无论如何都返回 0

    def __save_index_urls(self):
        name = self.uiLineEdit_url_name.text()
        url = self.uiLineEdit_index_url.text()
        if self.__check_name_url(name, url):
            self.__config.index_urls[name] = url
            self.indexurls_model.appendRow(
                (QStandardItem(name), QStandardItem(url))
            )

    def __del_index_url(self):
        model_index = self.uiTableView_indexurls.currentIndex()
        selected_row_index = model_index.row()
        if selected_row_index == -1:
            return MessageBox(
                "提示",
                "没有选中列表内的任何条目。",
            ).exec_()
        item_data = self.indexurls_model.item(selected_row_index)
        indexurl_name = item_data.text()
        assert bool(indexurl_name), "镜像源名称混入空字符或奇怪的东西"
        assert indexurl_name in self.__config.index_urls, "镜像源字典没这名称"
        del self.__config.index_urls[indexurl_name]
        self.indexurls_model.removeRow(selected_row_index)
        table_rowcount = self.indexurls_model.rowCount()
        if not table_rowcount:
            return
        if selected_row_index == -1:
            will_be_selected = self.indexurls_model.index(0, 0)
        else:
            will_be_selected = (
                self.indexurls_model.index(selected_row_index, 0)
                if selected_row_index < table_rowcount
                else self.indexurls_model.index(table_rowcount - 1, 0)
            )
        self.uiTableView_indexurls.setCurrentIndex(will_be_selected)

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

        url = self.uiLineEdit_index_url.text()
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
            self.uiLineEdit_effective_url.setText("没找到 Python 环境，无法获取镜像源地址。")
            return
        self.uiLineEdit_effective_url.setText(
            environ.get_global_index() or "无效的 Python 环境或当前全局镜像源地址为空。"
        )

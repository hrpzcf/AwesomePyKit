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
        self.__ordered_urls = None
        self.signal_slot_connection()

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
        self.__list_widget_urls_update()

    def __store_window_size(self):
        if self.isMaximized() or self.isMinimized():
            return
        self.__config.window_size = self.width(), self.height()

    def closeEvent(self, event: QResizeEvent):
        self.__store_window_size()
        self.__config.save_config()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

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

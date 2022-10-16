# coding: utf-8

import os

from chardet import detect
from PyQt5.QtWidgets import *

from .messagebox import MessageBox


class QueryFilePath(QWidget):
    def load_from_text(self, last_path):
        text_file_path, _ = QFileDialog.getOpenFileName(
            self, "选择文本文件", last_path, "文本文件 (*.txt)"
        )
        if not text_file_path:
            return "", ""
        try:
            with open(text_file_path, "rb") as f:
                encoding = detect(f.read()).get("encoding", "utf-8")
            with open(text_file_path, "rt", encoding=encoding) as obj:
                return obj.read(), os.path.dirname(text_file_path)
        except Exception as reason:
            MessageBox(
                "错误",
                f"文件打开失败：\n{str(reason)}",
                QMessageBox.Critical,
            ).exec_()
            return "", ""

    def save_as_text_file(self, data, last_path):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "保存文件", last_path, "文本文件 (*.txt)"
        )
        if not save_path:
            return ""
        try:
            with open(save_path, "wt", encoding="utf-8") as fobj:
                fobj.writelines(data)
        except Exception as reason:
            return MessageBox(
                "错误", f"文件保存失败：\n{str(reason)}", QMessageBox.Critical
            ).exec_()
        return os.path.dirname(save_path)

    def get_dir_path(self, last_path):
        _path = QFileDialog.getExistingDirectory(self, "选择目录", last_path)
        if _path:
            return os.path.normpath(_path)
        return ""

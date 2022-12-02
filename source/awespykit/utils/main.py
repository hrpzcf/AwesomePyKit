# coding: utf-8

__doc__ = """包含AwesomePyKit的主要类、函数、配置文件路径等。"""

import os.path as osp
import re
from subprocess import *
from typing import *
from typing import Match

import win32api
from fastpip import PyEnv
from PyQt5.QtCore import *
# noinspection PyUnresolvedReferences
from win32com.shell import shell


def loop_install(
    pyenv, sequence, *, index_url="", pre=False, user=False, upgrade=False
):
    for name in sequence:
        cmd_exec_result = pyenv.install(
            name,
            pre=pre,
            user=user,
            index_url=index_url,
            upgrade=upgrade,
        )
        yield cmd_exec_result[0][0], cmd_exec_result[1]


def loop_uninstall(pyenv, sequence):
    for name in sequence:
        cmd_exec_result = pyenv.uninstall(name)
        yield cmd_exec_result[0][0], cmd_exec_result[1]


def check_py_path(py_dir_path):
    return PyEnv(py_dir_path).env_path != ""


def clean_py_paths(paths):
    return [pth for pth in paths if check_py_path(pth)]


def check_index_url(url):
    return bool(re.match(r"^https://.+/simple/?$", url.lower()))


def clean_index_urls(urls):
    return [url for url in urls if check_index_url(url)]


class QThreadModel(QThread):
    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self.__target = target
        self.__args = args
        self.__kwargs = kwargs
        self.__at_start = list()
        self.__at_finish = list()

    def run(self):
        self.__target(*self.__args, **self.__kwargs)

    def __repr__(self):
        return f"{self.__target} with args: {self.__args}, kwargs: {self.__kwargs}"

    __str__ = __repr__

    def before_starting(self, *callable_objs):
        for cab in callable_objs:
            self.started.connect(cab)
        self.__at_start.extend(callable_objs)

    def after_completion(self, *callable_objs):
        for cab in callable_objs:
            self.finished.connect(cab)
        self.__at_finish.extend(callable_objs)

    def broken_signal(self):
        for cab in self.__at_start:
            self.started.disconnect(cab)
        for cab in self.__at_finish:
            self.finished.disconnect(cab)


class ThreadRepo:
    def __init__(self, interval):
        """interval: 清理已结束线程的时间间隔，单位毫秒。"""
        self._thread_repo = []
        self._timer_clths = QTimer()
        self._mutex = QMutex()
        self._timer_clths.timeout.connect(self.clean)
        self._timer_clths.start(interval)
        self._flag_cleaning = False

    def put(self, threadhandle, level=0):
        """将(线程句柄、重要等级)元组加入线程仓库。"""
        self._mutex.lock()
        self._thread_repo.append((threadhandle, level))
        self._mutex.unlock()

    def clean(self):
        """清除已结束的线程。"""
        if self._flag_cleaning:
            return
        self._mutex.lock()
        index = 0
        self._flag_cleaning = True
        while index < len(self._thread_repo):
            if self._thread_repo[index][0].isRunning():
                index += 1
                continue
            del self._thread_repo[index]
        self._flag_cleaning = False
        self._mutex.unlock()

    def stop_all(self):
        """
        按线程重要等级退出线程。
        0级：重要，安全退出；
        1级：不重要，立即退出；
        其他：未知等级，安全退出。
        """
        for thread, level in self._thread_repo:
            thread.broken_signal()
            if level == 0:
                thread.quit()
            elif level == 1:
                thread.terminate()
            else:
                thread.quit()

    def kill_all(self):
        """立即终止所有线程。"""
        for thread, _ in self._thread_repo:
            thread.broken_signal()
            thread.terminate()

    def is_empty(self):
        """返回线程仓库是否为空。"""
        return not self._thread_repo


def get_cmd_out(
    *commands, re_search=None, timeout=None
) -> Union[str, Match[str], None]:
    """用于从cmd命令执行输出的字符匹配想要的信息。"""
    info = STARTUPINFO()
    info.dwFlags = STARTF_USESHOWWINDOW
    info.wShowWindow = SW_HIDE
    proc = Popen(commands, stdout=PIPE, text=True, startupinfo=info)
    try:
        strings, _ = proc.communicate(timeout=timeout)
    except Exception:
        return ""
    if not re_search:
        return strings.strip()
    return re.search(re_search, strings)


def launch_explorer(folder_path: str, file_names: List[str] = None):
    """使用资源管理器打开文件夹并选择文件名列表中的文件"""
    assert isinstance(folder_path, str)
    assert osp.isdir(folder_path)
    assert file_names is None or all(isinstance(s, str) for s in file_names)
    if file_names is None:
        win32api.ShellExecute(0, "open", folder_path, None, None, 1)
        return
    folder_pidl = shell.SHILCreateFromPath(folder_path, 0)[0]
    files_tobe_selected = list()
    for file_name in file_names:
        file_fullpath = osp.join(folder_path, file_name)
        if not osp.isfile(file_fullpath):
            continue
        try:
            file_id = shell.SHParseDisplayName(file_fullpath, 0)[0]
            files_tobe_selected.append(file_id)
        except Exception:
            continue
    if not files_tobe_selected:
        return
    shell.SHOpenFolderAndSelectItems(folder_pidl, files_tobe_selected, 0)

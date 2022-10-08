# coding: utf-8

__doc__ = """包含AwesomePyKit的主要类、函数、配置文件路径等。"""

import json
import os
import os.path as op
import re
import subprocess
import sys
from subprocess import PIPE, STARTF_USESHOWWINDOW, STARTUPINFO, SW_HIDE, Popen

from fastpip import PyEnv, index_urls
from PyQt5.QtCore import QMutex, QThread, QTimer

_program_runs_in_bundle_mode = getattr(sys, "frozen", False)
if _program_runs_in_bundle_mode:
    _res_root = sys._MEIPASS
else:
    _res_root = op.dirname(op.dirname(op.abspath(__file__)))
_appdata_local_folder = os.getenv("LOCALAPPDATA")
if not _appdata_local_folder:
    if _program_runs_in_bundle_mode:
        config_root = op.dirname(sys.executable)
    else:
        config_root = _res_root
else:
    config_root = op.join(_appdata_local_folder, "Awespykit")
config_root = op.join(config_root, "config")

config_indexurl_manager = op.join(config_root, "indexurls_manager.json")
config_pyinstaller_tool = op.join(config_root, "pyinstaller_tool.json")
config_package_install = op.join(config_root, "package_install.json")
config_package_download = op.join(config_root, "package_download.json")


def get_res_path(*p):
    """
    用于在不同运行环境之下获取正确的资源文件路径

    不同的运行环境：Python 源代码运行、Pyinstaller 打包为单文件运行/打包为单目录运行
    """
    return op.join(_res_root, *p)


def _load_json(json_path, get_data):
    """
    如果 json_path 文件不存在或无法读取，则调用 get_data 函数取值并返回该值
    """
    if not op.exists(json_path):
        data = get_data()
        try:
            with open(json_path, "wt", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception:
            pass
        return data
    try:
        with open(json_path, "rt", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return get_data()


class Option:
    """枚举，用于 load_config 和 save_config 函数的 option 参数"""

    PKG_INSTALL = 0  # 包管理器“安装”界面设置
    PKG_MANAGER = 1  # 包管理器的环境路径列表
    PYINSTALLER = 2  # 程序打包工具设置
    INDEX_MANAGER = 3  # 镜像源设置工具保存的地址
    PKG_DOWNLOAD = 4  # 模块下载器的设置


def load_config(option):
    if not op.exists(config_root):
        os.makedirs(config_root)
    if option == Option.PKG_INSTALL:
        return _load_json(config_package_install, dict)
    if option == Option.PYINSTALLER:
        return _load_json(config_pyinstaller_tool, list)
    if option == Option.INDEX_MANAGER:
        return _load_json(config_indexurl_manager, index_urls.copy)
    if option == Option.PKG_DOWNLOAD:
        return _load_json(config_package_download, dict)
    assert False, f"选项错误：{option}"


def save_config(sequence, option):
    if option == Option.PKG_INSTALL:
        pth = config_package_install
    elif option == Option.PYINSTALLER:
        pth = config_pyinstaller_tool
    elif option == Option.INDEX_MANAGER:
        pth = config_indexurl_manager
    elif option == Option.PKG_DOWNLOAD:
        pth = config_package_download
    else:
        raise Exception(f"选项错误：{option}")
    try:
        with open(pth, "wt", encoding="utf-8") as f:
            json.dump(sequence, f, indent=4, ensure_ascii=False)
    except Exception:
        pass


def get_pyenv_list(paths=None):
    if not paths:
        paths = load_config(Option.PKG_MANAGER)
    return [PyEnv(p) for p in paths]


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
    return bool(re.match(r"^https://.+/simple[/]?$", url.lower()))


def clean_index_urls(urls):
    return [url for url in urls if check_index_url(url)]


class QThreadModel(QThread):
    def __init__(self, target, args=tuple()):
        super().__init__()
        self._args = args
        self._target = target
        self._at_start = list()
        self._at_finish = list()

    def run(self):
        self._target(*self._args)

    def __repr__(self):
        return f"{self._target} with args:{self._args}"

    __str__ = __repr__

    def at_start(self, *callable_objs):
        for cab in callable_objs:
            self.started.connect(cab)
        self._at_start.extend(callable_objs)

    def at_finish(self, *callable_objs):
        for cab in callable_objs:
            self.finished.connect(cab)
        self._at_finish.extend(callable_objs)

    def broken_signal(self):
        for cab in self._at_start:
            self.started.disconnect(cab)
        for cab in self._at_finish:
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


def get_cmd_out(*commands, regexp="", timeout=None):
    """用于从cmd命令执行输出的字符匹配想要的信息。"""
    info = STARTUPINFO()
    info.dwFlags = STARTF_USESHOWWINDOW
    info.wShowWindow = SW_HIDE
    proc = Popen(commands, stdout=PIPE, text=True, startupinfo=info)
    try:
        strings, _ = proc.communicate(timeout=timeout)
    except Exception:
        return ""
    if not regexp:
        return strings.strip()
    return re.search(regexp, strings)


def open_explorer(fd_path, option="root"):
    assert isinstance(fd_path, str)
    assert option in ("root", "select")
    fd_path = op.normpath(fd_path.strip())
    if op.isfile(fd_path):
        commands = f"explorer /select,{fd_path}"
    elif op.isdir(fd_path):
        commands = f"explorer /{option},{fd_path}"
    else:
        return
    subprocess.run(commands)

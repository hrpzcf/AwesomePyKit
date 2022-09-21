# coding: utf-8

__doc__ = """包含AwesomePyKit的主要类、函数、配置文件路径等。"""

import json
import os
import re
import subprocess
from subprocess import PIPE, STARTF_USESHOWWINDOW, STARTUPINFO, SW_HIDE, Popen

from fastpip import PyEnv, all_py_paths, cur_py_path, index_urls
from fastpip.errors import *
from PyQt5.QtCore import QMutex, QThread, QTimer

# 此程序打包为单目录形式时，__file__ 是 libm.pyc 文件的虚拟路径
# 路径在程序可执行文件的目录下：.\library\libm.pyc，文件不是真实存在的
_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_dir = os.path.join(_root_path, "config")
resources_dir = os.path.join(_root_path, "res")
config_file_py_paths = os.path.join(config_dir, "PythonPaths.json")
config_file_index_urls = os.path.join(config_dir, "IndexURLs.json")
config_file_pyi_defs = os.path.join(config_dir, "PyiDefault.json")
config_file_install_package = os.path.join(config_dir, "InstallPackage.json")
config_file_dload_package = os.path.join(config_dir, "DloadPackage.json")


def _load_json(path, get_data):
    """
    如果 path 文件不存在，则调用 get_data 获取数据创建配置并返回

    如果无法读取 path 配置文件，则调用 get_data 函数取值并返回该值
    """
    if not os.path.exists(path):
        data = get_data()
        try:
            with open(path, "wt", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception:
            pass
        return data
    try:
        with open(path, "rt", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return get_data()


def load_conf(option):
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    elif os.path.isfile(config_dir):
        os.remove(config_dir)
        os.makedirs(config_dir)
    # 加载包管理器安装界面设置字典
    if option == "insp":
        return _load_json(config_file_install_package, dict)
    # 加载已保存的环境路径列表
    if option == "pths":
        return _load_json(config_file_py_paths, list)
    # 加载程序打包工具设置字典
    if option == "pyic":
        return _load_json(config_file_pyi_defs, dict)
    # 加载镜像源地址字典
    if option == "urls":
        return _load_json(config_file_index_urls, index_urls.copy)
    # 加载模块下载器设置字典
    if option == "dlpc":
        return _load_json(config_file_dload_package, dict)
    raise Exception(f"没有此选项：{option}")


def save_conf(sequence, option):
    if option == "pths":
        pth = config_file_py_paths
    elif option == "urls":
        pth = config_file_index_urls
    elif option == "pyic":
        pth = config_file_pyi_defs
    elif option == "insp":
        pth = config_file_install_package
    elif option == "dlpc":
        pth = config_file_dload_package
    else:
        return
    try:
        with open(pth, "wt", encoding="utf-8") as f:
            json.dump(sequence, f, indent=4, ensure_ascii=False)
    except Exception:
        pass


def get_pyenv_list(paths=None):
    if not paths:
        paths = load_conf("pths")
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


class NewTask(QThread):
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


def open_explorer(path, option="root"):
    assert isinstance(path, str)
    assert option in ("root", "select")
    path = os.path.normpath(path.strip())
    if os.path.isfile(path):
        commands = f"explorer /select,{path}"
    elif os.path.isdir(path):
        commands = f"explorer /{option},{path}"
    else:
        return
    subprocess.run(commands)

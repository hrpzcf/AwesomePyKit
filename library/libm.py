# coding: utf-8

__doc__ = '''包含AwesomePyKit的主要类、函数、配置文件路径等。'''

import json
import os
import re
from subprocess import (
    PIPE,
    STARTF_USESHOWWINDOW,
    STARTUPINFO,
    SW_HIDE,
    Popen,
    TimeoutExpired,
)

from fastpip import PyEnv, all_py_paths, cur_py_path, index_urls
from fastpip.errors import *
from PyQt5.QtCore import QMutex, QThread, QTimer

_STARTUP = STARTUPINFO()
_STARTUP.dwFlags = STARTF_USESHOWWINDOW
_STARTUP.wShowWindow = SW_HIDE

_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
conf_path = os.path.join(_root_path, 'config')
sources_path = os.path.join(_root_path, 'sources')
conf_path_py_paths = os.path.join(conf_path, 'PythonPaths.json')
conf_path_index_urls = os.path.join(conf_path, 'IndexURLs.json')
conf_path_pyi_defs = os.path.join(conf_path, 'PyiDefault.json')


def _load_json(path, get_data):
    '''
    读取 json 配置文件的函数。
    如果 path 路径的配置文件不存在，则调用 get_data 函数取默认值并创建配置。
    如果无法读取 path 配置文件，则调用 get_data 函数取值并返回该值。
    :param path: str, json 文件完整路径。
    :param get_data: callable, 返回值是列表或字典的可调用对象。
    :return: list or dict, 从 json 文件读取的列表或字典或 get_data 函数的返回值。
    '''
    if not os.path.exists(path):
        data = get_data()
        try:
            with open(path, 'wt', encoding='utf-8') as fo:
                json.dump(data, fo, indent=4, ensure_ascii=False)
        except Exception:
            pass
        return data
    try:
        with open(path, 'rt', encoding='utf-8') as fo:
            return json.load(fo)
    except Exception:
        return get_data()


def load_conf(conf='all'):
    '''
    调用 _load_json 函数从 json 文件读取 Python 目录路径列表、镜像源地址字典。
    :return: tuple[list, dict], (Python路径列表, 镜像源地址字典)元组。
    '''
    if not os.path.exists(conf_path):
        os.mkdir(conf_path)
    if os.path.isfile(conf_path):
        os.remove(conf_path)
        os.mkdir(conf_path)
    if conf == 'pths':
        return _load_json(conf_path_py_paths, list)
    if conf == 'urls':
        return _load_json(conf_path_index_urls, index_urls.copy)
    if conf == 'pyic':
        return _load_json(conf_path_pyi_defs, dict)
    return (
        _load_json(conf_path_py_paths, list),
        _load_json(conf_path_index_urls, index_urls.copy),
        _load_json(conf_path_pyi_defs, dict),
    )


def save_conf(sequence, conf):
    if conf == 'pths':
        pth = conf_path_py_paths
    elif conf == 'urls':
        pth = conf_path_index_urls
    elif conf == 'pyic':
        pth = conf_path_pyi_defs
    else:
        return
    with open(pth, 'wt', encoding='utf-8') as fo:
        json.dump(sequence, fo, indent=4, ensure_ascii=False)


def get_cur_pyenv():
    return PyEnv()


def get_pyenv_list(py_dir_paths=None):
    '''返回 PyEnv 实例列表。'''
    if not py_dir_paths:
        py_dir_paths = load_conf('pths')
    py_env_list = []
    for py_dir_path in py_dir_paths:
        try:
            py_env_list.append(PyEnv(py_dir_path))
        except Exception:
            continue
    return py_env_list


def loop_install(pyenv, sequence, *, index_url='', upgrade=False):
    '''循环历遍包名列表 sequence 每一个包名 name，根据包名调用 pyenv.install 安装。'''
    for name in sequence:
        exit_status = pyenv.install(name, index_url=index_url, upgrade=upgrade)
        yield exit_status[0][0], exit_status[1]


def loop_uninstall(pyenv, sequence):
    '''循环历遍包名列表 sequence 每一个包名 name，根据包名调用 pyenv.uninstall 卸载。'''
    for name in sequence:
        exit_status = pyenv.uninstall(name)
        yield exit_status[0][0], exit_status[1]


def multi_install(pyenv, sequence, *, index_url='', upgrade=False):
    '''
    一次安装包名列表 sequence 中所有的包。
    注意：如果 sequence 中有一个包不可安装（没有匹配的包等原因），那sequence中所有的
    包都不会被安装，所以不是必须的情况下尽量不用这个函数来安装。
    '''
    return pyenv.install(*sequence, index_url=index_url, upgrade=upgrade)


def multi_uninstall(pyenv, sequence):
    '''
    一次卸载包名列表 sequence 中所有的包。
    注意：未安装的包则跳过卸载。
    '''
    return pyenv.uninstall(*sequence)


def set_index_url(pyenv, index_url):
    return pyenv.set_global_index(index_url)


def get_index_url(pyenv):
    return pyenv.get_global_index()


def check_py_path(py_dir_path):
    return os.path.isfile(os.path.join(py_dir_path, 'python.exe'))


def clean_py_paths(paths):
    return [pth for pth in paths if check_py_path(pth)]


def check_index_url(url):
    return bool(re.match(r'^https://.+/simple[/]?$', url.lower()))


def clean_index_urls(urls):
    return [url for url in urls if check_index_url(url)]


class InfoOutStream:
    INFO_TYPE = ('常规', '成功', '失败')

    def __init__(self, interface, limit=50):
        self._ui = interface
        self._limit = limit
        self._filter = list(self.INFO_TYPE)
        self._num = 0
        self._count = 0
        self._info = {'常规': [], '成功': [], '失败': []}

    def _del_info(self):
        if self._count > self._limit:
            name_max = max(self._info, key=lambda x: len(self._info[x]))
            del self._info[name_max][0]
            self._count -= 1

    def set_filter(self, *modes):
        if not all(it in self.INFO_TYPE for it in modes):
            raise ValueError(f'信息筛选模式"{modes}"无效。')
        self._filter.clear()
        self._filter.extend(modes)

    def write(self, info, inf_tp):
        if inf_tp not in self.INFO_TYPE:
            raise ValueError(f'信息分类方式"{inf_tp}"无效。')
        self._info[inf_tp].append((self._num, inf_tp, info))
        self._num += 1
        self._count += 1
        self._del_info()
        self.update(self._mk_text())

    def _mk_text(self):
        info = [self._info[x] for x in self._filter]
        info.sort(key=lambda item: item[0])
        for ind, val in enumerate(info):
            info[ind] = f'{val[1]}：{val[2]}...'
        return '\n'.join(info)

    def update(self, text):
        self._ui.te_infostream.setText(text)
        self._ui.te_infostream.verticalScrollBar().setValue(
            self._ui.te_infostream.verticalScrollBar().maximumHeight()
        )


class NewTask(QThread):
    def __init__(self, target, args=tuple()):
        super().__init__()
        self._args = args
        self._target = target

    def run(self):
        self._target(*self._args)

    def __repr__(self):
        return f'{self._target} with args:{self._args}'

    __str__ = __repr__


class ThreadRepo:
    def __init__(self, interval):
        '''interval: 清理已结束线程的时间间隔，单位毫秒。'''
        self._thread_repo = []
        self._timer_clths = QTimer()
        self._mutex = QMutex()
        self._timer_clths.timeout.connect(self.clean)
        self._timer_clths.start(interval)
        self._flag_cleaning = False

    def put(self, threadhandle, level=0):
        '''将(线程句柄、重要等级)元组加入线程仓库。'''
        self._mutex.lock()
        self._thread_repo.append((threadhandle, level))
        self._mutex.unlock()

    def clean(self):
        '''清除已结束的线程。'''
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
        '''
        按线程重要等级退出线程。
        0级：重要，安全退出；
        1级：不重要，立即退出；
        其他：未知等级，安全退出。
        '''
        for thread, level in self._thread_repo:
            if level == 0:
                thread.quit()
            elif level == 1:
                thread.terminate()
            else:
                thread.exit()

    def is_empty(self):
        '''返回线程仓库是否为空。'''
        return not self._thread_repo


def get_cmd_o(*commands, regexp='', timeout=None):
    ''' 用于从cmd命令执行输出的字符匹配想要的信息。'''
    exec_f = Popen(commands, stdout=PIPE, text=True, startupinfo=_STARTUP)
    try:
        strings, _ = exec_f.communicate(timeout=timeout)
    except TimeoutExpired:
        return ''
    if not regexp:
        return strings
    return re.search(regexp, strings)

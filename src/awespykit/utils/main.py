# coding: utf-8

__doc__ = """包含AwesomePyKit的主要类、函数、配置文件路径等。"""

import os.path as osp
import re
from subprocess import *
from typing import *
from typing import Match

import win32api
from fastpip import PyEnv

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

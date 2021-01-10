# coding: utf-8

__doc__ = '''包含pyinstaller相关的类或函数。'''

import os
from subprocess import (
    PIPE,
    STARTF_USESHOWWINDOW,
    STARTUPINFO,
    STDOUT,
    SW_HIDE,
    Popen,
)

from PyQt5.QtCore import QObject, pyqtSignal

from library.libm import get_cmd_o


class PyiTool(QObject):
    _STARTUP = STARTUPINFO()
    _STARTUP.dwFlags = STARTF_USESHOWWINDOW
    _STARTUP.wShowWindow = SW_HIDE
    executed = pyqtSignal(int)
    readline = pyqtSignal(str)

    def __init__(self, py_path='', cwd=os.getcwd()):
        super().__init__()
        self.initialize(py_path, cwd)

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self, path):
        if os.path.isdir(path):
            self._cwd = path

    @staticmethod
    def _check(py_path):
        ''' 检查给出的Python路径是否有效。'''
        return os.path.isfile(os.path.join(py_path, 'python.exe'))

    @property
    def pyi_path(self):
        ''' 返回给出的Python路径中的pyinstaller可执行文件路径。'''
        pyi_exec_path = os.path.join(
            self._py_path, 'Scripts', 'pyinstaller.exe'
        )
        if not os.path.isfile(pyi_exec_path):
            return ''
        return pyi_exec_path

    @property
    def pyi_ready(self):
        ''' 给出的Python目录中安装了pyinstaller返回True,否则返回False。'''
        return bool(self.pyi_path)

    def initialize(self, py_path, cwd):
        if self._check(py_path):
            self._py_path = py_path
        else:
            self._py_path = ''
        self._cwd = cwd
        self._execf = None
        self._commands = [self.pyi_path]

    def handle(self):
        if self._execf is None:
            self._execf = Popen(
                self._commands,
                stdin=PIPE,
                stdout=PIPE,
                stderr=STDOUT,
                text=True,
                cwd=self._cwd,
                startupinfo=self._STARTUP,
            )
        return self._execf

    def execute_cmd(self):
        if self.pyi_ready and self._execf:
            while self._execf.poll() is None:
                line = self._execf.stdout.readline()
                if not line or line == '\n':
                    continue
                self.readline.emit(line.strip())
            else:
                self.executed.emit(self._execf.returncode)
        else:
            if not self.pyi_ready:
                raise Exception('当前Python环境中找不到PyInstaller。')
            if self._execf is None:
                raise Exception('请先调用get_handle方法获取文件操作句柄。')
            raise Exception('未知错误。')

    def prepare_cmd(self, cmd_dict={}):
        ''' 从cmd_dict添加PyInstaller命令选项。'''
        if cmd_dict.get('pack_to_one', 'dir') == 'dir':
            self._commands.append('-D')
        else:
            self._commands.append('-F')
        if spec_path := cmd_dict.get('spec_dir', ''):
            self._commands.extend(('--specpath', spec_path))
        if name := cmd_dict.get('exefile_specfile_name', ''):
            self._commands.extend(('-n', name))
        if datas_to_add := cmd_dict.get('other_data', None):
            for data in datas_to_add:
                self._commands.extend(
                    ('--add-data', fr'{data[0]};{data[1]}')
                )
        if module_search_paths := cmd_dict.get('module_search_path', None):
            for module_path in module_search_paths:
                self._commands.extend(('-p', module_path))
        if key := cmd_dict.get('key', ''):
            self._commands.extend(('--key', key))
        if not cmd_dict.get('use_upx', False):
            self._commands.append('--noupx')
        if upx_excludes := cmd_dict.get('upx_exclude_files', None):
            for exfile in upx_excludes:
                self._commands.extend(('--upx-exclude', exfile))
        if cmd_dict.get('execute_with_console', True):
            self._commands.append('-c')
        else:
            self._commands.append('-w')
        if ico_path := cmd_dict.get('file_icon_path', ''):
            self._commands.extend(('-i', ico_path))
        if ver_file := cmd_dict.get('version_file', ''):
            self._commands.extend(('--version-file', ver_file))
        if dist_path := cmd_dict.get('output_dir', ''):
            self._commands.extend(('--distpath', dist_path))
        if work_path := cmd_dict.get('temp_working_dir', ''):
            self._commands.extend(('--workpath', work_path))
        if cmd_dict.get('without_confirm', False):
            self._commands.append('-y')
        if upx_dir := cmd_dict.get('upx_search_path', ''):
            self._commands.extend(('--upx-dir', upx_dir))
        if cmd_dict.get('clean_before_build', False):
            self._commands.append('--clean')
        self._commands.extend(
            ('--log-level', cmd_dict.get('log_level', 'INFO'))
        )
        self._commands.append(cmd_dict.get('program_entry', ''))

    def pyi_info(self):
        if self.pyi_ready:
            return get_cmd_o(self.pyi_path, '-v')
        return '0.0.0'

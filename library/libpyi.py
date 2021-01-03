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

from library.libm import get_cmd_o


class PyiTool:
    _stui = STARTUPINFO()
    _stui.dwFlags = STARTF_USESHOWWINDOW
    _stui.wShowWindow = SW_HIDE

    def __init__(self, py_path, cwd=os.getcwd()):
        if self._check_path(py_path):
            self.py_path = py_path
        else:
            self.py_path = ''
        self._execf = None
        self._cwd = cwd
        self._commands = [self.pyi_path]

    def __setattr__(self, name, value):
        if name == 'py_path':
            if not getattr(self, 'py_path', False):
                if PyiTool._check_path(value):
                    super().__setattr__(name, value)
                else:
                    print('无效的Python环境路径。')
            else:
                print('py_path属性不可更改。')
        else:
            super().__setattr__(name, value)

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self, path):
        if os.path.isdir(path):
            self._cwd = path

    @staticmethod
    def _check_path(py_path):
        ''' 检查给出的Python路径是否有效。'''
        f_py_path = os.path.join(py_path, 'python.exe')
        if os.path.isfile(f_py_path):
            return True
        return False

    @property
    def pyi_path(self):
        ''' 返回给出的Python路径中的pyinstaller可执行文件路径。'''
        pyi_exec_path = os.path.join(
            self.py_path, 'Scripts', 'pyinstaller.exe'
        )
        if not os.path.isfile(pyi_exec_path):
            return ''
        return pyi_exec_path

    @property
    def pyi_ready(self):
        ''' 给出的Python目录中安装了pyinstaller返回True,否则返回False。'''
        return bool(self.pyi_path)

    def get_handle(self):
        if self._execf is None:
            self._execf = Popen(
                self._commands,
                stdin=PIPE,
                stdout=PIPE,
                stderr=STDOUT,
                text=True,
                cwd=self._cwd,
                startupinfo=self._stui,
            )
        return self._execf

    def stream(self):
        '''
        如果程序执行中，返回("out", 命令执行的输出信息)元组。
        如果程序已结束，则返回("rtc", 程序的退出状态码)元组。
        '''
        if self.pyi_ready and self._execf is not None:
            while self._execf.poll() is None:
                yield 'out', self._execf.stdout.readline()
            else:
                yield 'rtc', self._execf.returncode
        else:
            if not self.pyi_ready:
                # 如果该Python环境未安装pyinstaller则返回以下信息。
                yield 'err', '当前Python环境中找不到PyInstaller。'
            elif self._execf is None:
                # 如果还未生成Popen对象则返回以下信息。
                yield 'err', '请先调用get_handle方法获取操作句柄。'

    def add_command(self, cmd_dict={}):
        ''' 从cmd_dict添加PyInstaller命令选项。'''
        if cmd_dict.get('pack_to_one', 'dir') == 'dir':
            self._commands.append('-D')
        else:
            self._commands.append('-F')
        if spec_path := cmd_dict.get('spec_dir', ''):
            self._commands.extend(('--specpath', spec_path))
        if name := cmd_dict.get('exefile_specfile_name', ''):
            self._commands.extend(('-n', name))
        if datas_to_add := cmd_dict.get('other_data', []):
            for data in datas_to_add:
                self._commands.extend(('--add-data', f'{data};.'))
        if module_search_paths := cmd_dict.get('module_search_path', []):
            for module_path in module_search_paths:
                self._commands.extend(('-p', module_path))
        if key := cmd_dict.get('key', ''):
            self._commands.extend(('--key', key))
        if not cmd_dict.get('use_upx', False):
            self._commands.append('--noupx')
        if upx_excludes := cmd_dict.get('upx_exclude_files', []):
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
        self._commands.extend('--log-level', cmd_dict.get('log_level', 'INFO'))
        self._commands.append(cmd_dict.get('program_entry', ''))

    def pyi_info(self):
        if self.pyi_ready:
            return get_cmd_o(self.pyi_path, '-v')
        return 'Pyinstaller尚未准备就绪'

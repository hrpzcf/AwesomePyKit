# coding: utf-8

__doc__ = """包含pyinstaller相关的类或函数。"""

import os
from subprocess import PIPE, STARTF_USESHOWWINDOW, STARTUPINFO, STDOUT, SW_HIDE, Popen

from PyQt5.QtCore import QObject, QTimer, pyqtSignal

from utils.main import config_dir, get_cmd_out


class PyiTool(QObject):
    STARTUP = STARTUPINFO()
    STARTUP.dwFlags = STARTF_USESHOWWINDOW
    STARTUP.wShowWindow = SW_HIDE
    stdout = pyqtSignal(str)
    run_time = pyqtSignal(int)
    completed = pyqtSignal(int)

    def __init__(self, py_path="", cwd=os.getcwd()):
        super().__init__()
        self.initialize(py_path, cwd)
        self.cumulative = -200
        self.emt = QTimer()
        self.emt.timeout.connect(self._time)
        self.run_time.connect(self.timer_ctrl)
        self._log_level = None

    @property
    def cwd(self):
        return self._cwd

    @cwd.setter
    def cwd(self, path):
        if os.path.isdir(path):
            self._cwd = path

    @property
    def pyi_path(self):
        """返回给出的Python路径中的pyinstaller可执行文件路径。"""
        pyi_exec_path = os.path.join(self._py_path, "Scripts", "pyinstaller.exe")
        if not os.path.isfile(pyi_exec_path):
            return ""
        return pyi_exec_path

    @property
    def pyi_ready(self):
        """给出的Python目录中安装了pyinstaller返回True,否则返回False。"""
        return bool(self.pyi_path)

    def initialize(self, py_path, cwd):
        # 信任传入的py_path
        self._py_path = py_path
        self._cwd = cwd
        self._process = None
        self._commands = [self.pyi_path]

    def handle(self):
        if self._process is None:
            self._process = Popen(
                self._commands,
                stdin=PIPE,
                stdout=PIPE,
                stderr=STDOUT,
                text=True,
                cwd=self._cwd,
                startupinfo=self.STARTUP,
            )
        return self._process

    def _time(self):
        if self.cumulative > 10000:
            self.cumulative = 0
        self.cumulative += 10

    def timer_ctrl(self, code):
        if code:
            self.emt.start(10)
        else:
            self.emt.stop()
            self.cumulative = -200

    def _emit_split_line(self):
        for line in self._process.stdout:
            self.stdout.emit(line.strip())
        self.completed.emit(self._process.wait())

    def _emit_split_time(self):
        self.run_time.emit(1)
        lines = []
        for line in self._process.stdout:
            lines.append(line.strip())
            if self.cumulative > 80:
                self.stdout.emit("\n".join(lines))
                lines.clear()
                self.cumulative = 0
        self.completed.emit(self._process.wait())
        self.run_time.emit(0)

    def execute_cmd(self):
        """执行命令并读取输出流，通过信号发射字符串、返回码更新主界面面板。"""
        if self.pyi_ready and self._process:
            if self._log_level == "TRACE":
                self._emit_split_time()
            else:
                self._emit_split_line()
        else:
            if not self.pyi_ready:
                self.stdout.emit("当前Python环境中找不到PYINSTALLER。")
            if self._process is None:
                self.stdout.emit("请先调用handle方法获取进程操作句柄。")
            self.completed.emit(-1)

    def prepare_cmd(self, cmd_dict=None):
        """从cmd_dict添加PyInstaller命令选项。"""
        if cmd_dict is None:
            cmd_dict = {}
        self._log_level = cmd_dict.get("log_level", None)
        if cmd_dict.get("pack_to_one", "dir") == "dir":
            self._commands.append("-D")
        else:
            self._commands.append("-F")
        temp_var = cmd_dict.get("spec_dir", "")
        if temp_var:
            self._commands.extend(("--specpath", temp_var))
        temp_var = cmd_dict.get("exefile_specfile_name", "")
        if temp_var:
            self._commands.extend(("-n", temp_var))
        temp_var = cmd_dict.get("other_data", None)
        if temp_var:
            for data in temp_var:
                self._commands.extend(("--add-data", rf"{data[0]};{data[1]}"))
        temp_var = cmd_dict.get("module_search_path", None)
        if temp_var:
            for module_path in temp_var:
                self._commands.extend(("-p", module_path))
        temp_var = cmd_dict.get("key", "")
        if temp_var:
            self._commands.extend(("--key", temp_var))
        temp_var = cmd_dict.get("debug_options", None)
        if temp_var:
            for ikey, val in temp_var.items():
                if val:
                    self._commands.extend(("-d", ikey))
        if not cmd_dict.get("use_upx", False):
            self._commands.append("--noupx")
        temp_var = cmd_dict.get("upx_exclude_files", None)
        if temp_var:
            for exfile in temp_var:
                self._commands.extend(("--upx-exclude", exfile.lower()))
        if cmd_dict.get("execute_with_console", True):
            self._commands.append("-c")
        else:
            self._commands.append("-w")
        temp_var = cmd_dict.get("file_icon_path", "")
        if temp_var:
            self._commands.extend(("-i", temp_var))
        temp_var = self._build_info_file(cmd_dict)
        if cmd_dict.get("write_file_info", False) and temp_var:
            self._commands.extend(("--version-file", temp_var))
        temp_var = cmd_dict.get("runtime_tmpdir", None)
        if temp_var:
            self._commands.extend(("--runtime-tmpdir", temp_var))
        temp_var = cmd_dict.get("output_dir", "")
        if temp_var:
            self._commands.extend(("--distpath", temp_var))
        temp_var = cmd_dict.get("temp_working_dir", "")
        if temp_var:
            self._commands.extend(("--workpath", temp_var))
        if cmd_dict.get("without_confirm", False):
            self._commands.append("-y")
        temp_var = cmd_dict.get("upx_search_path", "")
        if temp_var:
            self._commands.extend(("--upx-dir", temp_var))
        if cmd_dict.get("clean_before_build", False):
            self._commands.append("--clean")
        self._commands.extend(("--log-level", cmd_dict.get("log_level", "INFO")))
        self._commands.append(cmd_dict.get("program_entry", ""))

    def pyi_info(self):
        if self.pyi_ready:
            return get_cmd_out(self.pyi_path, "-v")
        return "0.0"

    @staticmethod
    def _build_info_file(cmd_dict):
        FILE_VERSION_INFO = """# coding: utf-8

VSVersionInfo(
    ffi=FixedFileInfo(
        filevers=$filevers$,
        prodvers=$prodvers$,
        mask=0x3F,
        flags=0x0,
        OS=0x40004,
        fileType=0x1,
        subtype=0x0,
        date=(0, 0),),
    kids=[StringFileInfo(
    [StringTable(
        u'080404b0',
        [
            StringStruct(u'CompanyName', u'$CompanyName$'),
            StringStruct(u'FileDescription', u'$FileDescription$'),
            StringStruct(u'FileVersion', u'$FileVersion$'),
            StringStruct(u'LegalCopyright', u'$LegalCopyright$'),
            StringStruct(u'OriginalFilename', u'$OriginalFilename$'),
            StringStruct(u'ProductName', u'$ProductName$'),
            StringStruct(u'ProductVersion', u'$ProductVersion$'),
            StringStruct(u'LegalTrademarks', u'$LegalTrademarks$'),
        ],)]),
    VarFileInfo([VarStruct(u'Translation', [2052, 1200])]),
    ],)
"""
        for key, val in cmd_dict.get("file_ver_info", {}).items():
            FILE_VERSION_INFO = FILE_VERSION_INFO.replace(key, val)
        file_info_path = os.path.join(config_dir, "FILE_INFO")
        try:
            with open(file_info_path, "w", encoding="utf-8") as file_info:
                file_info.write(FILE_VERSION_INFO)
            return file_info_path
        except Exception:
            return ""

# coding: utf-8

__doc__ = "项目目录下虚拟环境的工具包"

from os import listdir, path
from random import randint

from fastpip import *

_CMD_PREFIX = ("-m", "venv")
_VENVPREFIX = "venv"
_VENV_CFGFILE = "pyvenv.cfg"


class VtEnv(PyEnv):
    def __init__(self, project_root=""):
        super().__init__("")
        self.__venv_exist = False
        self.__project_root = project_root

    @property
    def project_root(self):
        return self.__project_root if path.isdir(self.__project_root) else ""

    @project_root.setter
    def project_root(self, value):
        assert isinstance(value, str)
        self.__project_root = value

    def __find_venv_file(self, dir_path):
        self.__venv_exist = False
        try:
            names = listdir(dir_path)
        except:
            return False
        for name in names:
            fullpath = path.join(dir_path, name)
            if path.exists(path.join(fullpath, _VENV_CFGFILE)):
                self.path = fullpath
                self.__venv_exist = True
                return self.__venv_exist
        return False

    def find_venv(self):
        if not self.project_root:
            self.__venv_exist = False
            return self.__venv_exist
        return self.__find_venv_file(self.project_root)

    @property
    def venv_exists(self):
        return self.__venv_exist

    def create_project_venv(self, interpreter):
        if not self.project_root:
            return False
        while True:
            dir_name = ".%s_%d" % (_VENVPREFIX, randint(100, 999))
            venv_fullpath = path.join(self.__project_root, dir_name)
            if not path.exists(venv_fullpath):
                break
        cmds = Command(interpreter, *_CMD_PREFIX, venv_fullpath)
        strings, return_code = execute_commands(cmds, False, None)
        if return_code:
            return False
        self.__venv_exist = True
        self.path = venv_fullpath
        return self.__venv_exist

# coding: utf-8

__doc__ = "项目目录下虚拟环境的工具包"

from os import listdir, path
from random import randint

from fastpip import *

_CMD_PREFIX = ("-m", "venv")
_VENVPREFIX = "venv_"
_VENV_CFGFILE = "pyvenv.cfg"


class VirtualEnv(PyEnv):
    def __init__(self, project_root=""):
        super().__init__("")
        self.__venv_exist = False
        self.__project = project_root

    @property
    def project(self):
        return self.__project if path.isdir(self.__project) else ""

    @project.setter
    def project(self, value):
        self.__project = value

    def __find_venv_file(self, dir_path):
        try:
            names = listdir(dir_path)
        except:
            return False
        for p in names:
            fullpath = path.join(dir_path, p)
            if path.exists(path.join(fullpath, _VENV_CFGFILE)):
                self.path = fullpath
                self.__venv_exist = True
                return self.__venv_exist
        return False

    def find_project_venv(self):
        if not self.project:
            return False
        if self.__find_venv_file(self.project):
            return True
        parent_dir = path.dirname(self.project)
        if path.samefile(parent_dir, self.project):
            return False
        if self.__find_venv_file(parent_dir):
            return True
        parent_dir = path.dirname(parent_dir)
        if path.samefile(parent_dir, self.project):
            return False
        return self.__find_venv_file(parent_dir)

    @property
    def venv_exists(self):
        return self.__venv_exist

    def create_project_venv(self, interpreter):
        if not self.project:
            return False
        while True:
            dir_name = "%s%d" % (_VENVPREFIX, randint(1000, 9999))
            venv_fullpath = path.join(self.__project, dir_name)
            if not path.exists(venv_fullpath):
                break
        cmds = Command(interpreter, *_CMD_PREFIX, venv_fullpath)
        strings, return_code = execute_commands(cmds, False, None)
        if return_code:
            return False
        self.__venv_exist = True
        self.path = venv_fullpath
        return self.__venv_exist

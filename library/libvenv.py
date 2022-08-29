# coding: utf-8

__doc__ = "项目目录下虚拟环境的创建、使用工具包"

from os import listdir, path
from random import randint

from fastpip import PyEnv
from fastpip.core.fastpip import _execute_cmd
from fastpip.utils.cmdutil import Command

CMD_PREFIX = ("-m", "venv")
VENV_PREFIX = "venv_"
VENV_CONFIG_FILE = "pyvenv.cfg"


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

    def find_project_venv(self):
        if not self.project:
            return False
        try:
            names = listdir(self.__project)
        except:
            return False
        for p in names:
            fullpath = path.join(self.__project, p)
            if path.exists(path.join(fullpath, VENV_CONFIG_FILE)):
                self.path = fullpath
                self.__venv_exist = True
                break
        return self.__venv_exist

    @property
    def venv_exists(self):
        return self.__venv_exist

    def create_project_venv(self, interpreter):
        if not self.project:
            return False
        dir_name = "%s%d" % (VENV_PREFIX, randint(1000, 9999))
        while True:
            venv_fullpath = path.join(self.__project, dir_name)
            if not path.exists(venv_fullpath):
                break
            dir_name = "%s%d" % (VENV_PREFIX, randint(1000, 9999))
        cmds = Command(interpreter, *CMD_PREFIX, venv_fullpath)
        _, return_code = _execute_cmd(cmds, "", True, True, None)
        if return_code:
            return False
        self.__venv_exist = True
        self.path = venv_fullpath
        return self.__venv_exist

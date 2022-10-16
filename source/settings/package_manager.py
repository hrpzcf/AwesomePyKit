# coding: utf-8

from .abstract_config import AbstractConfig

_shared_saved_pypaths = None


def get_shared_pypaths():
    return _shared_saved_pypaths


class PackageManagerConfig(AbstractConfig):
    """包管理器的设置类"""

    key_python_paths = "python_paths"
    key_include_pre = "include_pre"
    key_install_for_user = "install_for_user"
    key_index_url = "index_url"
    key_last_path = "last_path"
    key_use_index_url = "use_index_url"
    key_package_names = "package_names"

    CONFIGFILE = "package_manager.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE)
        global _shared_saved_pypaths
        _shared_saved_pypaths = self.pypaths

    @property
    def pypaths(self):
        if self.key_python_paths not in self:
            self[self.key_python_paths] = list()
        return self[self.key_python_paths]

    @pypaths.setter
    def pypaths(self, value: list):
        assert isinstance(value, list)
        self[self.key_python_paths].clear()
        self[self.key_python_paths].extend(value)

    @property
    def include_pre(self):
        if self.key_include_pre not in self:
            self[self.key_include_pre] = False
        return self[self.key_include_pre]

    @include_pre.setter
    def include_pre(self, value: bool):
        assert isinstance(value, bool)
        self[self.key_include_pre] = value

    @property
    def install_for_user(self):
        if self.key_install_for_user not in self:
            self[self.key_install_for_user] = False
        return self[self.key_install_for_user]

    @install_for_user.setter
    def install_for_user(self, value: bool):
        assert isinstance(value, bool)
        self[self.key_install_for_user] = value

    @property
    def last_path(self):
        if self.key_last_path not in self:
            self[self.key_last_path] = "."
        return self[self.key_last_path]

    @last_path.setter
    def last_path(self, value):
        assert isinstance(value, str)
        self[self.key_last_path] = value

    @property
    def index_url(self):
        if self.key_index_url not in self:
            self[self.key_index_url] = ""
        return self[self.key_index_url]

    @index_url.setter
    def index_url(self, value):
        assert isinstance(value, str)
        self[self.key_index_url] = value

    @property
    def use_index_url(self):
        if self.key_use_index_url not in self:
            self[self.key_use_index_url] = False
        return self[self.key_use_index_url]

    @use_index_url.setter
    def use_index_url(self, value: bool):
        assert isinstance(value, bool)
        self[self.key_use_index_url] = value

    @property
    def package_names(self):
        if self.key_package_names not in self:
            self[self.key_package_names] = list()
        return self[self.key_package_names]

    @package_names.setter
    def package_names(self, value: list):
        assert isinstance(value, list)
        self[self.key_package_names] = value

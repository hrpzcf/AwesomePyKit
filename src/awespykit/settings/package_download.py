# coding: utf-8

from typing import Sequence

from .abstract_config import AbstractConfig
from .package_manager import get_shared_pypaths


class PackageDownloadConfig(AbstractConfig):
    """模块安装包下载器的设置类"""

    _key_package_names = "package_names"
    _key_derived_from = "derived_from"
    _key_download_deps = "download_deps"
    _key_download_type = "download_type"
    _key_include_pre = "include_pre"
    _key_ignore_requires_python = "ignore_requires_python"
    _key_save_path = "save_path"
    _key_platform = "platform"
    _key_python_version = "python_version"
    _key_implementation = "implementation"
    _key_abis = "abis"
    _key_index_url = "index_url"
    _key_use_index_url = "use_index_url"
    _key_window_size = "window_size"
    _key_dlstatus_winsize = "dlstatus_winsize"

    CONFIGFILE = "package_download.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE)

    @property
    def package_names(self):
        if self._key_package_names not in self:
            self[self._key_package_names] = list()
        return self[self._key_package_names]

    @package_names.setter
    def package_names(self, value):
        assert isinstance(value, list)
        self[self._key_package_names] = value

    @property
    def derived_from(self):
        if self._key_derived_from not in self:
            self[self._key_derived_from] = -1
        return self[self._key_derived_from]

    @derived_from.setter
    def derived_from(self, value):
        assert isinstance(value, int)
        self[self._key_derived_from] = value

    @property
    def download_deps(self):
        if self._key_download_deps not in self:
            self[self._key_download_deps] = True
        return self[self._key_download_deps]

    @download_deps.setter
    def download_deps(self, value):
        assert isinstance(value, bool)
        self[self._key_download_deps] = value

    @property
    def download_type(self):
        if self._key_download_type not in self:
            self[self._key_download_type] = "unlimited"
        return self[self._key_download_type]

    @download_type.setter
    def download_type(self, value):
        assert value in (
            "unlimited",
            "no_binary",
            "only_binary",
            "prefer_binary",
        )
        self[self._key_download_type] = value

    @property
    def include_pre(self):
        if self._key_include_pre not in self:
            self[self._key_include_pre] = False
        return self[self._key_include_pre]

    @include_pre.setter
    def include_pre(self, value):
        assert isinstance(value, bool)
        self[self._key_include_pre] = value

    @property
    def ignore_requires_python(self):
        if self._key_ignore_requires_python not in self:
            self[self._key_ignore_requires_python] = False
        return self[self._key_ignore_requires_python]

    @ignore_requires_python.setter
    def ignore_requires_python(self, value):
        assert isinstance(value, bool)
        self[self._key_ignore_requires_python] = value

    @property
    def save_path(self):
        if self._key_save_path not in self:
            self[self._key_save_path] = ""
        return self[self._key_save_path]

    @save_path.setter
    def save_path(self, value):
        assert isinstance(value, str)
        self[self._key_save_path] = value

    @property
    def platform(self):
        if self._key_platform not in self:
            self[self._key_platform] = list()
        return self[self._key_platform]

    @platform.setter
    def platform(self, value):
        assert isinstance(value, list)
        self[self._key_platform] = value

    @property
    def python_version(self):
        if self._key_python_version not in self:
            self[self._key_python_version] = ""
        return self[self._key_python_version]

    @python_version.setter
    def python_version(self, value):
        assert isinstance(value, str)
        self[self._key_python_version] = value

    @property
    def implementation(self):
        if self._key_implementation not in self:
            self[self._key_implementation] = ""
        return self[self._key_implementation]

    @implementation.setter
    def implementation(self, value):
        assert isinstance(value, str)
        self[self._key_implementation] = value

    @property
    def abis(self):
        if self._key_abis not in self:
            self[self._key_abis] = list()
        return self[self._key_abis]

    @abis.setter
    def abis(self, value):
        assert isinstance(value, list)
        self[self._key_abis] = value

    @property
    def index_url(self):
        if self._key_index_url not in self:
            self[self._key_index_url] = ""
        return self[self._key_index_url]

    @index_url.setter
    def index_url(self, value):
        assert isinstance(value, str)
        self[self._key_index_url] = value

    @property
    def use_index_url(self):
        if self._key_use_index_url not in self:
            self[self._key_use_index_url] = False
        return self[self._key_use_index_url]

    @use_index_url.setter
    def use_index_url(self, value):
        assert isinstance(value, bool)
        self[self._key_use_index_url] = value

    @property
    def cur_pypaths(self):
        shared_pypaths = get_shared_pypaths()
        if shared_pypaths is None:
            return list()
        assert isinstance(shared_pypaths, list)
        return shared_pypaths

    @property
    def window_size(self):
        if self._key_window_size not in self:
            self[self._key_window_size] = 620, 660
        return self[self._key_window_size]

    @window_size.setter
    def window_size(self, value):
        assert isinstance(value, Sequence)
        assert len(value) == 2
        assert isinstance(value[0], int) and isinstance(value[1], int)
        self[self._key_window_size] = value

    @property
    def dlstatus_winsize(self):
        if self._key_dlstatus_winsize not in self:
            self[self._key_dlstatus_winsize] = 260, 500
        return self[self._key_dlstatus_winsize]

    @dlstatus_winsize.setter
    def dlstatus_winsize(self, value):
        assert isinstance(value, Sequence)
        assert len(value) == 2
        assert isinstance(value[0], int) and isinstance(value[1], int)
        self[self._key_dlstatus_winsize] = value

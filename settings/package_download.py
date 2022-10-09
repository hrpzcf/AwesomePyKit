# coding: utf-8

from .abstract_settings import AbstractSettings
from  .package_manager import get_global_pypaths


class PackageDownloadSettings(AbstractSettings):
    """模块安装包下载器的设置类"""

    key_package_names = "package_names"
    key_derived_from = "derived_from"
    key_download_deps = "download_deps"
    key_download_type = "download_type"
    key_include_pre = "include_pre"
    key_ignore_requires_python = "ignore_requires_python"
    key_save_path = "save_path"
    key_platform = "platform"
    key_python_version = "python_version"
    key_implementation = "implementation"
    key_abis = "abis"
    key_index_url = "index_url"
    key_use_index_url = "use_index_url"

    CONFIGFILE = "package_download.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE)

    @property
    def package_names(self):
        if self.key_package_names not in self:
            self[self.key_package_names] = list()
        return self[self.key_package_names]

    @package_names.setter
    def package_names(self, value):
        assert isinstance(value, list)
        self[self.key_package_names] = value

    @property
    def derived_from(self):
        if self.key_derived_from not in self:
            self[self.key_derived_from] = -1
        return self[self.key_derived_from]

    @derived_from.setter
    def derived_from(self, value):
        assert isinstance(value, int)
        self[self.key_derived_from] = value

    @property
    def download_deps(self):
        if self.key_download_deps not in self:
            self[self.key_download_deps] = True
        return self[self.key_download_deps]

    @download_deps.setter
    def download_deps(self, value):
        assert isinstance(value, bool)
        self[self.key_download_deps] = value

    @property
    def download_type(self):
        if self.key_download_type not in self:
            self[self.key_download_type] = "unlimited"
        return self[self.key_download_type]

    @download_type.setter
    def download_type(self, value):
        assert value in ("unlimited", "no_binary", "only_binary", "prefer_binary")
        self[self.key_download_type] = value

    @property
    def include_pre(self):
        if self.key_include_pre not in self:
            self[self.key_include_pre] = False
        return self[self.key_include_pre]

    @include_pre.setter
    def include_pre(self, value):
        assert isinstance(value, bool)
        self[self.key_include_pre] = value

    @property
    def ignore_requires_python(self):
        if self.key_ignore_requires_python not in self:
            self[self.key_ignore_requires_python] = False
        return self[self.key_ignore_requires_python]

    @ignore_requires_python.setter
    def ignore_requires_python(self, value):
        assert isinstance(value, bool)
        self[self.key_ignore_requires_python] = value

    @property
    def save_path(self):
        if self.key_save_path not in self:
            self[self.key_save_path] = ""
        return self[self.key_save_path]

    @save_path.setter
    def save_path(self, value):
        assert isinstance(value, str)
        self[self.key_save_path] = value

    @property
    def platform(self):
        if self.key_platform not in self:
            self[self.key_platform] = list()
        return self[self.key_platform]

    @platform.setter
    def platform(self, value):
        assert isinstance(value, list)
        self[self.key_platform] = value

    @property
    def python_version(self):
        if self.key_python_version not in self:
            self[self.key_python_version] = ""
        return self[self.key_python_version]

    @python_version.setter
    def python_version(self, value):
        assert isinstance(value, str)
        self[self.key_python_version] = value

    @property
    def implementation(self):
        if self.key_implementation not in self:
            self[self.key_implementation] = ""
        return self[self.key_implementation]

    @implementation.setter
    def implementation(self, value):
        assert isinstance(value, str)
        self[self.key_implementation] = value

    @property
    def abis(self):
        if self.key_abis not in self:
            self[self.key_abis] = list()
        return self[self.key_abis]

    @abis.setter
    def abis(self, value):
        assert isinstance(value, list)
        self[self.key_abis] = value

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
    def use_index_url(self, value):
        assert isinstance(value, bool)
        self[self.key_use_index_url] = value

    @property
    def cur_pypaths(self):
        global_pypaths = get_global_pypaths()
        if global_pypaths is None:
            return list()
        assert isinstance(global_pypaths, list)
        return global_pypaths

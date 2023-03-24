# coding: utf-8

from copy import deepcopy
from typing import *

from com import WorkDir

from .abstract_config import AbstractConfig
from .package_manager import get_shared_pypaths


class CloudFunctionCFG(dict):
    _key_project_paths = "project_paths"
    _key_selected_env = "selected_env"
    _key_previous_path = "previous_path"
    _key_overwrite_reqfile = "overwrite_reqfile"
    _key_projectpath_index = "projectpath_index"
    _key_working_tempdir = "working_tempdir"
    _key_custom_tmpdir = "custom_tmpdir"
    _key_generated_dir = "generated_dir"
    _key_generated_name = "generated_name"
    _key_overwrite_samefile = "overwrite_samefile"
    _key_upgrade_requires = "upgrade_requires"
    _key_excluded_paths = "excluded_paths"

    def __init__(self):
        super().__init__()

    @property
    def project_paths(self) -> List[str]:
        return self.setdefault(self._key_project_paths, list())

    @project_paths.setter
    def project_paths(self, value):
        assert isinstance(value, list)
        assert all(isinstance(i, str) for i in value)
        self[self._key_project_paths] = value

    @property
    def selected_env(self) -> int:
        return self.setdefault(self._key_selected_env, -1)

    @selected_env.setter
    def selected_env(self, value):
        assert isinstance(value, int)
        self[self._key_selected_env] = value

    @property
    def previous_path(self):
        return self.setdefault(self._key_previous_path, "")

    @previous_path.setter
    def previous_path(self, value):
        assert isinstance(value, str)
        self[self._key_previous_path] = value

    @property
    def overwrite_reqfile(self):
        return self.setdefault(self._key_overwrite_reqfile, False)

    @overwrite_reqfile.setter
    def overwrite_reqfile(self, value):
        assert isinstance(value, bool)
        self[self._key_overwrite_reqfile] = value

    @property
    def projectpath_index(self):
        return self.setdefault(self._key_projectpath_index, -1)

    @projectpath_index.setter
    def projectpath_index(self, value):
        assert isinstance(value, int)
        self[self._key_projectpath_index] = value

    @property
    def working_tmpdir(self) -> WorkDir:
        value = self.setdefault(self._key_working_tempdir, WorkDir.TmpDir)
        if not isinstance(value, WorkDir):
            try:
                value = WorkDir(value)
            except:
                value = WorkDir.TmpDir
            self[self._key_working_tempdir] = value
        return self[self._key_working_tempdir]

    @working_tmpdir.setter
    def working_tmpdir(self, value):
        assert isinstance(value, WorkDir)
        self[self._key_working_tempdir] = value

    @property
    def custom_tempdir(self):
        return self.setdefault(self._key_custom_tmpdir, "")

    @custom_tempdir.setter
    def custom_tempdir(self, value):
        assert isinstance(value, str)
        self[self._key_custom_tmpdir] = value

    @property
    def generated_dir(self):
        return self.setdefault(self._key_generated_dir, "")

    @generated_dir.setter
    def generated_dir(self, value):
        assert isinstance(value, str)
        self[self._key_generated_dir] = value

    @property
    def generated_name(self):
        return self.setdefault(self._key_generated_name, "")

    @generated_name.setter
    def generated_name(self, value):
        assert isinstance(value, str)
        self[self._key_generated_name] = value

    @property
    def overwrite_samefile(self):
        return self.setdefault(self._key_overwrite_samefile, False)

    @overwrite_samefile.setter
    def overwrite_samefile(self, value):
        assert isinstance(value, bool)
        self[self._key_overwrite_samefile] = value

    @property
    def upgrade_requires(self):
        return self.setdefault(self._key_upgrade_requires, False)

    @upgrade_requires.setter
    def upgrade_requires(self, value):
        assert isinstance(value, bool)
        self[self._key_upgrade_requires] = value

    @property
    def excluded_paths(self) -> List[str]:
        return self.setdefault(self._key_excluded_paths, [])

    @excluded_paths.setter
    def excluded_paths(self, value):
        assert isinstance(value, list)
        self[self._key_excluded_paths] = value


class CloudFunctionConfig(AbstractConfig):
    _key_current = "current"
    _key_multi_cfg = "multicfg"
    _key_window_size = "window_size"
    _key_exc_windowsize = "exc_windowsize"

    CONFIGFILE = "cloud_function.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE)

    @property
    def cur_pypaths(self):
        shared_pypaths = get_shared_pypaths()
        if shared_pypaths is None:
            return list()
        assert isinstance(shared_pypaths, list)
        return shared_pypaths

    @property
    def window_size(self):
        return self.setdefault(self._key_window_size, (600, 500))

    @window_size.setter
    def window_size(self, value):
        assert isinstance(value, Sequence)
        assert len(value) == 2
        assert isinstance(value[0], int) and isinstance(value[1], int)
        self[self._key_window_size] = value

    @property
    def exc_windowsize(self):
        return self.setdefault(self._key_exc_windowsize, (500, 400))

    @exc_windowsize.setter
    def exc_windowsize(self, value):
        assert isinstance(value, Sequence)
        assert len(value) == 2
        assert isinstance(value[0], int) and isinstance(value[1], int)
        self[self._key_exc_windowsize] = value

    def checkout_cfg(self, name: str) -> bool:
        if name not in self.multicfg:
            return False
        self.current.clear()
        self.current.update(self.multicfg[name])
        return True

    def store_curcfg(self, name: str) -> bool:
        if not name or not isinstance(name, str):
            return False
        self.multicfg[name] = deepcopy(self.current)
        return True

    @property
    def multicfg(self) -> dict:
        if self._key_multi_cfg not in self:
            self[self._key_multi_cfg] = dict()
        return self[self._key_multi_cfg]

    @property
    def current(self) -> CloudFunctionCFG:
        if self._key_current not in self:
            self[self._key_current] = CloudFunctionCFG()
        elif not isinstance(self[self._key_current], CloudFunctionCFG):
            new_scf_configure = CloudFunctionCFG()
            new_scf_configure.update(self[self._key_current])
            self[self._key_current] = new_scf_configure
        return self[self._key_current]

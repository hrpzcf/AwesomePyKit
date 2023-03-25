# coding: utf-8

from copy import deepcopy
from typing import Sequence

from .abstract_config import AbstractConfig
from .package_manager import get_shared_pypaths


class PyiConfigure(dict):
    _key_script_path = "script_path"
    _key_program_root = "program_root"
    _key_project_root = "project_root"
    _key_bundle_spec_name = "bundle_spec_name"
    _key_module_paths = "module_paths"
    _key_other_datas = "other_datas"
    _key_icon_path = "icon_path"
    _key_onedir_bundle = "onedir_bundle"
    _key_provide_console = "provide_console"
    _key_no_confirm = "no_confirm"
    _key_donot_use_upx = "donot_use_upx"
    _key_clean_building = "clean_building"
    _key_add_verfile = "add_verfile"
    _key_working_dir = "working_dir"
    _key_distribution_dir = "distribution_dir"
    _key_spec_dir = "spec_dir"
    _key_upx_dir = "upx_dir"
    _key_upx_excludes = "upx_excludes"
    _key_environ_path = "environ_path"
    _key_log_level = "log_level"
    _key_version_info = "version_info"
    _key_debug_options = "debug_options"
    _key_runtime_tmpdir = "runtime_tmpdir"
    _key_prioritize_venv = "prioritize_venv"
    _key_encryption_key = "encryption_key"
    _key_uac_admin = "uac_admin"
    _key_open_dist_folder = "open_dist_folder"
    _key_delete_spec_file = "delete_spec_file"
    _key_delete_working_dir = "delete_working_dir"
    _key_hidden_imports = "hidden_imports"
    _key_exclude_modules = "exclude_modules"

    def __init__(self):
        super().__init__()

    @property
    def script_path(self):
        return self.setdefault(self._key_script_path, "")

    @script_path.setter
    def script_path(self, value):
        assert isinstance(value, str)
        self[self._key_script_path] = value

    @property
    def program_root(self):
        return self.setdefault(self._key_program_root, "")

    @program_root.setter
    def program_root(self, value):
        assert isinstance(value, str)
        self[self._key_program_root] = value

    @property
    def project_root(self):
        return self.setdefault(self._key_project_root, "")

    @project_root.setter
    def project_root(self, value):
        assert isinstance(value, str)
        self[self._key_project_root] = value

    @property
    def bundle_spec_name(self):
        return self.setdefault(self._key_bundle_spec_name, "")

    @bundle_spec_name.setter
    def bundle_spec_name(self, value):
        assert isinstance(value, str)
        self[self._key_bundle_spec_name] = value

    @property
    def module_paths(self):
        return self.setdefault(self._key_module_paths, list())

    @module_paths.setter
    def module_paths(self, value):
        assert isinstance(value, list)
        self[self._key_module_paths] = value

    @property
    def other_datas(self):
        return self.setdefault(self._key_other_datas, list())

    @other_datas.setter
    def other_datas(self, value):
        assert isinstance(value, list)
        self[self._key_other_datas] = value

    @property
    def icon_path(self):
        return self.setdefault(self._key_icon_path, "")

    @icon_path.setter
    def icon_path(self, value):
        assert isinstance(value, str)
        self[self._key_icon_path] = value

    @property
    def onedir_bundle(self):
        return self.setdefault(self._key_onedir_bundle, True)

    @onedir_bundle.setter
    def onedir_bundle(self, value):
        assert isinstance(value, bool)
        self[self._key_onedir_bundle] = value

    @property
    def provide_console(self):
        return self.setdefault(self._key_provide_console, True)

    @provide_console.setter
    def provide_console(self, value):
        assert isinstance(value, bool)
        self[self._key_provide_console] = value

    @property
    def no_confirm(self):
        return self.setdefault(self._key_no_confirm, False)

    @no_confirm.setter
    def no_confirm(self, value):
        assert isinstance(value, bool)
        self[self._key_no_confirm] = value

    @property
    def donot_use_upx(self):
        return self.setdefault(self._key_donot_use_upx, False)

    @donot_use_upx.setter
    def donot_use_upx(self, value):
        assert isinstance(value, bool)
        self[self._key_donot_use_upx] = value

    @property
    def clean_building(self):
        return self.setdefault(self._key_clean_building, False)

    @clean_building.setter
    def clean_building(self, value):
        assert isinstance(value, bool)
        self[self._key_clean_building] = value

    @property
    def add_verfile(self):
        return self.setdefault(self._key_add_verfile, False)

    @add_verfile.setter
    def add_verfile(self, value):
        assert isinstance(value, bool)
        self[self._key_add_verfile] = value

    @property
    def working_dir(self):
        return self.setdefault(self._key_working_dir, "")

    @working_dir.setter
    def working_dir(self, value):
        assert isinstance(value, str)
        self[self._key_working_dir] = value

    @property
    def distribution_dir(self):
        return self.setdefault(self._key_distribution_dir, "")

    @distribution_dir.setter
    def distribution_dir(self, value):
        assert isinstance(value, str)
        self[self._key_distribution_dir] = value

    @property
    def spec_dir(self):
        return self.setdefault(self._key_spec_dir, "")

    @spec_dir.setter
    def spec_dir(self, value):
        assert isinstance(value, str)
        self[self._key_spec_dir] = value

    @property
    def upx_dir(self):
        return self.setdefault(self._key_upx_dir, "")

    @upx_dir.setter
    def upx_dir(self, value):
        assert isinstance(value, str)
        self[self._key_upx_dir] = value

    @property
    def upx_excludes(self):
        return self.setdefault(self._key_upx_excludes, list())

    @upx_excludes.setter
    def upx_excludes(self, value):
        assert isinstance(value, list)
        self[self._key_upx_excludes] = value

    @property
    def environ_path(self):
        return self.setdefault(self._key_environ_path, "")

    @environ_path.setter
    def environ_path(self, value):
        assert isinstance(value, str)
        self[self._key_environ_path] = value

    @property
    def log_level(self):
        return self.setdefault(self._key_log_level, "INFO")

    @log_level.setter
    def log_level(self, value):
        assert value in ("TRACE", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL")
        self[self._key_log_level] = value

    @property
    def version_info(self):
        default = {
            "$filevers$": "(0, 0, 0, 0)",
            "$prodvers$": "(0, 0, 0, 0)",
            "$CompanyName$": "",
            "$FileDescription$": "",
            "$LegalCopyright$": "",
            "$OriginalFilename$": "",
            "$ProductName$": "",
            "$FileVersion$": "0.0.0.0",
            "$ProductVersion$": "0.0.0.0",
            "$LegalTrademarks$": "",
        }
        return self.setdefault(self._key_version_info, default)

    @version_info.setter
    def version_info(self, value):
        assert isinstance(value, dict)
        self[self._key_version_info] = value

    @property
    def debug_options(self):
        default = {"imports": False, "bootloader": False, "noarchive": False}
        return self.setdefault(self._key_debug_options, default)

    @debug_options.setter
    def debug_options(self, value):
        assert isinstance(value, dict)
        self[self._key_debug_options] = value

    @property
    def runtime_tmpdir(self):
        return self.setdefault(self._key_runtime_tmpdir, "")

    @runtime_tmpdir.setter
    def runtime_tmpdir(self, value):
        assert isinstance(value, str)
        self[self._key_runtime_tmpdir] = value

    @property
    def prioritize_venv(self):
        return self.setdefault(self._key_prioritize_venv, False)

    @prioritize_venv.setter
    def prioritize_venv(self, value):
        assert isinstance(value, bool)
        self[self._key_prioritize_venv] = value

    @property
    def encryption_key(self):
        return self.setdefault(self._key_encryption_key, "")

    @encryption_key.setter
    def encryption_key(self, value):
        assert isinstance(value, str)
        self[self._key_encryption_key] = value

    @property
    def uac_admin(self):
        return self.setdefault(self._key_uac_admin, False)

    @uac_admin.setter
    def uac_admin(self, value):
        assert isinstance(value, bool)
        self[self._key_uac_admin] = value

    @property
    def open_dist_folder(self):
        return self.setdefault(self._key_open_dist_folder, False)

    @open_dist_folder.setter
    def open_dist_folder(self, value):
        assert isinstance(value, bool)
        self[self._key_open_dist_folder] = value

    @property
    def delete_spec_file(self):
        return self.setdefault(self._key_delete_spec_file, False)

    @delete_spec_file.setter
    def delete_spec_file(self, value):
        assert isinstance(value, bool)
        self[self._key_delete_spec_file] = value

    @property
    def delete_working_dir(self):
        return self.setdefault(self._key_delete_working_dir, False)

    @delete_working_dir.setter
    def delete_working_dir(self, value):
        assert isinstance(value, bool)
        self[self._key_delete_working_dir] = value

    @property
    def hidden_imports(self):
        return self.setdefault(self._key_hidden_imports, list())

    @hidden_imports.setter
    def hidden_imports(self, value):
        assert isinstance(value, list)
        self[self._key_hidden_imports] = value

    @property
    def exclude_modules(self):
        return self.setdefault(self._key_exclude_modules, list())

    @exclude_modules.setter
    def exclude_modules(self, value):
        assert isinstance(value, list)
        self[self._key_exclude_modules] = value


class PyinstallerToolConfig(AbstractConfig):
    _key_window_size = "window_size"
    _key_impcheck_winsize = "impcheck_winsize"
    _key_envch_winsize = "envch_winsize"
    _key_current = "current"
    _key_multi_cfg = "multicfg"

    CONFIGFILE = "pyinstaller_assistant.json"

    def __init__(self):
        super().__init__(self.CONFIGFILE)

    def checkout_cfg(self, name: str) -> bool:
        if name not in self.multicfg:
            return False
        self.current.clear()
        self.current.update(self.multicfg[name])
        return True

    def store_curcfg(self, name: str) -> bool:
        if not name or not isinstance(name, str):
            return False
        new_settings_dict = dict()
        new_settings_dict.update(self.current)
        self.multicfg[name] = deepcopy(new_settings_dict)
        return True

    @property
    def pypaths(self):
        shared_pypaths = get_shared_pypaths()
        if shared_pypaths is None:
            return list()
        assert isinstance(shared_pypaths, list)
        return shared_pypaths

    @property
    def multicfg(self) -> dict:
        if self._key_multi_cfg not in self:
            self[self._key_multi_cfg] = dict()
        return self[self._key_multi_cfg]

    @property
    def current(self) -> PyiConfigure:
        if self._key_current not in self:
            self[self._key_current] = PyiConfigure()
        elif not isinstance(self[self._key_current], PyiConfigure):
            new_pyi_configure = PyiConfigure()
            new_pyi_configure.update(self[self._key_current])
            self[self._key_current] = new_pyi_configure
        return self[self._key_current]

    @property
    def window_size(self):
        if self._key_window_size not in self:
            self[self._key_window_size] = 960, 600
        return self[self._key_window_size]

    @window_size.setter
    def window_size(self, value):
        assert isinstance(value, Sequence)
        assert len(value) == 2
        assert isinstance(value[0], int) and isinstance(value[1], int)
        self[self._key_window_size] = value

    @property
    def envch_winsize(self):
        if self._key_envch_winsize not in self:
            self[self._key_envch_winsize] = 430, 200
        return self[self._key_envch_winsize]

    @envch_winsize.setter
    def envch_winsize(self, value):
        assert isinstance(value, Sequence)
        assert len(value) == 2
        assert isinstance(value[0], int) and isinstance(value[1], int)
        self[self._key_envch_winsize] = value

    @property
    def impcheck_winsize(self):
        if self._key_impcheck_winsize not in self:
            self[self._key_impcheck_winsize] = 960, 600
        return self[self._key_impcheck_winsize]

    @impcheck_winsize.setter
    def impcheck_winsize(self, value):
        assert isinstance(value, Sequence)
        assert len(value) == 2
        assert isinstance(value[0], int) and isinstance(value[1], int)
        self[self._key_impcheck_winsize] = value

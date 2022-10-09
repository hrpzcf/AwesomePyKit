# coding: utf-8

import os
import os.path as op
import sys

_runs_in_bundle_mode = getattr(sys, "frozen", False)
if _runs_in_bundle_mode:
    _res_root = sys._MEIPASS
else:
    _res_root = op.dirname(op.dirname(op.abspath(__file__)))
_appdata_local_folder = os.getenv("LOCALAPPDATA")
if not _appdata_local_folder:
    if _runs_in_bundle_mode:
        config_root = op.dirname(sys.executable)
    else:
        config_root = _res_root
else:
    config_root = op.join(_appdata_local_folder, "Awespykit")
config_root = op.join(config_root, "config")


__all__ = [
    "IndexManagerSettings",
    "PackageManagerSettings",
    "PackageDownloadSettings",
]

from .indexurl_manager import IndexManagerSettings
from .package_manager import PackageManagerSettings
from .package_download import PackageDownloadSettings
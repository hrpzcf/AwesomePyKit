# coding: utf-8

try:
    import importlib.metadata as metadata
except ImportError:
    import importlib_metadata as metadata

__PRESET_VERSION = "2.0.1"

NAME = "Awespykit"
try:
    VERSION = metadata.version(NAME)
except:
    VERSION = __PRESET_VERSION
AUTHOR = "hrp/hrpzcf"

__all__ = ["AUTHOR", "NAME", "VERSION"]

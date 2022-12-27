# coding: utf-8

import os

from setuptools import *

from source.awespykit.__info__ import *

req_file = "requirements.txt"
description = "一个关于 Python 的 GUI 工具箱：包管理器、程序打包、切换 pip 源、模块安装包下载。"
try:
    with open("README.md", "rt", encoding="utf-8") as md:
        long_description = md.read()
except Exception:
    long_description = description
assert os.path.isfile(req_file), "'requirements.txt' does not exist!"
with open(req_file, "rt", encoding="utf-8") as rf:
    install_requires = [s.strip(os.linesep) for s in rf if s]

setup(
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=NAME,
    url=URL,
    author=AUTHOR,
    version=VERSION,
    license="GNU General Public License v3 (GPLv3)",
    install_requires=install_requires,
    package_dir={"": "source"},
    packages=find_packages("source"),
    python_requires=">=3.7",
    platforms=["win32", "win_amd64"],
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Environment :: Win32 (MS Windows)",
    ],
    package_data={"awespykit": ["help/About.html"]},
    entry_points={
        "console_scripts": [
            "rpk = awespykit.runpykit:run_pykit_sysexit_when_close"
        ]
    },
)

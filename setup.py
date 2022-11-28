# coding: utf-8

from setuptools import *

from source.awespykit.__info__ import *

description = "一个关于 Python 的 GUI 工具箱：包管理器、程序打包、切换 pip 源、模块安装包下载。"

try:
    with open("README.md", "rt", encoding="utf-8") as md:
        long_description = md.read()
except Exception:
    long_description = description

setup(
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    name=NAME,
    url=URL,
    author=AUTHOR,
    version=VERSION,
    license="MIT License",
    install_requires=["chardet>=4.0.0", "PyQt5>=5.15.0", "fastpip>=1.4.1,<2.0"],
    package_dir={"": "source"},
    packages=find_packages("source"),
    python_requires=">=3.7",
    platforms=["win32", "win_amd64"],
    classifiers=[
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    package_data={"awespykit": ["help/About.html"]},
    entry_points={
        "console_scripts": ["rpk = awespykit.runpykit:run_pykit_sysexit_when_close"]
    },
)

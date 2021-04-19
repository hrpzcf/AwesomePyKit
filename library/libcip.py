# coding: utf-8

__doc__ = "包含检查项目导入模块所需的类、函数等。"

import os
import re

from chardet.universaldetector import UniversalDetector

from .libm import PyEnv


def file_encodings(project_root):
    pattern = re.compile(r"^.+\.py[w]?$")
    path_encoding_groups = []
    for root, _, files in os.walk(project_root):
        for name in files:
            if not pattern.match(name):
                continue
            path_encoding_groups.append(os.path.join(root, name))
    encoding_detector = UniversalDetector()
    for index, file_path in enumerate(path_encoding_groups):
        encoding_detector.reset()
        try:
            with open(file_path, "rb") as sf:
                for line in sf:
                    encoding_detector.feed(line)
                    if encoding_detector.done:
                        break
            encoding_detector.close()
            path_encoding_groups[index] = (
                file_path,
                encoding_detector.result["encoding"],
            )
        except Exception:
            path_encoding_groups[index] = file_path, None
    return path_encoding_groups


class ImportInspector:
    match_all = re.compile(r"^[^#\n]*?import [_0-9a-zA-Z .,;(]+$", re.M)

    def __init__(self, python_dir, project_root):
        self._root = project_root
        self._imports = PyEnv(python_dir).imports()
        self._imports.extend(self.project_imports())

    def missing_items(self):
        """
        返回给定Python环境中，给定目录内脚本导入但环境未安装的模块集合。
        返回值类型：(文件路径, {文件中导入的模块}, {环境中未安装的模块})。
        """
        groups = file_encodings(self._root)
        if groups:
            for _path, encoding in groups:
                if encoding is None:
                    continue
                try:
                    with open(_path, encoding=encoding) as sf:
                        string = sf.read()
                    imps, missing = self.missing_imports(string)
                    yield _path, imps, missing
                except Exception:
                    yield _path, None, None
        else:
            yield None, None, None

    def missing_imports(self, string):
        """
        查找环境中未安装但string中需要导入的模块。
        pre3为最终处理后得到的string中所有导入的模块列表。
        """
        final_res, processed_2, processed_1 = (
            set(),
            [],
            self.match_all.findall(string),
        )
        for item in processed_1:
            if ";" in item:
                for string in item.split(";"):
                    if string:
                        processed_2.append(string.strip())
            else:
                processed_2.append(item)
        for item in processed_2:
            if "from " in item:
                matched = re.match(
                    r"^\s*from (?:([^.]+).*|\.([^.]+)) import",
                    item,
                )
                if not matched:
                    continue
                for group in matched.groups():
                    if group is None:
                        continue
                    final_res.add(group)
            else:
                matched = re.match(r"\s*import (.+)", item)
                if not matched:
                    continue
                tmp_string = matched.group(1)
                if " as " in tmp_string:
                    matched = re.match(r"([^.]+).* as", tmp_string)
                    if matched:
                        final_res.add(matched.group(1))
                elif "," in tmp_string:
                    string_list = tmp_string.split(",")
                    for string in string_list:
                        string = string.strip()
                        package_name = string.split(".")[0]
                        if package_name:
                            final_res.add(package_name)
                else:
                    package_name = tmp_string.split(".")[0]
                    if package_name:
                        final_res.add(package_name)
        return final_res, set(p for p in final_res if p not in self._imports)

    def project_imports(self):
        """项目目录下可导入的包、模块。"""
        project_imports = set()
        m_pattern = re.compile(r"^([0-9a-zA-Z_]+).*(?<!_d)\.py[cdw]?$")
        for root, _, files in os.walk(self._root):
            if "__init__.py" in files:
                project_imports.add(os.path.basename(root))
            for file_name in files:
                matched = m_pattern.match(file_name)
                if not matched:
                    continue
                project_imports.add(matched.group(1))
        return project_imports

# coding: utf-8

__doc__ = '包含检查项目导入模块所需的类、函数等。'

import os
import re

from chardet.universaldetector import UniversalDetector

from .libm import PyEnv


def file_encodings(project_root):
    pattern = re.compile(r'^.+\.py[w]?$')
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
            with open(file_path, 'rb') as sf:
                for line in sf:
                    encoding_detector.feed(line)
                    if encoding_detector.done:
                        break
            encoding_detector.close()
            path_encoding_groups[index] = (
                file_path,
                encoding_detector.result['encoding'],
            )
        except Exception:
            path_encoding_groups[index] = file_path, None
    return path_encoding_groups


class ImportInspector:
    pt = re.compile(r'^[^#\n]*?import [_0-9a-zA-Z .,;(]+$', re.M)

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
        pre1, pre2, pre3 = self.pt.findall(string), [], set()
        for item in pre1:
            if ';' in item:
                pre2.extend(s.strip() for s in item.split(';'))
            else:
                pre2.append(item)
        for item in pre2:
            if 'from ' in item:
                m_obj = re.match(
                    r'^\s*from (?:([^.]+).*|\.([^.]+)) import', item
                )
                if not m_obj:
                    continue
                for s in m_obj.groups():
                    if s is None:
                        continue
                    pre3.add(s)
            else:
                m_obj = re.match(r'\s*import (.+)', item)
                if not m_obj:
                    continue
                tmp_string = m_obj.group(1)
                if ' as ' in tmp_string:
                    m_obj = re.match(r'([^.]+).* as', tmp_string)
                    if not m_obj:
                        continue
                    pre3.add(m_obj.group(1))
                elif ',' in tmp_string:
                    pre3.update(s.strip() for s in tmp_string.split(','))
                else:
                    pre3.add(tmp_string)
        return pre3, set(p for p in pre3 if p not in self._imports)

    def project_imports(self):
        """项目目录下可导入的包、模块。"""
        project_imports = set()
        pt = re.compile(r'^([0-9a-zA-Z_]+).*(?<!_d)\.py[cdw]?$')
        for root, _, files in os.walk(self._root):
            if '__init__.py' in files:
                project_imports.add(os.path.basename(root))
            for file_name in files:
                m_obj = pt.match(file_name)
                if not m_obj:
                    continue
                project_imports.add(m_obj.group(1))
        return project_imports

# coding: utf-8

__doc__ = "检查项目导入的所有模块所需的类、函数等。"

import ast
import re
from os import walk
from os.path import basename, join

from chardet.universaldetector import UniversalDetector

from .libm import PyEnv


class TreeVisit(ast.NodeVisitor):
    def __init__(self, out=None):
        if isinstance(out, set):
            self.__result = out
        else:
            self.__result = set()

    def visit_ImportFrom(self, node):
        self.__result.add(self.split(node.module))
        self.generic_visit(node)

    def visit_Import(self, node):
        self.__result.update(self.split(n.name) for n in node.names)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id == "__import__":
                self.add_call_node_args0(node.args[0])
        elif isinstance(node.func, ast.Attribute):
            attr = node.func.attr
            name = node.func.value
            if isinstance(name, ast.Name) and name.id == "importlib":
                if attr == "__import__" or attr == "import_module":
                    self.add_call_node_args0(node.args[0])
        self.generic_visit(node)

    def getresult(self):
        return self.__result

    @staticmethod
    def split(string: str):
        return string.split(".", 1)[0]

    def add_call_node_args0(self, args0):
        if isinstance(args0, ast.Str):
            self.__result.add(self.split(args0.s))
        elif isinstance(args0, ast.Constant):
            self.__result.add(self.split(args0.value))


def to_be_excluded(_dirpath: str, exclude_dirs):
    _dirpath = _dirpath.lower()
    for p in exclude_dirs:
        if not p:
            continue
        if _dirpath.startswith(p.lower()):
            return True
    return False


def file_codings(project_root, exclude_dirs):
    pattern = re.compile(r"^.+\.py[w]?$")
    path_coding_groups = []
    for root, _, files in walk(project_root):
        if to_be_excluded(root, exclude_dirs):
            continue
        for name in files:
            if not pattern.match(name):
                continue
            path_coding_groups.append(join(root, name))
    coding_detector = UniversalDetector()
    for index, file_path in enumerate(path_coding_groups):
        coding_detector.reset()
        try:
            with open(file_path, "rb") as sf:
                for line in sf:
                    coding_detector.feed(line)
                    if coding_detector.done:
                        break
            coding_detector.close()
            if coding_detector.result["confidence"] < 0.9:
                coding = "utf-8"
            else:
                coding = coding_detector.result["encoding"]
            path_coding_groups[index] = (file_path, coding)
        except Exception:
            path_coding_groups[index] = file_path, None
    return path_coding_groups


class ImportInspector:
    def __init__(self, python_dir, project_root, excludes=None):
        self._root = project_root
        self._excludes = list()
        if isinstance(excludes, (list, tuple)):
            self._excludes.extend(excludes)
        self.__importables = self.__project_importables()
        self.__importables.update(PyEnv(python_dir).names_for_import())

    def __modules_tobe_imported(self, string):
        """
        查找并返回 string 中所有需要导入的模块集合
        """
        try:
            node = ast.parse(string, "<string>", "exec")
        except:
            return set()
        abstract_syntax_tree_visit = TreeVisit()
        abstract_syntax_tree_visit.visit(node)
        return abstract_syntax_tree_visit.getresult()

    def __project_importables(self):
        """项目目录下可导入的包、模块。"""
        project_imports = set()
        fnp = re.compile(r"^([0-9a-zA-Z_]+).*(?<!_d)\.py[cdw]?$")
        for root, _, files in walk(self._root):
            if to_be_excluded(root, self._excludes):
                continue
            if "__init__.py" in files:
                project_imports.add(basename(root))
            for file_name in files:
                matched = fnp.match(file_name)
                if not matched:
                    continue
                project_imports.add(matched.group(1))
        return project_imports

    def get_missing_items(self):
        """
        查找指定目录内源码所有需要导入的模块，并计算哪些模块未在指定环境中安装
        返回值类型：[(源码文件路径, {源码导入的模块}, {环境中未安装的模块})...]
        """
        results = list()
        for p, c in file_codings(self._root, self._excludes):
            if c is None:
                continue
            try:
                with open(p, encoding=c) as f:
                    file_string = f.read()
                imps = self.__modules_tobe_imported(file_string)
                results.append((p, imps, imps - self.__importables))
            except Exception:
                results.append((p, set(), set()))
        if not results:
            results.append((None, set(), set()))
        return results

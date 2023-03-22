# coding: utf-8

import os
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import *

from chardet import detect
from com import *
from fastpip import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from settings import *
from ui import *

from .messagebox import MessageBox
from .query_file_path import QueryFilePath

EMPTY_STR = ""
DEFAULT_GENERATED_DIR = "scf_packaged"


class CloudFunctionWindow(Ui_cloud_function, QMainWindow, QueryFilePath):
    REQUIRE_FILE = "requirements.txt"
    signal_packing = pyqtSignal(bool, str)
    signal_reqinstalled = pyqtSignal(int, str, bool)
    signal_show_workingtips = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.__setup_other_widgets()
        self.__config = CloudFunctionConfig()
        self.thread_repo = ThreadRepo(500)
        self.environments: Optional[List[EnvDisplayPair]] = None
        self.__previous_path = ""
        self.__requirements = list()
        self.__signal_connection()
        self.__path_ctrlgroup = (
            self.uiComboBox_preject_path,
            self.uiPushButton_clear_path,
            self.uiPushButton_select_projectdir,
        )
        self.__work_ctrlgroup = (
            self.uiTableWidget_reqirement_lines,
            self.uiPushButton_add_line,
            self.uiPushButton_delete_line,
            self.uiPushButton_start_scfpacking,
        )
        self.__checkbox_confirm_projectpath_click()

    def display(self):
        self.resize(*self.__config.window_size)
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()
        if self.thread_repo.is_empty():
            self.config_dict_to_widgets()

    def __save_window_size(self):
        if self.isMinimized() or self.isMinimized():
            return
        self.__config.window_size = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        self.__save_window_size()
        self.config_widgets_to_dict()
        self.__config.save_config()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

    def eventFilter(self, sender: QObject, event: QEvent) -> bool:
        if (
            sender == self.uiLabel_whatis_cloudfunction
            and event.type() == QEvent.MouseButtonRelease
        ):
            QDesktopServices.openUrl(
                QUrl("https://cloud.tencent.com/product/scf")
            )
            return True
        return super().eventFilter(sender, event)

    def __signal_connection(self):
        self.uiPushButton_clear_path.clicked.connect(
            self.__remove_combo_project_path
        )
        self.uiPushButton_select_projectdir.clicked.connect(
            lambda: self.__select_dirpath_settext(
                self.uiComboBox_preject_path.setCurrentText
            )
        )
        self.uiPushButton_start_scfpacking.clicked.connect(
            self.__start_cloud_function_packing
        )
        self.uiCheckBox_confirm_project_path.clicked.connect(
            self.__checkbox_confirm_projectpath_click
        )
        self.uiPushButton_add_line.clicked.connect(self.__add_requirement_line)
        self.uiPushButton_delete_line.clicked.connect(
            self.__delete_requirement_line
        )
        self.uiPushButton_save_config.clicked.connect(
            self.__save_current_configs
        )
        self.uiPushButton_delete_config.clicked.connect(
            self.__delete_selected_config
        )
        self.uiPushButton_switch_config.clicked.connect(
            self.__checkout_saved_config
        )
        self.uiRadioButton_using_projectdir.toggled.connect(
            self.__working_tmpdir_clicked
        )
        self.uiRadioButton_using_customdir.toggled.connect(
            self.__working_tmpdir_clicked
        )
        self.uiRadioButton_using_autotempdir.toggled.connect(
            self.__working_tmpdir_clicked
        )
        self.uiPushButton_select_customdir.clicked.connect(
            lambda: self.__select_dirpath_settext(
                self.uiLineEdit_customdir_path.setText
            )
        )
        self.uiPushButton_select_generateddir.clicked.connect(
            lambda: self.__select_dirpath_settext(
                self.uiLineEdit_generateddir.setText
            )
        )
        self.signal_packing.connect(self.__on_packing_completed)
        self.signal_reqinstalled.connect(self.__set_requirement_install_result)
        self.signal_show_workingtips.connect(self.uiLabel_working_tips.setText)

    def __setup_other_widgets(self):
        self.uiComboBox_python_envs.setView(QListView())
        self.uiComboBox_preject_path.setView(QListView())
        delegate = ItemDelegate(self.uiTableWidget_reqirement_lines, False)
        self.uiTableWidget_reqirement_lines.setItemDelegateForColumn(
            1, delegate
        )
        self.uiTableWidget_reqirement_lines.setItemDelegateForColumn(
            2, delegate
        )
        horiz_head = self.uiTableWidget_reqirement_lines.horizontalHeader()
        horiz_head.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        horiz_head.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.uiComboBox_preject_path.lineEdit().clear()
        self.uiLabel_whatis_cloudfunction.installEventFilter(self)
        self.__working_movie = QMovie(":/loading.gif")
        self.__working_movie.setScaledSize(QSize(16, 16))
        self.uiLabel_working_movie.setMovie(self.__working_movie)
        self.uiLabel_working_movie.hide()

    def __show_working(self):
        self.uiLabel_working_tips.clear()
        self.__working_movie.start()
        self.uiLabel_working_movie.show()

    def __hide_working(self):
        self.uiLabel_working_tips.clear()
        self.__working_movie.stop()
        self.uiLabel_working_movie.hide()

    def __load_requirements_update_table(self, is_checked: bool):
        if is_checked:
            project = self.uiComboBox_preject_path.currentText()
            requirements = os.path.join(project, self.REQUIRE_FILE)
            if not os.path.isfile(requirements):
                return
            with open(requirements, "rb") as b:
                encoding = detect(b.read())["encoding"]
            with open(requirements, "rt", encoding=encoding) as f:
                content_lines = f.readlines()
            self.uiTableWidget_reqirement_lines.clearContents()
            self.uiTableWidget_reqirement_lines.setRowCount(len(content_lines))
            for row, line in enumerate(content_lines):
                self.uiTableWidget_reqirement_lines.setItem(
                    row, 0, QTableWidgetItem(line.strip())
                )
        else:
            self.uiTableWidget_reqirement_lines.setRowCount(0)

    def __checkbox_confirm_projectpath_click(self):
        is_checked = self.uiCheckBox_confirm_project_path.isChecked()
        project = self.uiComboBox_preject_path.currentText()
        if is_checked:
            if os.path.isdir(project):
                self.__check_add_projectpath(project)
                self.uiLineEdit_generatedname.setPlaceholderText(
                    os.path.basename(project)
                )
                self.uiLineEdit_generateddir.setPlaceholderText(
                    os.path.join(project, DEFAULT_GENERATED_DIR)
                )
            else:
                MessageBox(
                    "提示",
                    "当前的项目路径不是一个有效目录路径！",
                    QMessageBox.Warning,
                ).exec_()
                self.uiCheckBox_confirm_project_path.setChecked(False)
                return
        else:
            self.uiLineEdit_generateddir.setPlaceholderText("")
            self.uiLineEdit_generatedname.setPlaceholderText("")
        for ctrl in self.__work_ctrlgroup:
            ctrl.setEnabled(is_checked)
        for ctrl in self.__path_ctrlgroup:
            ctrl.setEnabled(not is_checked)
        self.__load_requirements_update_table(is_checked)

    def __remove_combo_project_path(self):
        cur_index = self.uiComboBox_preject_path.currentIndex()
        if cur_index != -1:
            del self.__config.current.project_paths[cur_index]
            self.uiComboBox_preject_path.removeItem(cur_index)

    def __check_add_projectpath(self, project: str):
        if project and project not in self.__config.current.project_paths:
            self.uiComboBox_preject_path.addItem(project)
            self.__config.current.project_paths.append(project)

    def __environs_combobox_update(self):
        if self.uiComboBox_python_envs.count() != 0:
            return
        if not self.__config.cur_pypaths:
            return
        if self.environments:
            return
        self.environments = [
            EnvDisplayPair(PyEnv(p)) for p in self.__config.cur_pypaths
        ]
        item_number = len(self.environments)
        if not item_number:
            return
        for i, envp in enumerate(self.environments):
            self.uiComboBox_python_envs.addItem(envp.display)
            envp.signal_connect(self.uiComboBox_python_envs.setItemText, i)
            envp.load_real_display()
        current_index = self.__config.current.selected_env
        if current_index < 0 or current_index >= item_number:
            self.__config.current.selected_env = current_index = 0
        self.uiComboBox_python_envs.setCurrentIndex(current_index)

    def __project_paths_combobox_update(self):
        if self.uiComboBox_preject_path.count() != 0:
            return
        self.uiComboBox_preject_path.addItems(
            self.__config.current.project_paths
        )

    def config_widgets_to_dict(self):
        self.__config.current.selected_env = (
            self.uiComboBox_python_envs.currentIndex()
        )
        self.__config.current.overwrite_reqfile = (
            self.uiCheckBox_overwrite_requirement.isChecked()
        )
        self.__config.current.projectpath_index = (
            self.uiComboBox_preject_path.currentIndex()
        )
        if self.uiRadioButton_using_autotempdir.isChecked():
            self.__config.current.working_tmpdir = WorkDir.TmpDir
        elif self.uiRadioButton_using_projectdir.isChecked():
            self.__config.current.working_tmpdir = WorkDir.Project
        elif self.uiRadioButton_using_customdir.isChecked():
            self.__config.current.working_tmpdir = WorkDir.Custom
        else:
            self.__config.current.working_tmpdir = WorkDir.TmpDir
        self.__config.current.custom_tempdir = (
            self.uiLineEdit_customdir_path.text()
        )
        self.__config.current.generated_dir = (
            self.uiLineEdit_generateddir.text()
        )
        self.__config.current.generated_name = (
            self.uiLineEdit_generatedname.text()
        )
        self.__config.current.overwrite_samefile = (
            self.uiCheckBox_overwrite_samefile.isChecked()
        )
        self.__config.current.upgrade_requires = (
            self.uiCheckBox_upgrade_requires.isChecked()
        )

    def config_dict_to_widgets(self, config_name=None):
        self.__update_configuration_list()
        if config_name:
            self.__config.checkout_cfg(config_name)
        else:
            self.__environs_combobox_update()
        self.uiComboBox_python_envs.setCurrentIndex(
            self.__config.current.selected_env
        )
        self.__project_paths_combobox_update()
        self.uiCheckBox_overwrite_requirement.setChecked(
            self.__config.current.overwrite_reqfile
        )
        self.uiComboBox_preject_path.setCurrentIndex(
            self.__config.current.projectpath_index
        )
        working_dir = self.__config.current.working_tmpdir
        if working_dir == WorkDir.TmpDir:
            self.uiRadioButton_using_autotempdir.setChecked(True)
        elif working_dir == WorkDir.Project:
            self.uiRadioButton_using_projectdir.setChecked(True)
        elif working_dir == WorkDir.Custom:
            self.uiRadioButton_using_customdir.setChecked(True)
        else:
            self.uiRadioButton_using_autotempdir.setChecked(True)
        custom_ischecked = working_dir == WorkDir.Custom
        self.uiLineEdit_customdir_path.setEnabled(custom_ischecked)
        self.uiPushButton_select_customdir.setEnabled(custom_ischecked)
        self.uiLineEdit_customdir_path.setText(
            self.__config.current.custom_tempdir
        )
        self.uiLineEdit_generateddir.setText(
            self.__config.current.generated_dir
        )
        self.uiLineEdit_generatedname.setText(
            self.__config.current.generated_name
        )
        self.uiCheckBox_overwrite_samefile.setChecked(
            self.__config.current.overwrite_samefile
        )
        self.uiCheckBox_upgrade_requires.setChecked(
            self.__config.current.upgrade_requires
        )

    def __select_dirpath_settext(self, settextFunc: Callable[[str], None]):
        _path = self.get_dir_path(self.__config.current.previous_path)
        if not _path:
            return
        settextFunc(_path)
        self.__config.current.previous_path = _path

    def __get_table_requirement_items(self):
        self.__requirements.clear()
        for i in range(self.uiTableWidget_reqirement_lines.rowCount()):
            item = self.uiTableWidget_reqirement_lines.item(i, 0)
            if not item:
                continue
            require = item.text()
            if not require:
                continue
            self.__requirements.append(require)
        return self.__requirements

    def __on_packing_completed(self, succeeded, message):
        if succeeded:
            MessageBox(
                "打包成功",
                "云函数部署包已打包完成！",
                QMessageBox.Information,
                parent=self,
            ).exec_()
        else:
            MessageBox(
                "打包失败", message, QMessageBox.Critical, parent=self
            ).exec_()

    def __clear_requirements_result(self):
        for i in range(self.uiTableWidget_reqirement_lines.rowCount()):
            item = self.uiTableWidget_reqirement_lines.item(i, 1)
            if item:
                item.setText("")

    def __start_cloud_function_packing(self):
        self.__clear_requirements_result()
        if self.uiCheckBox_overwrite_requirement.isChecked():
            self.__overwrite_requirement_file()
        env_index = self.uiComboBox_python_envs.currentIndex()
        if env_index == -1 or not self.environments:
            MessageBox(
                "警告",
                "没有选择任何 Python 环境，请检查...",
                QMessageBox.Warning,
                parent=self,
            ).exec_()
            return
        projectdir = self.uiComboBox_preject_path.currentText()
        upgrade = self.uiCheckBox_upgrade_requires.isChecked()
        requirements = self.__get_table_requirement_items()
        environment: PyEnv = self.environments[env_index].environ
        if self.uiRadioButton_using_autotempdir.isChecked():
            workingdir_type = WorkDir.TmpDir
        elif self.uiRadioButton_using_projectdir.isChecked():
            workingdir_type = WorkDir.Project
        elif self.uiRadioButton_using_customdir.isChecked():
            workingdir_type = WorkDir.Custom
        else:
            MessageBox(
                "错误",
                "未知的工作目录选项，请反馈给开发者...",
                QMessageBox.Critical,
                parent=self,
            ).exec_()
            return
        customdir_text = self.uiLineEdit_customdir_path.text()
        generated_name = (
            self.uiLineEdit_generatedname.text()
            or self.uiLineEdit_generatedname.placeholderText()
        )
        if not generated_name:
            MessageBox(
                "错误",
                "还没有指定生成的文件名，请检查...",
                QMessageBox.Critical,
                parent=self,
            ).exec_()
            return
        generated_dir = (
            self.uiLineEdit_generateddir.text()
            or self.uiLineEdit_generateddir.placeholderText()
        )
        if not generated_dir:
            MessageBox(
                "错误",
                "还没有指定打包文件保存目录，请检查...",
                QMessageBox.Critical,
                parent=self,
            ).exec_()
            return
        generated_file = Path(generated_dir).joinpath(generated_name)
        if not generated_file.suffix.lower() == ".zip":
            generated_file = generated_file.with_suffix(".zip")
        overwrite_samefile = self.uiCheckBox_overwrite_samefile.isChecked()

        def start_scfpackaging():
            self.signal_show_workingtips.emit("开始检查打包条件...")
            if not overwrite_samefile and generated_file.exists():
                self.signal_packing.emit(
                    False, f"已存在<{generated_file}>文件且不允许覆盖..."
                )
                return
            if not os.path.exists(generated_dir):
                try:
                    os.makedirs(generated_dir, exist_ok=True)
                except PermissionError:
                    self.signal_packing.emit(False, "打包文件保存目录创建失败...")
                    return
            elif not os.path.isdir(generated_dir):
                self.signal_packing.emit(False, "打包文件保存路径不是一个目录...")
                return
            if workingdir_type == WorkDir.TmpDir:
                try:
                    working_directory = TemporaryDirectory()
                except Exception as e:
                    self.signal_packing.emit(False, f"临时工作目录创建失败：\n{e}")
                    return
                requires_install_path = working_directory.name
            elif workingdir_type == WorkDir.Custom:
                working_directory = Path(customdir_text)
                if not working_directory.exists():
                    try:
                        os.makedirs(working_directory)
                    except Exception as e:
                        self.signal_packing.emit(False, f"自定义工作目录创建失败：\n{e}")
                        return
                elif not working_directory.is_dir():
                    self.signal_packing.emit(False, "自定义工作路径不是目录...")
                    return
                requires_install_path = str(working_directory)
            elif workingdir_type == WorkDir.Project:
                working_directory = Path(projectdir)
                if not working_directory.is_dir():
                    self.signal_packing.emit(False, "作为工作目录的项目目录不可用...")
                    return
                requires_install_path = str(working_directory)
            else:
                self.signal_packing.emit(
                    False, f"未知的工作目录类型：{workingdir_type!r}"
                )
                return
            self.signal_show_workingtips.emit("开始安装项目的依赖包...")
            # 本来设计是每个包独立安装的，但是发现一起安装能节省很多时间
            # 所以就砍掉了每个依赖包安装完成就更新安装结果的功能，改为一次性更新
            _, result = environment.install(
                *requirements, target=requires_install_path, upgrade=upgrade
            )
            if not result:
                self.signal_packing.emit(False, f"一个或多个依赖包安装失败，打包中断...")
                if isinstance(working_directory, TemporaryDirectory):
                    working_directory.cleanup()
                return
            for index, name in enumerate(requirements):
                self.signal_reqinstalled.emit(index, name, result)
            self.signal_show_workingtips.emit("开始创建压缩文件...")
            compressed_arcnames: Dict[Path, Path] = dict()
            try:
                with zipfile.ZipFile(
                    generated_file, "w", zipfile.ZIP_DEFLATED
                ) as binary_file:
                    for _path in Path(projectdir).glob("**/*"):
                        if not _path.is_file():
                            continue
                        arcfilename = _path.relative_to(projectdir)
                        binary_file.write(_path, arcfilename)
                        compressed_arcnames[arcfilename] = _path
                    if workingdir_type != WorkDir.Project:
                        for _path in Path(requires_install_path).glob("**/*"):
                            if not _path.is_file():
                                continue
                            arcfilename = _path.relative_to(
                                requires_install_path
                            )
                            if arcfilename in compressed_arcnames:
                                self.signal_packing.emit(
                                    False,
                                    f"以下文件如果打包将发生覆盖，请处理：\n"
                                    f"{compressed_arcnames[arcfilename]!s}\n{_path!s}",
                                )
                                return
                            binary_file.write(_path, arcfilename)
            except Exception as e:
                self.signal_packing.emit(False, f"创建压缩文件出错：\n{e}")
                return
            finally:
                if isinstance(working_directory, TemporaryDirectory):
                    self.signal_show_workingtips.emit("正在清理临时文件夹...")
                    working_directory.cleanup()
            self.signal_packing.emit(True, EMPTY_STR)

        packaging_thread = QThreadModel(start_scfpackaging)
        packaging_thread.before_starting(
            self.__lock_critical_widgets, self.__show_working
        )
        packaging_thread.after_completion(
            self.__release_critical_widgets, self.__hide_working
        )
        packaging_thread.start()
        self.thread_repo.put(packaging_thread, 0)

    def __set_requirement_install_result(
        self, index: int, name: str, result: bool
    ):
        if index < 0 or index >= self.uiTableWidget_reqirement_lines.rowCount():
            return
        item = self.uiTableWidget_reqirement_lines.item(index, 0)
        if item is None or item.text() != name:
            return
        result_item = QTableWidgetItem("安装成功" if result else "安装失败")
        result_item.setData(
            Qt.UserRole, RoleData.Success if result else RoleData.Failed
        )
        self.uiTableWidget_reqirement_lines.setItem(index, 1, result_item)

    def __add_requirement_line(self):
        self.uiTableWidget_reqirement_lines.setRowCount(
            self.uiTableWidget_reqirement_lines.rowCount() + 1
        )

    def __delete_requirement_line(self):
        row = self.uiTableWidget_reqirement_lines.currentIndex().row()
        if row == -1:
            return
        self.uiTableWidget_reqirement_lines.removeRow(row)

    def __overwrite_requirement_file(self):
        if self.__requirements:
            try:
                with open(
                    os.path.join(
                        self.uiComboBox_preject_path.currentText(),
                        self.REQUIRE_FILE,
                    ),
                    "wt",
                    encoding="utf-8",
                ) as f:
                    for line in self.__requirements:
                        f.write(f"{line}\n")
            except Exception as e:
                MessageBox(
                    "错误",
                    f"无法重写‘{self.REQUIRE_FILE}’文件：\n{e}",
                    QMessageBox.Critical,
                    parent=self,
                ).exec_()

    def __lock_critical_widgets(self):
        self.uiPushButton_start_scfpacking.setEnabled(False)
        self.uiCheckBox_confirm_project_path.setEnabled(False)
        self.uiPushButton_add_line.setEnabled(False)
        self.uiPushButton_delete_line.setEnabled(False)
        self.uiRadioButton_using_customdir.setEnabled(False)
        self.uiRadioButton_using_autotempdir.setEnabled(False)
        self.uiRadioButton_using_projectdir.setEnabled(False)
        self.uiCheckBox_overwrite_samefile.setEnabled(False)
        self.uiLineEdit_generateddir.setEnabled(False)
        self.uiLineEdit_generatedname.setEnabled(False)
        self.uiPushButton_select_generateddir.setEnabled(False)
        self.uiCheckBox_upgrade_requires.setEnabled(False)
        self.uiCheckBox_overwrite_requirement.setEnabled(False)

    def __release_critical_widgets(self):
        self.uiPushButton_start_scfpacking.setEnabled(True)
        self.uiCheckBox_confirm_project_path.setEnabled(True)
        self.uiPushButton_add_line.setEnabled(True)
        self.uiPushButton_delete_line.setEnabled(True)
        self.uiRadioButton_using_customdir.setEnabled(True)
        self.uiRadioButton_using_autotempdir.setEnabled(True)
        self.uiRadioButton_using_projectdir.setEnabled(True)
        self.uiCheckBox_overwrite_samefile.setEnabled(True)
        self.uiLineEdit_generateddir.setEnabled(True)
        self.uiLineEdit_generatedname.setEnabled(True)
        self.uiPushButton_select_generateddir.setEnabled(True)
        self.uiCheckBox_upgrade_requires.setEnabled(True)
        self.uiCheckBox_overwrite_requirement.setEnabled(True)

    def __update_configuration_list(self, force=False):
        if force:
            self.uiListWidget_config_list.clear()
        elif self.uiListWidget_config_list.count() != 0:
            return
        self.uiListWidget_config_list.addItems(self.__config.multicfg)

    def __save_current_configs(self):
        config_name = (
            self.uiLineEdit_config_name.text()
            or self.uiLineEdit_config_name.placeholderText()
        )
        if not config_name:
            MessageBox(
                "警告",
                "还没有输入要保存的配置方案名称。",
                QMessageBox.Warning,
                parent=self,
            ).exec_()
            return
        if config_name in self.__config.multicfg:
            if (
                MessageBox(
                    "询问",
                    f"配置方案列表中已经存在名为{config_name}的配置，确定要覆盖吗？",
                    QMessageBox.Question,
                    (("accept", "确定"), ("reject", "取消")),
                    self,
                ).exec_()
                != 0
            ):
                return
        self.config_widgets_to_dict()
        self.__config.store_curcfg(config_name)
        self.__update_configuration_list(force=True)

    def __delete_selected_config(self):
        if not len(self.__config.multicfg):
            MessageBox(
                "提示",
                "没有任何已保存的配置方案。",
                QMessageBox.Information,
                parent=self,
            ).exec_()
            return
        selected_item = self.uiListWidget_config_list.currentItem()
        if not selected_item:
            return MessageBox("提示", "没有选择任何配置。").exec_()
        config_name = selected_item.text()
        if config_name not in self.__config.multicfg:
            return
        if (
            MessageBox(
                "询问",
                f"即将被删除的配置：{config_name}",
                QMessageBox.Question,
                (("accept", "确定"), ("reject", "取消")),
                self,
            ).exec_()
            != 0
        ):
            return
        del self.__config.multicfg[config_name]
        self.__update_configuration_list(force=True)

    def __checkout_saved_config(self):
        if not len(self.__config.multicfg):
            MessageBox(
                "提示",
                "没有已保存的配置。",
                QMessageBox.Information,
                parent=self,
            ).exec_()
            return
        config_item = self.uiListWidget_config_list.currentItem()
        if not config_item:
            MessageBox(
                "提示",
                "没有选择任何配置。",
                QMessageBox.Information,
                parent=self,
            ).exec_()
            return
        self.config_dict_to_widgets(config_item.text())
        self.uiListWidget_config_list.setCurrentRow(-1)

    def __working_tmpdir_clicked(self):
        ischecked = self.uiRadioButton_using_customdir.isChecked()
        self.uiLineEdit_customdir_path.setEnabled(ischecked)
        self.uiPushButton_select_customdir.setEnabled(ischecked)

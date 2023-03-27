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
from res.res import *
from settings import *
from ui import *

from .messagebox import MessageBox
from .query_file_path import QueryFilePath

DEFAULT_CUSTOM_TMPDIR = "scf_reqs"
DEFAULT_GENERATED_DIR = "scf_dist"


class CloudFunctionWindow(Ui_cloud_function, QMainWindow, QueryFilePath):
    REQUIRE_FILE = "requirements.txt"
    signal_packing = pyqtSignal(bool, str)
    signal_reqinstalled = pyqtSignal(int, str, bool)
    signal_show_workingtips = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        self.__setup_other_widgets()
        self.config = CloudFunctionConfig()
        self.thread_repo = ThreadRepo(500)
        self.environments: Optional[List[EnvDisplayPair]] = None
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
        self.__change_ctrlgroups_state(False)

    def display(self):
        self.resize(*self.config.window_size)
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()
        if self.thread_repo.is_empty():
            self.config_dict_to_widgets()

    def __save_window_size(self):
        if self.isMinimized() or self.isMinimized():
            return
        self.config.window_size = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        if not self.thread_repo.is_empty():
            MessageBox(
                "提示",
                "打包任务正在进行，关闭此窗口不会结束任务，但关闭启动窗口可能会强行结束任务！",
                QMessageBox.Warning,
                parent=self,
            ).exec_()
        self.__save_window_size()
        self.config_widgets_to_dict()
        self.config.save_config()

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
        elif (
            sender == self.uiLabel_set_excludes
            and event.type() == QEvent.MouseButtonRelease
        ):
            CloudExcludesWindow(self).display()
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
            self.__checkbox_confirm_projectpath
        )
        self.uiPushButton_add_line.clicked.connect(self.__add_requirement_line)
        self.uiPushButton_delete_line.clicked.connect(
            self.__delete_requirement_line
        )
        self.uiPushButton_save_config.clicked.connect(
            self.__save_current_configs
        )
        self.uiPushButton_del_scfconfig.clicked.connect(
            self.__delete_selected_config
        )
        self.uiPushButton_switch_config.clicked.connect(
            self.__checkout_saved_config
        )
        self.uiRadioButton_using_projectdir.clicked.connect(
            self.__workingdir_option_changed
        )
        self.uiRadioButton_using_customtemp.clicked.connect(
            self.__workingdir_option_changed
        )
        self.uiRadioButton_using_autotempdir.clicked.connect(
            self.__workingdir_option_changed
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
        self.signal_packing.connect(self.__on_scfpacking_completed)
        self.signal_reqinstalled.connect(self.__set_requirement_install_result)
        self.signal_show_workingtips.connect(self.uiLabel_working_tips.setText)
        self.uiListWidget_config_list.clicked.connect(
            self.__scfconfig_list_clicked
        )

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
        self.uiLabel_set_excludes.installEventFilter(self)
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

    def __load_requirements_update_table(self, confirm: bool):
        if confirm:
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

    def __change_ctrlgroups_state(self, confirm: bool):
        for ctrl in self.__work_ctrlgroup:
            ctrl.setEnabled(confirm)
        for ctrl in self.__path_ctrlgroup:
            ctrl.setEnabled(not confirm)

    def __checkbox_confirm_projectpath(self):
        project = self.uiComboBox_preject_path.currentText()
        confirm = self.uiCheckBox_confirm_project_path.isChecked()
        if os.path.isabs(project) and os.path.isdir(project):
            if confirm:
                self.__check_add_projectpath(project)
                self.uiLineEdit_generatedname.setPlaceholderText(
                    os.path.basename(project)
                )
                self.uiLineEdit_generateddir.setPlaceholderText(
                    os.path.join(project, DEFAULT_GENERATED_DIR)
                )
                self.uiLineEdit_customdir_path.setPlaceholderText(
                    os.path.join(project, DEFAULT_CUSTOM_TMPDIR)
                )
            else:
                self.uiLineEdit_generateddir.setPlaceholderText("")
                self.uiLineEdit_generatedname.setPlaceholderText("")
                self.uiLineEdit_customdir_path.setPlaceholderText("")
            self.__change_ctrlgroups_state(confirm)
            self.__load_requirements_update_table(confirm)
        else:
            MessageBox(
                "提示",
                "当前的项目路径不是绝对路径或者不是一个目录路径！",
                QMessageBox.Warning,
                parent=self,
            ).exec_()
            self.uiCheckBox_confirm_project_path.setChecked(False)

    def __remove_combo_project_path(self):
        cur_index = self.uiComboBox_preject_path.currentIndex()
        if cur_index != -1:
            del self.config.current.project_paths[cur_index]
            self.uiComboBox_preject_path.removeItem(cur_index)

    def __check_add_projectpath(self, project: str):
        if project and project not in self.config.current.project_paths:
            self.uiComboBox_preject_path.addItem(project)
            self.config.current.project_paths.append(project)

    def __environs_combobox_update(self):
        if self.uiComboBox_python_envs.count() != 0:
            return
        if not self.config.cur_pypaths:
            return
        if self.environments:
            return
        self.environments = [
            EnvDisplayPair(PyEnv(p)) for p in self.config.cur_pypaths
        ]
        item_number = len(self.environments)
        if not item_number:
            return
        for i, envp in enumerate(self.environments):
            self.uiComboBox_python_envs.addItem(envp.display)
            envp.signal_connect(self.uiComboBox_python_envs.setItemText, i)
            envp.load_real_display()
        current_index = self.config.current.selected_env
        if current_index < 0 or current_index >= item_number:
            self.config.current.selected_env = current_index = 0
        self.uiComboBox_python_envs.setCurrentIndex(current_index)

    def __project_paths_combobox_update(self):
        if self.uiComboBox_preject_path.count() != 0:
            return
        self.uiComboBox_preject_path.addItems(self.config.current.project_paths)

    def config_widgets_to_dict(self):
        self.config.current.selected_env = (
            self.uiComboBox_python_envs.currentIndex()
        )
        self.config.current.overwrite_reqfile = (
            self.uiCheckBox_overwrite_requirement.isChecked()
        )
        self.config.current.projectpath_index = (
            self.uiComboBox_preject_path.currentIndex()
        )
        if self.uiRadioButton_using_autotempdir.isChecked():
            self.config.current.working_tmpdir = WorkDir.TmpDir
        elif self.uiRadioButton_using_projectdir.isChecked():
            self.config.current.working_tmpdir = WorkDir.Project
        elif self.uiRadioButton_using_customtemp.isChecked():
            self.config.current.working_tmpdir = WorkDir.Custom
        else:
            self.config.current.working_tmpdir = WorkDir.TmpDir
        self.config.current.custom_tempdir = (
            self.uiLineEdit_customdir_path.text()
        )
        self.config.current.generated_dir = self.uiLineEdit_generateddir.text()
        self.config.current.generated_name = (
            self.uiLineEdit_generatedname.text()
        )
        self.config.current.overwrite_samefile = (
            self.uiCheckBox_overwrite_samefile.isChecked()
        )
        self.config.current.upgrade_requires = (
            self.uiCheckBox_upgrade_requires.isChecked()
        )

    def config_dict_to_widgets(self, config_name=None):
        self.__update_configuration_list()
        if config_name:
            self.config.checkout_cfg(config_name)
        else:
            self.__environs_combobox_update()
        self.uiComboBox_python_envs.setCurrentIndex(
            self.config.current.selected_env
        )
        self.__project_paths_combobox_update()
        self.uiCheckBox_overwrite_requirement.setChecked(
            self.config.current.overwrite_reqfile
        )
        self.uiComboBox_preject_path.setCurrentIndex(
            self.config.current.projectpath_index
        )
        working_dir = self.config.current.working_tmpdir
        self.uiRadioButton_using_projectdir.setChecked(
            working_dir == WorkDir.Project
        )
        self.uiRadioButton_using_customtemp.setChecked(
            working_dir == WorkDir.Custom
        )
        self.uiRadioButton_using_autotempdir.setChecked(
            working_dir == WorkDir.TmpDir
        )
        self.__workingdir_option_changed()
        self.uiLineEdit_customdir_path.setText(
            self.config.current.custom_tempdir
        )
        self.uiLineEdit_generateddir.setText(self.config.current.generated_dir)
        self.uiLineEdit_generatedname.setText(
            self.config.current.generated_name
        )
        self.uiCheckBox_overwrite_samefile.setChecked(
            self.config.current.overwrite_samefile
        )
        self.uiCheckBox_upgrade_requires.setChecked(
            self.config.current.upgrade_requires
        )

    def __select_dirpath_settext(self, settextFunc: Callable[[str], None]):
        _path = self.get_dir_path(self.config.current.previous_path)
        if not _path:
            return
        settextFunc(_path)
        self.config.current.previous_path = _path

    def __get_table_requirement_items(self) -> List[str]:
        requirements = list()
        for i in range(self.uiTableWidget_reqirement_lines.rowCount()):
            item = self.uiTableWidget_reqirement_lines.item(i, 0)
            if not item:
                continue
            require = item.text()
            if not require:
                continue
            requirements.append(require)
        return requirements

    def __on_scfpacking_completed(self, succeeded, message):
        if succeeded:
            MessageBox(
                "打包成功",
                "云函数部署包已打包完成！",
                QMessageBox.Information,
                parent=self,
            ).exec_()
        else:
            MessageBox(
                "打包失败",
                message or "在打包过程中出现了错误...",
                QMessageBox.Critical,
                parent=self,
            ).exec_()

    def __cleartable_requirments(self):
        for i in range(self.uiTableWidget_reqirement_lines.rowCount()):
            item = self.uiTableWidget_reqirement_lines.item(i, 1)
            if item:
                item.setText("")

    def __start_cloud_function_packing(self):
        self.__cleartable_requirments()
        env_index = self.uiComboBox_python_envs.currentIndex()
        if env_index == -1 or not self.environments:
            MessageBox(
                "警告",
                "没有选择任何 Python 环境，请检查...",
                QMessageBox.Warning,
                parent=self,
            ).exec_()
            return
        upgrade = self.uiCheckBox_upgrade_requires.isChecked()
        environment = self.environments[env_index].environ
        projectdir = self.uiComboBox_preject_path.currentText()
        if not (os.path.isabs(projectdir) and os.path.isdir(projectdir)):
            MessageBox(
                "错误",
                "项目目录路径不是绝对路径，或者路径不是一个目录路径...",
                QMessageBox.Critical,
                parent=self,
            ).exec_()
            return
        requirements = self.__get_table_requirement_items()
        if self.uiCheckBox_overwrite_requirement.isChecked():
            self.__write_requirements(projectdir, requirements)
        customtmpdir_text = (
            self.uiLineEdit_customdir_path.text()
            or self.uiLineEdit_customdir_path.placeholderText()
        )
        if self.uiRadioButton_using_autotempdir.isChecked():
            workingdir_type = WorkDir.TmpDir
        elif self.uiRadioButton_using_projectdir.isChecked():
            workingdir_type = WorkDir.Project
        elif self.uiRadioButton_using_customtemp.isChecked():
            if not customtmpdir_text:
                MessageBox(
                    "错误",
                    "没有输入自定义工作目录路径...",
                    QMessageBox.Critical,
                    parent=self,
                ).exec_()
                return
            workingdir_type = WorkDir.Custom
        else:
            MessageBox(
                "错误",
                "未知的工作目录选项，请反馈给开发者...",
                QMessageBox.Critical,
                parent=self,
            ).exec_()
            return
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
            workingdir_handle = ""
            if workingdir_type == WorkDir.TmpDir:
                try:
                    workingdir_handle = TemporaryDirectory()
                except Exception as e:
                    self.signal_packing.emit(False, f"临时工作目录创建失败：\n{e}")
                    return
                requires_install_path = workingdir_handle.name
            elif workingdir_type == WorkDir.Custom:
                if os.path.isabs(customtmpdir_text):
                    workingdir_handle = customtmpdir_text
                else:
                    workingdir_handle = os.path.join(
                        projectdir, customtmpdir_text
                    )
                if not os.path.exists(workingdir_handle):
                    try:
                        os.makedirs(workingdir_handle, exist_ok=True)
                    except Exception as e:
                        self.signal_packing.emit(False, f"自定义工作目录创建失败：\n{e}")
                        return
                elif not os.path.isdir(workingdir_handle):
                    self.signal_packing.emit(False, "自定义工作路径不是目录...")
                    return
                requires_install_path = workingdir_handle
            elif workingdir_type == WorkDir.Project:
                if not os.path.isdir(projectdir):
                    self.signal_packing.emit(False, "作为工作目录的项目目录不可用...")
                    return
                requires_install_path = projectdir
            else:
                self.signal_packing.emit(
                    False, f"未知的工作目录类型：{workingdir_type!r}"
                )
                return
            self.signal_show_workingtips.emit("开始安装项目的依赖包...")
            # 本来设计是每个包独立安装的，但是发现一起安装能节省很多时间
            # 所以就砍掉了每个依赖包安装完成就更新安装结果的功能，改为一次性更新
            if requirements:
                _, result = environment.install(
                    *requirements, target=requires_install_path, upgrade=upgrade
                )
                if not result:
                    self.signal_packing.emit(False, f"一个或多个依赖包安装失败，打包中断...")
                    if isinstance(workingdir_handle, TemporaryDirectory):
                        workingdir_handle.cleanup()
                    return
                for index, name in enumerate(requirements):
                    self.signal_reqinstalled.emit(index, name, result)
            self.signal_show_workingtips.emit("开始创建压缩文件...")
            compressed_arcnames: Dict[Path, Path] = dict()
            exclude_paths = [Path(generated_dir).resolve()]
            try:
                with zipfile.ZipFile(
                    generated_file, "w", zipfile.ZIP_DEFLATED
                ) as binary_file:
                    if workingdir_type != WorkDir.Project:
                        filtered_filepaths = self.__filtered_files(
                            Path(projectdir),
                            exclude_paths + [Path(requires_install_path)],
                        )
                    else:
                        filtered_filepaths = self.__filtered_files(
                            Path(projectdir), exclude_paths
                        )
                    for _path in filtered_filepaths:
                        arcfilename = _path.relative_to(projectdir)
                        binary_file.write(_path, arcfilename)
                        compressed_arcnames[arcfilename] = _path
                    if workingdir_type != WorkDir.Project:
                        for _path in self.__filtered_files(
                            Path(requires_install_path), exclude_paths
                        ):
                            arcfilename = _path.relative_to(
                                requires_install_path
                            )
                            if arcfilename in compressed_arcnames:
                                self.signal_packing.emit(
                                    False,
                                    f"继续打包将使以下文件将在压缩包内重复，请处理：\n"
                                    f"{compressed_arcnames[arcfilename]!s}\n{_path!s}",
                                )
                                return
                            binary_file.write(_path, arcfilename)
            except Exception as e:
                self.signal_packing.emit(False, f"创建压缩文件出错：\n{e}")
                return
            finally:
                if isinstance(workingdir_handle, TemporaryDirectory):
                    self.signal_show_workingtips.emit("正在清理临时文件夹...")
                    workingdir_handle.cleanup()
            self.signal_packing.emit(True, None)

        packaging_thread = QThreadModel(start_scfpackaging)
        packaging_thread.before_starting(
            self.__lock_critical_widgets, self.__show_working
        )
        packaging_thread.after_completion(
            self.__release_critical_widgets, self.__hide_working
        )
        packaging_thread.start()
        self.thread_repo.put(packaging_thread, 0)

    def __filtered_files(
        self, _path: Path, prev_excludeds: List[Path]
    ) -> Generator[Path, None, None]:
        previous_cwd = os.getcwd()
        try:
            os.chdir(_path)
            prev_excludeds.extend(
                Path(apath).resolve()
                for apath in self.config.current.excluded_paths
            )
            for afile in _path.rglob("*"):
                if not afile.is_file():
                    continue
                for excluded in prev_excludeds:
                    if excluded.is_file() and afile.samefile(excluded):
                        break
                    elif excluded.is_dir() and excluded in afile.parents:
                        break
                else:
                    yield afile
        finally:
            os.chdir(previous_cwd)

    def __set_requirement_install_result(
        self, index: int, name: str, res: bool
    ):
        if index < 0 or index >= self.uiTableWidget_reqirement_lines.rowCount():
            return
        item = self.uiTableWidget_reqirement_lines.item(index, 0)
        if item is None or item.text() != name:
            return
        result_item = QTableWidgetItem("安装成功" if res else "安装失败")
        result_item.setData(
            Qt.UserRole, RoleData.Success if res else RoleData.Failed
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

    def __write_requirements(self, parent, requirements):
        if not requirements:
            return
        try:
            with open(
                os.path.join(parent, self.REQUIRE_FILE),
                "wt",
                encoding="utf-8",
            ) as f:
                f.write(os.linesep.join(requirements))
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
        self.uiRadioButton_using_customtemp.setEnabled(False)
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
        self.uiRadioButton_using_customtemp.setEnabled(True)
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
        self.uiListWidget_config_list.addItems(self.config.multicfg)

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
        if config_name in self.config.multicfg:
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
        self.uiLineEdit_config_name.clear()
        self.config_widgets_to_dict()
        self.config.store_curcfg(config_name)
        self.__update_configuration_list(force=True)

    def __delete_selected_config(self):
        if not len(self.config.multicfg):
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
        if config_name not in self.config.multicfg:
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
        del self.config.multicfg[config_name]
        self.__update_configuration_list(force=True)

    def __checkout_saved_config(self):
        if not len(self.config.multicfg):
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
        MessageBox(
            "提示", "配置数据切换成功...", QMessageBox.Information, parent=self
        ).exec_()

    def __workingdir_option_changed(self):
        custom = self.uiRadioButton_using_customtemp.isChecked()
        self.uiLineEdit_customdir_path.setEnabled(custom)
        self.uiPushButton_select_customdir.setEnabled(custom)

    def __scfconfig_list_clicked(self):
        index = self.uiListWidget_config_list.currentRow()
        if index == -1:
            return
        self.uiLineEdit_config_name.setText(
            self.uiListWidget_config_list.item(index).text()
        )


class CloudExcludesWindow(Ui_cloud_excludes, QMainWindow, QueryFilePath):
    def __init__(self, parent: CloudFunctionWindow = None):
        self.__parent = parent
        super().__init__(parent)
        self.setupUi(self)
        self.__setup_widgets()
        self.uiPushButton_add_dirpath.clicked.connect(self.__add_dirpath)
        self.uiPushButton_add_filepath.clicked.connect(self.__add_filepath)
        self.uiPushButton_del_line.clicked.connect(self.__delete_line)
        self.uiPushButton_clear_items.clicked.connect(self.__clear_table_items)
        self.uiPushButton_new_line.clicked.connect(self.__add_new_line)

    def __setup_widgets(self):
        self.uiPushButton_add_dirpath.setIcon(QIcon(":/add_dir.png"))
        self.uiPushButton_add_filepath.setIcon(QIcon(":/add_file.png"))
        self.uiPushButton_new_line.setIcon(QIcon(":/new_line.png"))
        self.uiPushButton_del_line.setIcon(QIcon(":/del_line.png"))
        self.uiPushButton_clear_items.setIcon(QIcon(":/clear.png"))
        self.uiTableWidget_exclude_paths = DropableTableWidget(
            self,
            tooltip=self.uiTableWidget_exclude_paths_old.toolTip(),
        )
        self.uiTableWidget_exclude_paths.setObjectName(
            "uiTableWidget_exclude_paths"
        )
        self.horizontalLayout.replaceWidget(
            self.uiTableWidget_exclude_paths_old,
            self.uiTableWidget_exclude_paths,
        )
        self.uiTableWidget_exclude_paths_old.deleteLater()
        self.uiTableWidget_exclude_paths.setRowCount(
            len(self.__parent.config.current.excluded_paths)
        )
        for row, text in enumerate(self.__parent.config.current.excluded_paths):
            self.uiTableWidget_exclude_paths.setItem(
                row, 0, QTableWidgetItem(text)
            )

    def display(self):
        self.resize(*self.__parent.config.exc_windowsize)
        if self.isMaximized():
            self.showMaximized()
        else:
            self.showNormal()

    def __save_window_size(self):
        if self.isMinimized() or self.isMinimized():
            return
        self.__parent.config.exc_windowsize = self.width(), self.height()

    def closeEvent(self, event: QCloseEvent):
        self.__parent.config.current.excluded_paths = (
            self.uiTableWidget_exclude_paths.getItemsText()
        )
        self.__save_window_size()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Escape:
            self.close()

    def __add_filepath(self):
        paths, previous = self.get_file_paths(
            self.__parent.config.current.previous_path
        )
        if paths:
            row = self.uiTableWidget_exclude_paths.rowCount()
            self.uiTableWidget_exclude_paths.setRowCount(row + len(paths))
            for increase, _path in enumerate(paths):
                self.uiTableWidget_exclude_paths.setItem(
                    row + increase, 0, QTableWidgetItem(_path)
                )
            self.__parent.config.current.previous_path = previous

    def __add_dirpath(self):
        _path = self.get_dir_path(self.__parent.config.current.previous_path)
        if _path:
            row = self.uiTableWidget_exclude_paths.rowCount()
            self.uiTableWidget_exclude_paths.setRowCount(row + 1)
            self.uiTableWidget_exclude_paths.setItem(
                row, 0, QTableWidgetItem(_path)
            )
            self.__parent.config.current.previous_path = _path

    def __delete_line(self):
        selected_row_indexes = [
            r.row() for r in self.uiTableWidget_exclude_paths.selectedIndexes()
        ]
        if not selected_row_indexes:
            MessageBox(
                "提示", "没有选中任何项目...", QMessageBox.Information, parent=self
            ).exec_()
            return
        selected_row_indexes.sort()
        top_row = selected_row_indexes[0]
        selected_count = len(selected_row_indexes)
        for ii, row in enumerate(selected_row_indexes):
            self.uiTableWidget_exclude_paths.removeRow(row)
            for remain_i in range(ii + 1, selected_count):
                # 因为表格只有一列，行索引不会有重复的，所以这里不做进一步判断
                selected_row_indexes[remain_i] -= 1
        remain_row_count = self.uiTableWidget_exclude_paths.rowCount()
        if remain_row_count:
            if top_row >= remain_row_count:
                top_row = remain_row_count - 1
            self.uiTableWidget_exclude_paths.setRangeSelected(
                QTableWidgetSelectionRange(top_row, 0, top_row, 0), True
            )

    def __add_new_line(self):
        self.uiTableWidget_exclude_paths.setRowCount(
            self.uiTableWidget_exclude_paths.rowCount() + 1
        )

    def __clear_table_items(self):
        self.uiTableWidget_exclude_paths.setRowCount(0)

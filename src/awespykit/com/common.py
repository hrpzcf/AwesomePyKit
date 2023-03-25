# coding: utf-8

from typing import *

from fastpip import PyEnv
from PyQt5.QtCore import *

EMPTY_STR = ""


class VerInfo:
    """包装 PyInstaller 版本号的类"""

    defver = "0.0.0"

    def __init__(self, ver=defver):
        assert isinstance(ver, str)
        self.__ver = ver

    def __repr__(self):
        if not self.__ver:
            return self.defver
        return self.__ver

    __str__ = __repr__

    def is_null(self):
        return self.__ver == self.defver

    def set(self, ver: str):
        assert isinstance(ver, str)
        if ver:
            self.__ver = ver
        else:
            self.__ver = self.defver
        return self.__ver


class QThreadModel(QThread):
    def __init__(self, target, *args, **kwargs):
        super().__init__()
        self.__target = target
        self.__args = args
        self.__kwargs = kwargs
        self.__at_start = list()
        self.__at_finish = list()

    def run(self):
        self.__target(*self.__args, **self.__kwargs)

    def __repr__(self):
        return (
            f"{self.__target} with args: {self.__args}, kwargs: {self.__kwargs}"
        )

    __str__ = __repr__

    def before_starting(self, *callable_objs):
        for cab in callable_objs:
            self.started.connect(cab)
        self.__at_start.extend(callable_objs)

    def after_completion(self, *callable_objs):
        for cab in callable_objs:
            self.finished.connect(cab)
        self.__at_finish.extend(callable_objs)

    def no_signal(self):
        for cab in self.__at_start:
            self.started.disconnect(cab)
        for cab in self.__at_finish:
            self.finished.disconnect(cab)


class ThreadRepo:
    def __init__(self, interval):
        """interval: 清理已结束线程的时间间隔，单位毫秒。"""
        self._thread_repo = []
        self._timer_clths = QTimer()
        self._mutex = QMutex()
        self._timer_clths.timeout.connect(self.clean)
        self._timer_clths.start(interval)
        self._flag_cleaning = False

    def put(self, threadhandle, level=0):
        """将(线程句柄、重要等级)元组加入线程仓库。"""
        self._mutex.lock()
        self._thread_repo.append((threadhandle, level))
        self._mutex.unlock()

    def clean(self):
        """清除已结束的线程。"""
        if self._flag_cleaning:
            return
        self._mutex.lock()
        index = 0
        self._flag_cleaning = True
        while index < len(self._thread_repo):
            if self._thread_repo[index][0].isRunning():
                index += 1
                continue
            del self._thread_repo[index]
        self._flag_cleaning = False
        self._mutex.unlock()

    def stop_all(self):
        """
        按线程重要等级退出线程。
        0级：重要，安全退出；
        1级：不重要，立即退出；
        其他：未知等级，安全退出。
        """
        for thread, level in self._thread_repo:
            thread.no_signal()
            if level == 0:
                thread.quit()
            elif level == 1:
                thread.terminate()
            else:
                thread.quit()

    def kill_all(self):
        """立即终止所有线程。"""
        for thread, _ in self._thread_repo:
            thread.no_signal()
            thread.terminate()

    def is_empty(self):
        """返回线程仓库是否为空。"""
        return not self._thread_repo


class EnvDisplayPair(QObject):
    __signal_setinfo = pyqtSignal([str], [int, str])

    def __init__(self, environ: PyEnv):
        super().__init__()
        self.__environ = environ
        self.__i = None
        self.__discard = False
        self.__thread: Union[QThreadModel, None] = None
        self.__display = None
        self.__mutex = QMutex()

    def signal_connect(self, callback, index=None, clean=True):
        self.__i = index
        if clean:
            if index is None:
                if self.receivers(self.__signal_setinfo[str]):
                    self.__signal_setinfo[str].disconnect()
            else:
                if self.receivers(self.__signal_setinfo[int, str]):
                    self.__signal_setinfo[int, str].disconnect()
        if index is None:
            self.__signal_setinfo[str].connect(callback)
        else:
            self.__signal_setinfo[int, str].connect(callback)

    def disconnect_all(self):
        if self.receivers(self.__signal_setinfo[str]):
            self.__signal_setinfo[str].disconnect()
        if self.receivers(self.__signal_setinfo[int, str]):
            self.__signal_setinfo[int, str].disconnect()

    def disconnect_1(self, callback):
        self.__signal_setinfo[str].disconnect(callback)

    def disconnect_2(self, callback):
        self.__signal_setinfo[int, str].disconnect(callback)

    def discard(self):
        self.__mutex.lock()
        self.__discard = True
        if self.__thread is not None and self.__thread.isRunning():
            self.__thread.terminate()
        self.__mutex.unlock()

    def load_real_display(self):
        self.__mutex.lock()
        current_display_name = self.__display
        self.__mutex.unlock()
        if current_display_name is not None:
            return current_display_name

        def load_display_name():
            __display = str(self.__environ)
            self.__mutex.lock()
            self.__display = __display
            if not self.__discard:
                if self.__i is None:
                    self.__signal_setinfo[str].emit(__display)
                else:
                    self.__signal_setinfo[int, str].emit(self.__i, __display)
            self.__mutex.unlock()

        self.__mutex.lock()
        if not self.__discard:
            self.__thread = QThreadModel(load_display_name)
            self.__thread.start()
        self.__mutex.unlock()

    @property
    def display(self):
        self.__mutex.lock()
        __display = self.__display
        self.__mutex.unlock()
        if __display is None:
            __display = f"loading info ... @ {self.__environ.path}"
        return __display

    @property
    def env_path(self):
        return self.__environ.env_path

    @property
    def environ(self):
        return self.__environ

    @property
    def completed(self):
        return self.__display is not None

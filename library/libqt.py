# coding: utf-8

from PyQt5.QtWidgets import QLineEdit, QTextEdit


class QTextEditMod(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.paths = []
        self.setLineWrapMode(QTextEdit.NoWrap)

    def clear(self):
        super().clear()
        self.paths.clear()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.paths.extend(
            path.toLocalFile() for path in event.mimeData().urls()
        )
        self.setText('\n'.join(self.paths))


class QLineEditMod(QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.path = ''

    def clear(self):
        self.clear()
        self.path = ''

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.path = event.mimeData().urls()[0].toLocalFile()
        self.setText(self.path)

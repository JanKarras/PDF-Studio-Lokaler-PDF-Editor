from PySide6.QtCore import QObject, QRunnable, Signal


class TaskSignals(QObject):
    succeeded = Signal(object)
    failed = Signal(str)
    progress = Signal(int, int)
    finished = Signal()


class Task(QRunnable):
    def __init__(self, operation):
        super().__init__()
        self.signals = TaskSignals()
        self.operation = operation

    def run(self):
        try:
            self.signals.succeeded.emit(self.operation(self.signals.progress.emit))
        except Exception as error:
            self.signals.failed.emit(str(error))
        finally:
            self.signals.finished.emit()

from PySide6.QtWidgets import QMessageBox

from .tasks import Task


class TaskActions:
    def startTask(self, label, operation, success):
        if self.busy:
            return
        self.busy = True
        self.statusLabel.setText(label)
        self.progressBar.setRange(0, 0)
        self.progressBar.show()
        self.updateState()
        task = Task(operation)
        task.signals.progress.connect(self.taskProgress)
        task.signals.succeeded.connect(success)
        task.signals.failed.connect(self.showError)
        task.signals.finished.connect(self.taskFinished)
        self.activeTask = task
        self.workPool.start(task)

    def taskProgress(self, current, total):
        self.progressBar.setRange(0, total)
        self.progressBar.setValue(current)

    def taskFinished(self):
        self.busy = False
        self.activeTask = None
        self.progressBar.hide()
        self.updateState()
        self.scheduleThumbnails()

    def showError(self, message):
        QMessageBox.warning(self, "Aktion konnte nicht abgeschlossen werden", message)

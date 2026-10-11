from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QListWidget


class DropGrid(QListWidget):
    filesDropped = Signal(list)
    pagesMoved = Signal(list, int)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() or event.source() is self:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            super().dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            paths = [url.toLocalFile() for url in event.mimeData().urls() if url.isLocalFile()]
            self.filesDropped.emit(paths)
            event.acceptProposedAction()
        elif event.source() is self:
            target = self.itemAt(event.position().toPoint())
            destination = self.row(target) if target else self.count()
            if target and event.position().x() > self.visualItemRect(target).center().x():
                destination += 1
            ids = [item.data(Qt.ItemDataRole.UserRole) for item in self.selectedItems()]
            self.pagesMoved.emit(ids, destination)
            event.setDropAction(Qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, supportedActions):
        drag = QDrag(self)
        drag.setMimeData(self.model().mimeData(self.selectedIndexes()))
        drag.exec(Qt.DropAction.MoveAction)

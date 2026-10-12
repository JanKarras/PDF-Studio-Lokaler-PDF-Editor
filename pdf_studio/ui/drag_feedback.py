from PySide6.QtCore import QLine
from PySide6.QtGui import QColor, QPainter, QPen


class DragFeedback:
    def updateDropMarker(self, position):
        target = self.itemAt(position)
        if target is None and self.count():
            target = self.item(self.count() - 1)
            after = True
        else:
            after = bool(target and position.x() > self.visualItemRect(target).center().x())
        if target:
            rect = self.visualItemRect(target)
            edge = rect.right() + 4 if after else rect.left() - 4
            self.dropMarker = QLine(edge, rect.top(), edge, rect.bottom())
        self.viewport().update()

    def dragLeaveEvent(self, event):
        self.dropMarker = None
        self.viewport().update()
        event.accept()

    def paintDropMarker(self):
        marker = getattr(self, "dropMarker", None)
        if marker is not None:
            painter = QPainter(self.viewport())
            painter.setPen(QPen(QColor("#7fa8ff"), 3))
            painter.drawLine(marker)

from PySide6.QtCore import QRect, QSize, Qt
from PySide6.QtGui import QColor, QPainter, QFont
from PySide6.QtWidgets import QAbstractItemView

from .drop_grid import DropGrid


class PageGrid(DropGrid):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(self.ViewMode.IconMode)
        self.setMovement(self.Movement.Static)
        self.setResizeMode(self.ResizeMode.Adjust)
        self.setWrapping(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.setDragDropMode(QAbstractItemView.DragDropMode.InternalMove)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        self.setSpacing(12)
        self.setIconSize(QSize(180, 230))
        self.setGridSize(QSize(220, 318))
        self.setUniformItemSizes(True)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setWordWrap(False)
        self.setObjectName("pageGrid")

    def paintEvent(self, event):
        super().paintEvent(event)
        self.paintDropMarker()
        if not self.count():
            painter = QPainter(self.viewport())
            box = self.viewport().rect().adjusted(36, 36, -36, -36)
            painter.setPen(QColor("#40506a"))
            painter.drawRoundedRect(box, 20, 20)
            painter.setPen(QColor("#ebeff7"))
            painter.setFont(QFont("Segoe UI", 22, QFont.Weight.DemiBold))
            headingBox = QRect(box.left() + 12, box.center().y() - 95, box.width() - 24, 55)
            painter.drawText(headingBox, Qt.AlignmentFlag.AlignCenter, "Deine PDFs. Dein Arbeitsbereich.")
            painter.setFont(QFont("Segoe UI", 12))
            painter.setPen(QColor("#a9b6cb"))
            bodyBox = QRect(box.left() + 12, box.center().y() - 25, box.width() - 24, 105)
            painter.drawText(bodyBox, Qt.AlignmentFlag.AlignCenter,
                             "PDF-Dateien hier ablegen\noder mit › PDFs öffnen ‹ starten\n\nLokal bearbeiten · Sicher exportieren · Ohne Cloud")

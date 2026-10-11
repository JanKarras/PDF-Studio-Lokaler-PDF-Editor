from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap


def applicationIcon():
    canvas = QPixmap(128, 128)
    canvas.fill(Qt.GlobalColor.transparent)
    painter = QPainter(canvas)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(QColor("#1b2b46"))
    painter.drawRoundedRect(QRectF(4, 4, 120, 120), 26, 26)
    painter.setBrush(QColor("#48628a"))
    painter.drawRoundedRect(QRectF(36, 22, 62, 78), 7, 7)
    painter.setBrush(QColor("#edf3ff"))
    painter.drawRoundedRect(QRectF(24, 32, 62, 78), 7, 7)
    painter.setPen(QPen(QColor("#577cc0"), 5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
    for position, length in [(53, 31), (67, 36), (81, 24)]:
        painter.drawLine(37, position, 37 + length, position)
    painter.end()
    return QIcon(canvas)

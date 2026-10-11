from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QImage, QPixmap

from pdf_studio.core.rendering import renderPage
from .tasks import Task


class ThumbnailActions:
    def loadVisibleThumbnails(self):
        if self.closing:
            return
        visible = []
        viewport = self.grid.viewport().rect()
        for index, page in enumerate(self.history.pages):
            item = self.grid.item(index)
            if self.grid.visualItemRect(item).intersects(viewport):
                visible.append((item, page))
            elif not item.icon().isNull():
                item.setIcon(QIcon())
        width = int(self.grid.iconSize().width() * self.devicePixelRatioF())
        for item, page in visible:
            key = (page.id, page.rotation, width)
            if key in self.thumbnailCache:
                item.setIcon(self.thumbnailCache[key])
                self.thumbnailCache.move_to_end(key)
            elif key not in self.thumbnailErrors and self.thumbnailTask is None:
                task = Task(lambda progress, page=page, width=width: (key, renderPage(page, width)))
                task.signals.succeeded.connect(self.thumbnailReady)
                task.signals.failed.connect(lambda message, key=key: self.thumbnailFailed(key, message))
                task.signals.finished.connect(self.thumbnailFinished)
                self.thumbnailTask = task
                self.renderPool.start(task)
                break

    def thumbnailReady(self, result):
        key, (pixels, width, height) = result
        image = QImage(pixels, width, height, width * 3, QImage.Format.Format_RGB888).copy()
        icon = QIcon(QPixmap.fromImage(image))
        self.thumbnailCache[key] = icon
        while len(self.thumbnailCache) > 96:
            self.thumbnailCache.popitem(last=False)
        for index, page in enumerate(self.history.pages):
            if page.id == key[0] and page.rotation == key[1]:
                self.grid.item(index).setIcon(icon)
                break

    def thumbnailFailed(self, key, message):
        self.thumbnailErrors.add(key)
        for index, page in enumerate(self.history.pages):
            if page.id == key[0]:
                self.grid.item(index).setToolTip(message)
                self.grid.item(index).setText(f"Seite {index + 1}\nVorschau nicht verfügbar")
                break

    def thumbnailFinished(self):
        self.thumbnailTask = None
        self.scheduleThumbnails()

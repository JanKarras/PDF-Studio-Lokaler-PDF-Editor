from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QListWidgetItem


class ViewActions:
    def refresh(self, selectedIds=None):
        selected = set(self.selectionIds() if selectedIds is None else selectedIds)
        self.grid.blockSignals(True)
        self.grid.clear()
        for index, page in enumerate(self.history.pages):
            item = QListWidgetItem(f"Seite {index + 1}\n{page.original.name}")
            item.setSizeHint(self.grid.gridSize() - QSize(14, 14))
            item.setData(Qt.ItemDataRole.UserRole, page.id)
            item.setToolTip(f"Seite {index + 1} · {page.original.name}\nQuellseite {page.index + 1} · Drehung {page.rotation}°")
            self.grid.addItem(item)
            item.setSelected(page.id in selected)
        self.grid.blockSignals(False)
        self.updateState()
        self.scheduleThumbnails()

    def updateState(self):
        hasPages = bool(self.history.pages)
        selected = bool(self.grid.selectedItems())
        for key, action in self.actionsMap.items():
            enabled = True
            if key in ("save", "extract", "split", "select"):
                enabled = hasPages
            elif key in ("left", "right", "half", "delete"):
                enabled = selected
            elif key == "undo":
                enabled = bool(self.history.past)
                action.setToolTip("Rückgängig: " + (self.history.past[-1][1] if self.history.past else "Keine Aktion"))
            elif key == "redo":
                enabled = bool(self.history.future)
            action.setEnabled(enabled and not self.busy)
        self.grid.setEnabled(not self.busy)
        changed = self.history.pages != self.history.saved
        self.setWindowTitle(f"PDF Studio{' •' if changed else ''}")
        if not self.busy:
            self.statusLabel.setText(f"{len(self.history.pages)} Seiten · {len(self.grid.selectedItems())} ausgewählt" if hasPages
                                     else "Bereit · Alle Dateien bleiben auf deinem Gerät")

    def zoomChanged(self, value):
        self.grid.setIconSize(QSize(value, int(value * 1.28)))
        self.grid.setGridSize(QSize(value + 40, int(value * 1.28) + 88))
        for index in range(self.grid.count()):
            self.grid.item(index).setSizeHint(self.grid.gridSize() - QSize(14, 14))
        self.scheduleThumbnails()

    def scheduleThumbnails(self):
        self.thumbnailTimer.start(50)

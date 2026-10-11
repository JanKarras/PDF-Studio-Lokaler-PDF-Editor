from PySide6.QtWidgets import QMessageBox

from pdf_studio.core.operations import deletePages, movePages, rotatePages


class EditActions:
    def rotate(self, degrees):
        self.history.commit(rotatePages(self.history.pages, self.selectionIds(), degrees), "Seiten drehen")
        self.refresh()

    def deleteSelected(self):
        ids = self.selectionIds()
        if not ids:
            return
        if QMessageBox.question(self, "Seiten löschen", f"{len(ids)} Seite(n) löschen?\nDu kannst diese Aktion rückgängig machen.",
                                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return
        self.history.commit(deletePages(self.history.pages, ids), "Seiten löschen")
        self.refresh()

    def moveSelected(self, ids, destination):
        if not self.busy:
            self.history.commit(movePages(self.history.pages, ids, destination), "Seiten verschieben")
            self.refresh(ids)

    def selectionIds(self):
        from PySide6.QtCore import Qt
        return [item.data(Qt.ItemDataRole.UserRole) for item in self.grid.selectedItems()]

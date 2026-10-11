from pathlib import Path
from PySide6.QtWidgets import QFileDialog, QMessageBox

from pdf_studio.core.exporter import exportPdf, validateTarget
from pdf_studio.core.errors import StudioError


class ExportActions:
    def saveAll(self):
        self.savePages(self.history.pages, True)

    def savePages(self, pages, markSaved=False):
        if not pages or self.busy:
            return
        target, _ = QFileDialog.getSaveFileName(self, "PDF als neue Datei speichern", "PDF-Studio.pdf", "PDF-Dateien (*.pdf)")
        if not target:
            return
        if Path(target).suffix.lower() != ".pdf":
            target += ".pdf"
        overwrite = Path(target).exists()
        if overwrite and QMessageBox.question(self, "Datei ersetzen", f"{Path(target).name} existiert bereits. Ersetzen?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No) != QMessageBox.StandardButton.Yes:
            return
        try:
            validateTarget(self.history.pages, target, overwrite)
        except StudioError as error:
            self.showError(str(error))
            return
        snapshot = tuple(pages)
        self.startTask("PDF wird sicher gespeichert …", lambda progress: exportPdf(snapshot, target, overwrite, progress),
                       lambda result: self.exported(result, snapshot if markSaved else None))

    def exported(self, target, savedPages=None):
        if savedPages is not None:
            self.history.saved = savedPages
        self.updateState()
        QMessageBox.information(self, "PDF gespeichert", f"Die PDF wurde gespeichert:\n{target}")

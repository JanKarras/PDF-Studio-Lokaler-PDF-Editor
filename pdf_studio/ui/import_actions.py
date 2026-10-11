from PySide6.QtWidgets import QFileDialog, QMessageBox

from pdf_studio.core.importer import importFiles


class ImportActions:
    def openFiles(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "PDF-Dateien hinzufügen", "", "PDF-Dateien (*.pdf)")
        if paths:
            self.addFiles(paths)

    def addFiles(self, paths):
        if self.busy:
            return
        if not paths:
            return
        self.startTask("PDF-Dateien werden geladen …",
                       lambda progress: importFiles(paths, self.workspace.name, progress), self.imported)

    def imported(self, result):
        pages, errors = result
        if pages:
            self.history.commit(self.history.pages + pages, "PDFs hinzufügen")
            self.refresh([page.id for page in pages])
        if errors:
            QMessageBox.warning(self, "Nicht alle PDFs konnten geladen werden", "\n\n".join(errors))

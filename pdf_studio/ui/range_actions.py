from PySide6.QtWidgets import QFileDialog, QInputDialog, QMessageBox

from pdf_studio.core.errors import StudioError
from pdf_studio.core.ranges import parseRange, parseGroups
from pdf_studio.core.splitter import splitPlan, exportSplit


class RangeActions:
    def extract(self):
        pages = self.history.pages
        if not pages:
            return
        ids = set(self.selectionIds())
        initial = ", ".join(str(index + 1) for index, page in enumerate(pages) if page.id in ids) or "1"
        text, accepted = QInputDialog.getText(self, "Seiten extrahieren", "Seiten oder Bereiche (z. B. 1, 3, 5-9):", text=initial)
        if accepted:
            try:
                self.savePages(tuple(pages[index] for index in parseRange(text, len(pages))))
            except StudioError as error:
                self.showError(str(error))

    def split(self):
        if not self.history.pages:
            return
        options = ["Nach ausgewählter Seite", "Frei definierte Bereiche", "Jede Seite einzeln"]
        mode, accepted = QInputDialog.getItem(self, "PDF aufteilen", "Aufteilung:", options, editable=False)
        if not accepted:
            return
        try:
            groups = self.splitGroups(mode)
            if groups is None:
                return
            folder = QFileDialog.getExistingDirectory(self, "Zielordner für neue PDFs")
            if folder:
                plan = splitPlan(self.history.pages, groups, folder)
                self.startTask("PDF wird aufgeteilt …", lambda progress: exportSplit(plan, progress),
                               lambda paths: QMessageBox.information(self, "Aufteilung abgeschlossen", f"{len(paths)} PDFs gespeichert in:\n{folder}"))
        except StudioError as error:
            self.showError(str(error))

    def splitGroups(self, mode):
        pages = self.history.pages
        if mode == "Jede Seite einzeln":
            return [(index,) for index in range(len(pages))]
        if mode == "Nach ausgewählter Seite":
            ids = self.selectionIds()
            if len(ids) != 1:
                raise StudioError("Bitte genau eine Seite auswählen, nach der geteilt werden soll.")
            index = next(index for index, page in enumerate(pages) if page.id == ids[0]) + 1
            if index == len(pages):
                raise StudioError("Nach der letzten Seite gibt es keine weiteren Seiten.")
            return [tuple(range(index)), tuple(range(index, len(pages)))]
        text, accepted = QInputDialog.getText(self, "Teilbereiche", "Teilbereiche durch Semikolon trennen (z. B. 1-3; 4-6; 7,9):")
        return parseGroups(text, len(pages)) if accepted else None

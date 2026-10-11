from PySide6.QtWidgets import QMessageBox


class LifecycleActions:
    def closeEvent(self, event):
        if self.busy:
            QMessageBox.information(self, "Vorgang läuft", "Bitte warte, bis der laufende Vorgang abgeschlossen ist.")
            event.ignore()
            return
        if self.history.pages != self.history.saved:
            answer = QMessageBox.question(self, "Ungespeicherte Änderungen",
                "Es gibt nicht gespeicherte Änderungen. Arbeitsbereich wirklich schließen?",
                QMessageBox.StandardButton.Discard | QMessageBox.StandardButton.Cancel,
                QMessageBox.StandardButton.Cancel)
            if answer != QMessageBox.StandardButton.Discard:
                event.ignore()
                return
        self.closing = True
        self.thumbnailTimer.stop()
        self.renderPool.clear()
        self.renderPool.waitForDone()
        self.workPool.waitForDone()
        self.workspace.cleanup()
        event.accept()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "thumbnailTimer"):
            self.scheduleThumbnails()

    def about(self):
        QMessageBox.information(self, "Über PDF Studio",
            "PDF Studio 1.0.0\n\nPDFs lokal ordnen, drehen, zusammenfügen und aufteilen.\n"
            "Keine Telemetrie. Keine Cloud.\n\nGPL-3.0-or-later · Quellcode auf GitHub\n"
            "JanKarras/PDF-Studio-Lokaler-PDF-Editor\n\n"
            "Lizenztexte und Bibliothekshinweise befinden sich im Ordner licenses des Programmpakets.")

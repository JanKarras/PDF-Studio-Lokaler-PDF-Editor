from pathlib import Path
import pikepdf
from PySide6.QtCore import Qt, QMimeData, QPointF, QUrl
from PySide6.QtGui import QDropEvent, QDragEnterEvent
from PySide6.QtWidgets import QFileDialog, QMessageBox, QInputDialog

from conftest import waitUntil


def testFileDropImportsMultipleUnicodePaths(window, app, pdfFiles):
    mime = QMimeData()
    mime.setUrls([QUrl.fromLocalFile(str(path)) for path in pdfFiles])
    enter = QDragEnterEvent(window.grid.rect().center(), Qt.DropAction.CopyAction, mime,
                           Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
    window.grid.dragEnterEvent(enter)
    assert enter.isAccepted()
    drop = QDropEvent(QPointF(100, 100), Qt.DropAction.CopyAction, mime,
                      Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
    window.grid.dropEvent(drop)
    waitUntil(app, lambda: not window.busy)
    assert window.grid.count() == 5


def testSaveAndExtractThroughDialogs(window, app, pdfFiles, tmp_path, monkeypatch):
    window.addFiles([str(path) for path in pdfFiles])
    waitUntil(app, lambda: not window.busy)
    target = tmp_path / "UI export ä.pdf"
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args, **kwargs: (str(target), "PDF"))
    monkeypatch.setattr(QMessageBox, "information", lambda *args: QMessageBox.StandardButton.Ok)
    window.saveAll()
    waitUntil(app, lambda: not window.busy)
    assert window.history.saved == window.history.pages
    with pikepdf.open(target) as document:
        assert len(document.pages) == 5
    target = tmp_path / "UI extract.pdf"
    monkeypatch.setattr(QInputDialog, "getText", lambda *args, **kwargs: ("2, 4-5", True))
    window.extract()
    waitUntil(app, lambda: not window.busy)
    with pikepdf.open(target) as document:
        assert [str(page.obj.StudioMarker) for page in document.pages] == ["0-1", "1-0", "1-1"]


def testSplitThroughDialogs(window, app, pdfFiles, tmp_path, monkeypatch):
    window.addFiles([str(path) for path in pdfFiles])
    waitUntil(app, lambda: not window.busy)
    folder = tmp_path / "parts"
    folder.mkdir()
    monkeypatch.setattr(QInputDialog, "getItem", lambda *args, **kwargs: ("Jede Seite einzeln", True))
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", lambda *args: str(folder))
    monkeypatch.setattr(QMessageBox, "information", lambda *args: QMessageBox.StandardButton.Ok)
    window.split()
    waitUntil(app, lambda: not window.busy)
    assert len(list(folder.glob("*.pdf"))) == 5

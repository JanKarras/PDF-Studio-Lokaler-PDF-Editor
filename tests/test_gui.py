from PySide6.QtCore import Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QMessageBox

from conftest import waitUntil


def testImportSelectionRotationUndoAndRedo(window, app, pdfFiles):
    window.addFiles([str(path) for path in pdfFiles])
    waitUntil(app, lambda: not window.busy)
    assert window.grid.count() == 5
    waitUntil(app, lambda: bool(window.thumbnailCache))
    window.grid.setFocus()
    QTest.keyClick(window.grid, Qt.Key.Key_A, Qt.KeyboardModifier.ControlModifier)
    assert len(window.selectionIds()) == 5
    QTest.keyClick(window.grid, Qt.Key.Key_R, Qt.KeyboardModifier.ControlModifier)
    assert all(page.rotation == 90 for page in window.history.pages)
    QTest.keyClick(window.grid, Qt.Key.Key_Z, Qt.KeyboardModifier.ControlModifier)
    assert all(page.rotation == 0 for page in window.history.pages)
    QTest.keyClick(window.grid, Qt.Key.Key_Y, Qt.KeyboardModifier.ControlModifier)
    assert all(page.rotation == 90 for page in window.history.pages)


def testReorderDeleteAndUndoPreserveUiOrder(window, app, pdfFiles, monkeypatch):
    window.addFiles([str(path) for path in pdfFiles])
    waitUntil(app, lambda: not window.busy)
    original = window.history.pages
    ids = [original[1].id, original[3].id]
    window.grid.pagesMoved.emit(ids, 5)
    assert [window.grid.item(index).data(Qt.ItemDataRole.UserRole) for index in range(5)] == [page.id for page in window.history.pages]
    assert window.history.pages[-2:] == (original[1], original[3])
    assert set(window.selectionIds()) == set(ids)
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.StandardButton.Yes)
    window.grid.setFocus()
    QTest.keyClick(window.grid, Qt.Key.Key_Delete)
    assert window.grid.count() == 3
    window.undo()
    assert window.grid.count() == 5
    window.undo()
    assert window.history.pages == original


def testUnsavedCloseCancelAndDiscard(window, app, pdfFiles, monkeypatch):
    window.addFiles([str(pdfFiles[0])])
    waitUntil(app, lambda: not window.busy)
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.StandardButton.Cancel)
    assert not window.close()
    assert not window.closing
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.StandardButton.Discard)
    assert window.close()
    assert window.closing


def testZoomAndDisabledActions(window, app, pdfFiles):
    assert not window.actionsMap["save"].isEnabled()
    window.addFiles([str(pdfFiles[0])])
    assert not window.actionsMap["open"].isEnabled()
    waitUntil(app, lambda: not window.busy)
    window.zoomSlider.setValue(260)
    assert window.grid.iconSize().width() == 260
    app.processEvents()
    assert window.grid.visualItemRect(window.grid.item(0)).height() >= window.grid.iconSize().height() + 40
    assert window.actionsMap["save"].isEnabled()

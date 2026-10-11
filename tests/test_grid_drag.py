from types import SimpleNamespace
from PySide6.QtCore import Qt, QPointF

from conftest import waitUntil


def testInternalMultiPageDragCommitsOnceWithoutRemovingRows(window, app, pdfFiles, monkeypatch):
    from pdf_studio.ui import drop_grid
    window.addFiles([str(path) for path in pdfFiles])
    waitUntil(app, lambda: not window.busy)
    original = window.history.pages
    window.grid.clearSelection()
    window.grid.item(1).setSelected(True)
    window.grid.item(3).setSelected(True)
    target = window.grid.visualItemRect(window.grid.item(4))
    position = QPointF(target.right() - 2, target.center().y())
    mime = window.grid.model().mimeData(window.grid.selectedIndexes())
    outcomes = []
    event = SimpleNamespace(mimeData=lambda: mime, source=lambda: window.grid,
                            position=lambda: position, setDropAction=lambda action: outcomes.append(action),
                            accept=lambda: outcomes.append("accepted"), ignore=lambda: outcomes.append("ignored"))
    drag = SimpleNamespace(setMimeData=lambda data: outcomes.append("mime"),
                           exec=lambda action: window.grid.dropEvent(event))
    monkeypatch.setattr(drop_grid, "QDrag", lambda source: drag)
    window.grid.startDrag(Qt.DropAction.MoveAction)
    assert window.history.pages == (original[0], original[2], original[4], original[1], original[3])
    assert window.grid.count() == 5
    assert len(window.history.past) == 2
    assert Qt.DropAction.MoveAction in outcomes and "accepted" in outcomes
    window.undo()
    assert window.history.pages == original


def testShiftAndControlMouseSelection(window, app, pdfFiles):
    from PySide6.QtTest import QTest
    window.addFiles([str(path) for path in pdfFiles])
    waitUntil(app, lambda: not window.busy)
    window.grid.clearSelection()
    viewport = window.grid.viewport()
    QTest.mouseClick(viewport, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier,
                     window.grid.visualItemRect(window.grid.item(0)).center())
    QTest.mouseClick(viewport, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.ShiftModifier,
                     window.grid.visualItemRect(window.grid.item(2)).center())
    assert len(window.selectionIds()) == 3
    QTest.mouseClick(viewport, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.ControlModifier,
                     window.grid.visualItemRect(window.grid.item(4)).center())
    assert len(window.selectionIds()) == 4


def testMouseGestureStartsInternalPageDrag(window, app, pdfFiles, monkeypatch):
    from PySide6.QtCore import QEvent, QPoint
    from PySide6.QtGui import QMouseEvent
    from PySide6.QtTest import QTest
    from PySide6.QtWidgets import QApplication
    from pdf_studio.ui import drop_grid
    window.addFiles([str(pdfFiles[0])])
    waitUntil(app, lambda: not window.busy)
    calls = []
    drag = SimpleNamespace(setMimeData=lambda mime: calls.append("mime"), exec=lambda action: calls.append("drag"))
    monkeypatch.setattr(drop_grid, "QDrag", lambda source: drag)
    viewport = window.grid.viewport()
    origin = window.grid.visualItemRect(window.grid.item(0)).center()
    destination = origin + QPoint(40, 0)
    QTest.mousePress(viewport, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, origin)
    event = QMouseEvent(QEvent.Type.MouseMove, QPointF(destination), QPointF(viewport.mapToGlobal(destination)),
                        Qt.MouseButton.NoButton, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
    QApplication.sendEvent(viewport, event)
    QTest.mouseRelease(viewport, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, destination)
    assert "mime" in calls and "drag" in calls

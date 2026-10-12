import pytest
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QDragMoveEvent

from conftest import waitUntil


class InternalMoveEvent(QDragMoveEvent):
    def source(self):
        return self.grid


@pytest.mark.parametrize("targetIndex,after", [(0, False), (1, True), (2, True)])
def testDraggingOverPageAcceptsMoveAndMatchesDrop(window, app, pdfFiles, targetIndex, after):
    window.addFiles([str(pdfFiles[0])])
    waitUntil(app, lambda: not window.busy)
    original = window.history.pages
    sourceIndex = 2 if targetIndex == 0 else 0
    window.grid.clearSelection()
    window.grid.item(sourceIndex).setSelected(True)
    rect = window.grid.visualItemRect(window.grid.item(targetIndex))
    position = rect.center()
    position.setX(rect.right() - 2 if after else rect.left() + 2)
    mime = window.grid.model().mimeData(window.grid.selectedIndexes())
    event = InternalMoveEvent(position, Qt.DropAction.MoveAction, mime,
                              Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier)
    event.grid = window.grid
    window.grid.dragEnterEvent(event)
    window.grid.dragMoveEvent(event)
    assert event.isAccepted()
    assert event.dropAction() == Qt.DropAction.MoveAction
    assert window.grid.dropMarker is not None
    from types import SimpleNamespace
    drop = SimpleNamespace(mimeData=lambda: mime, source=lambda: window.grid,
                           position=lambda: QPointF(position), setDropAction=lambda action: None,
                           accept=lambda: None, ignore=lambda: pytest.fail("Internal drop rejected"))
    window.grid.dropEvent(drop)
    assert window.history.pages != original
    assert window.history.pages[targetIndex] == original[sourceIndex]
    assert window.grid.dropMarker is None
    window.undo()
    assert window.history.pages == original


def testLeavingGridClearsInsertionMarker(window):
    from types import SimpleNamespace
    window.grid.dropMarker = object()
    window.grid.dragLeaveEvent(SimpleNamespace(accept=lambda: None))
    assert window.grid.dropMarker is None

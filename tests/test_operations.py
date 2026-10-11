from pdf_studio.core.importer import importFiles
from pdf_studio.core.operations import movePages, rotatePages, deletePages
from pdf_studio.core.history import History


def testMoveMultiplePagesPreservesOrder(pdfFiles, tmp_path):
    pages, _ = importFiles(pdfFiles, tmp_path)
    moved = movePages(pages, [pages[1].id, pages[3].id], 5)
    assert moved == (pages[0], pages[2], pages[4], pages[1], pages[3])
    assert movePages(pages, [pages[1].id, pages[2].id], 2) == pages
    assert movePages(pages, [pages[4].id], 0)[0] == pages[4]


def testRotateAndDelete(pdfFiles, tmp_path):
    pages, _ = importFiles(pdfFiles, tmp_path)
    rotated = rotatePages(pages, [pages[0].id, pages[3].id], -90)
    assert rotated[0].rotation == rotated[3].rotation == 270
    assert rotated[1] == pages[1]
    assert rotatePages(rotated, [pages[0].id], 90)[0] == pages[0]
    assert len(deletePages(rotated, [pages[0].id, pages[4].id])) == 3


def testHistoryAcrossSourcesAndSavedState(pdfFiles, tmp_path):
    pages, _ = importFiles(pdfFiles, tmp_path)
    history = History()
    states = [pages, movePages(pages, [pages[4].id], 0)]
    states.append(rotatePages(states[-1], [pages[0].id], 180))
    states.append(deletePages(states[-1], [pages[1].id]))
    for state in states:
        history.commit(state, "test")
    history.saved = states[-1]
    for expected in list(reversed(states[:-1])) + [()]:
        history.undo()
        assert history.pages == expected
    for expected in states:
        history.redo()
        assert history.pages == expected
    assert history.pages == history.saved
    history.undo()
    history.commit(pages, "new branch")
    assert not history.future


def testNoOpDoesNotEraseRedo(pdfFiles, tmp_path):
    pages, _ = importFiles(pdfFiles, tmp_path)
    history = History()
    history.commit(pages, "add")
    history.commit(pages[:-1], "delete")
    history.undo()
    assert not history.commit(history.pages, "noop")
    assert history.future

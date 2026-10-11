import pikepdf

from pdf_studio.core.importer import importFiles
from pdf_studio.core.exporter import exportPdf
from pdf_studio.core.operations import movePages, rotatePages, deletePages
from pdf_studio.core.ranges import parseRange


def testMergeReopenAndSourceIntegrity(pdfFiles, tmp_path):
    originals = [path.read_bytes() for path in pdfFiles]
    pages, _ = importFiles(pdfFiles, tmp_path)
    target = exportPdf(pages, tmp_path / "merged.pdf")
    with pikepdf.open(target) as document:
        assert [str(page.obj.StudioMarker) for page in document.pages] == ["0-0", "0-1", "0-2", "1-0", "1-1"]
        assert [tuple(page.MediaBox)[2:] for page in document.pages] == [(240, 360), (420, 250), (300, 500), (180, 280), (600, 400)]
    assert [path.read_bytes() for path in pdfFiles] == originals


def testExportMatchesReorderDeleteAndRotate(pdfFiles, tmp_path):
    pages, _ = importFiles(pdfFiles, tmp_path)
    pages = movePages(pages, [pages[1].id, pages[4].id], 0)
    pages = rotatePages(pages, [pages[0].id, pages[1].id], 90)
    pages = deletePages(pages, [pages[3].id])
    target = exportPdf(pages, tmp_path / "edited.pdf")
    with pikepdf.open(target) as document:
        assert [str(page.obj.StudioMarker) for page in document.pages] == ["0-1", "1-1", "0-0", "1-0"]
        assert [int(page.Rotate) for page in document.pages] == [180, 180, 0, 0]


def testExtractUsesRequestedRangeOrder(pdfFiles, tmp_path):
    pages, _ = importFiles(pdfFiles, tmp_path)
    subset = tuple(pages[index] for index in parseRange("5, 1, 3", len(pages)))
    target = exportPdf(subset, tmp_path / "extract.pdf")
    with pikepdf.open(target) as document:
        assert [str(page.obj.StudioMarker) for page in document.pages] == ["1-1", "0-0", "0-2"]


def testDuplicatePageCopiesHaveIndependentRotation(pdfFiles, tmp_path):
    pages, _ = importFiles([pdfFiles[0], pdfFiles[0]], tmp_path)
    rotated = rotatePages(pages, [pages[0].id], 90)
    target = exportPdf(rotated, tmp_path / "duplicates.pdf")
    with pikepdf.open(target) as document:
        assert int(document.pages[0].Rotate) == 90
        assert int(document.pages[3].Rotate) == 0

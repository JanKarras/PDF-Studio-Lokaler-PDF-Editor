import pikepdf
import pytest

from pdf_studio.core.errors import StudioError
from pdf_studio.core.importer import importFiles
from pdf_studio.core.splitter import splitPlan, exportSplit
from pdf_studio.core.ranges import parseGroups


def testSplitByRangesAndSinglePages(pdfFiles, tmp_path):
    pages, _ = importFiles(pdfFiles, tmp_path)
    for groups in [parseGroups("1-2;3-5", 5), [(index,) for index in range(5)]]:
        folder = tmp_path / str(len(groups))
        folder.mkdir()
        results = exportSplit(splitPlan(pages, groups, folder))
        assert len(results) == len(groups)
        for target, group in zip(results, groups):
            with pikepdf.open(target) as document:
                assert len(document.pages) == len(group)
                for page, index in zip(document.pages, group):
                    with pikepdf.open(pages[index].source) as source:
                        assert page.obj.StudioMarker == source.pages[pages[index].index].obj.StudioMarker


def testExistingSplitOutputPreventsPartialWrites(pdfFiles, tmp_path):
    pages, _ = importFiles(pdfFiles, tmp_path)
    existing = tmp_path / "PDF-Studio_Seite-002.pdf"
    existing.write_bytes(b"keep")
    with pytest.raises(StudioError):
        splitPlan(pages, [(0,), (1,), (2,)], tmp_path)
    assert not (tmp_path / "PDF-Studio_Seite-001.pdf").exists()
    assert existing.read_bytes() == b"keep"


def testSplitFailureRollsBackCreatedOutputs(pdfFiles, tmp_path, monkeypatch):
    from pdf_studio.core import splitter
    pages, _ = importFiles(pdfFiles, tmp_path)
    plan = splitPlan(pages, [(0,), (1,)], tmp_path)
    originalExport = splitter.exportPdf
    def failSecond(pages, target):
        if "002" in str(target):
            raise StudioError("failed")
        return originalExport(pages, target)
    monkeypatch.setattr(splitter, "exportPdf", failSecond)
    with pytest.raises(StudioError):
        exportSplit(plan)
    assert all(not target.exists() for _, target in plan)

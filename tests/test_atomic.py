from pathlib import Path

import pikepdf
import pytest

from pdf_studio.core.errors import StudioError
from pdf_studio.core.importer import importPdf
from pdf_studio.core.exporter import exportPdf


def testConcurrentDestinationIsNotOverwritten(pdfFiles, tmp_path, monkeypatch):
    import os
    pages = importPdf(pdfFiles[0], tmp_path)
    target = tmp_path / "race.pdf"
    operation = "rename" if os.name == "nt" else "link"
    originalPublish = getattr(os, operation)
    def racePublish(source, destination):
        Path(destination).write_bytes(b"other writer")
        originalPublish(source, destination)
    monkeypatch.setattr(os, operation, racePublish)
    with pytest.raises(StudioError):
        exportPdf(pages, target)
    assert target.read_bytes() == b"other writer"
    assert not list(tmp_path.glob(".pdf-studio-*"))


def testEmptyExportRejected(tmp_path):
    with pytest.raises(StudioError, match="Keine Seiten"):
        exportPdf((), tmp_path / "empty.pdf")


@pytest.mark.skipif(__import__("os").name != "nt", reason="Windows publication uses no-clobber rename")
def testWindowsExportDoesNotRequireHardlinks(pdfFiles, tmp_path, monkeypatch):
    import os
    pages = importPdf(pdfFiles[0], tmp_path)
    monkeypatch.setattr(os, "link", lambda *args: (_ for _ in ()).throw(OSError("no hardlinks")))
    target = exportPdf(pages, tmp_path / "portable.pdf")
    with pikepdf.open(target) as document:
        assert len(document.pages) == 3

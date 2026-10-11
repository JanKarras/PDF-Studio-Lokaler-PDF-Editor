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
    originalLink = os.link
    def raceLink(source, destination):
        Path(destination).write_bytes(b"other writer")
        originalLink(source, destination)
    monkeypatch.setattr(os, "link", raceLink)
    with pytest.raises(StudioError):
        exportPdf(pages, target)
    assert target.read_bytes() == b"other writer"
    assert not list(tmp_path.glob(".pdf-studio-*"))


def testEmptyExportRejected(tmp_path):
    with pytest.raises(StudioError, match="Keine Seiten"):
        exportPdf((), tmp_path / "empty.pdf")

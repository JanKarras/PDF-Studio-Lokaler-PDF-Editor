from pathlib import Path

import pikepdf
import pytest

from pdf_studio.core.errors import StudioError
from pdf_studio.core.importer import importPdf
from pdf_studio.core.exporter import exportPdf


def testNoOverwriteOrSourceReplacement(pdfFiles, tmp_path):
    pages = importPdf(pdfFiles[0], tmp_path)
    original = pdfFiles[0].read_bytes()
    with pytest.raises(StudioError, match="Quelldateien"):
        exportPdf(pages, pdfFiles[0], overwrite=True)
    target = tmp_path / "existing.pdf"
    target.write_bytes(b"keep me")
    with pytest.raises(StudioError, match="existiert"):
        exportPdf(pages, target)
    assert target.read_bytes() == b"keep me"
    assert pdfFiles[0].read_bytes() == original
    exportPdf(pages, target, overwrite=True)
    with pikepdf.open(target) as document:
        assert len(document.pages) == 3
    assert not list(tmp_path.glob(".pdf-studio-*"))


def testFailedWritePreservesExistingFile(pdfFiles, tmp_path, monkeypatch):
    pages = importPdf(pdfFiles[0], tmp_path)
    target = tmp_path / "existing.pdf"
    target.write_bytes(b"original output")
    def failSave(self, *args, **kwargs):
        raise OSError("disk full")
    monkeypatch.setattr(pikepdf.Pdf, "save", failSave)
    with pytest.raises(StudioError, match="disk full"):
        exportPdf(pages, target, overwrite=True)
    assert target.read_bytes() == b"original output"
    assert not list(tmp_path.glob(".pdf-studio-*"))


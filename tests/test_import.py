import pikepdf
import pytest

from pdf_studio.core.errors import StudioError
from pdf_studio.core.importer import importPdf, importFiles


def testOpenUnicodeAndStableReferences(pdfFiles, tmp_path):
    pages = importPdf(pdfFiles[0], tmp_path)
    assert len(pages) == 3
    assert len({page.id for page in pages}) == 3
    assert all(page.original == pdfFiles[0] for page in pages)
    assert pages[0].source != pdfFiles[0]
    pdfFiles[0].unlink()
    with pikepdf.open(pages[0].source) as document:
        assert len(document.pages) == 3


def testInvalidAndMissingFiles(tmp_path):
    invalid = tmp_path / "invalid.pdf"
    invalid.write_bytes(b"not a pdf")
    for source in [invalid, tmp_path / "missing.pdf"]:
        with pytest.raises(StudioError, match="nicht geöffnet"):
            importPdf(source, tmp_path)
    assert list(tmp_path.glob("*.pdf")) == [invalid]


def testEncryptedFileRejected(pdfFiles, tmp_path):
    target = tmp_path / "encrypted.pdf"
    with pikepdf.open(pdfFiles[0]) as document:
        document.save(target, encryption=pikepdf.Encryption(owner="owner", user="secret"))
    with pytest.raises(StudioError, match="Passwort"):
        importPdf(target, tmp_path)


def testBatchImportPartialSuccess(pdfFiles, tmp_path):
    progress = []
    pages, errors = importFiles([pdfFiles[0], tmp_path / "missing.pdf", pdfFiles[1]], tmp_path,
                               lambda current, total: progress.append((current, total)))
    assert len(pages) == 5
    assert len(errors) == 1
    assert progress[-1] == (3, 3)

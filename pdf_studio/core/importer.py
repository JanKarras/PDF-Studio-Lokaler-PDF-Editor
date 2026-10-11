from pathlib import Path
from shutil import copyfile
from uuid import uuid4

import pikepdf

from .errors import StudioError
from .model import createPage


def importPdf(filePath, workspace):
    original = Path(filePath).resolve()
    snapshot = Path(workspace) / (uuid4().hex + ".pdf")
    try:
        copyfile(original, snapshot)
        with pikepdf.open(snapshot, attempt_recovery=False) as document:
            if document.is_encrypted:
                raise StudioError("Passwortgeschützte PDFs werden in Version 1.0 nicht unterstützt.")
            if not len(document.pages):
                raise StudioError("Die PDF-Datei enthält keine Seiten.")
            pages = tuple(createPage(snapshot, original, index) for index in range(len(document.pages)))
        return pages
    except pikepdf.PasswordError as error:
        snapshot.unlink(missing_ok=True)
        raise StudioError(f"{original.name}: Passwortgeschützte PDF wird nicht unterstützt.") from error
    except (OSError, pikepdf.PdfError, StudioError) as error:
        snapshot.unlink(missing_ok=True)
        raise StudioError(f"{original.name}: PDF konnte nicht geöffnet werden. {error}") from error


def importFiles(filePaths, workspace, progress=None):
    pages, errors = [], []
    for index, filePath in enumerate(filePaths):
        try:
            pages.extend(importPdf(filePath, workspace))
        except StudioError as error:
            errors.append(str(error))
        if progress:
            progress(index + 1, len(filePaths))
    return tuple(pages), errors

from contextlib import ExitStack
from pathlib import Path
import os
import tempfile

import pikepdf

from .errors import StudioError


def validateTarget(pages, target, overwrite=False):
    target = Path(target).resolve()
    if not pages:
        raise StudioError("Keine Seiten zum Exportieren vorhanden.")
    for page in pages:
        if target == page.original or (target.exists() and page.original.exists() and os.path.samefile(target, page.original)):
            raise StudioError("Quelldateien dürfen nicht überschrieben werden. Bitte einen neuen Dateinamen wählen.")
    if target.exists() and not overwrite:
        raise StudioError(f"Die Ausgabedatei existiert bereits: {target.name}")
    return target


def exportPdf(pages, target, overwrite=False, progress=None):
    target = validateTarget(pages, target, overwrite)
    tempPath = None
    try:
        with ExitStack() as stack:
            output = stack.enter_context(pikepdf.Pdf.new())
            sources = {}
            for index, page in enumerate(pages):
                if page.source not in sources:
                    sources[page.source] = stack.enter_context(pikepdf.open(page.source))
                output.pages.append(sources[page.source].pages[page.index])
                copied = output.pages[-1]
                copied.Rotate = (int(copied.obj.get("/Rotate", 0)) + page.rotation) % 360
                if progress:
                    progress(index + 1, len(pages))
            descriptor, tempName = tempfile.mkstemp(prefix=".pdf-studio-", suffix=".pdf", dir=target.parent)
            tempPath = Path(tempName)
            os.close(descriptor)
            output.save(tempPath)
        with pikepdf.open(tempPath) as check:
            if len(check.pages) != len(pages):
                raise StudioError("Die exportierte PDF konnte nicht verifiziert werden.")
        with tempPath.open("rb+") as stream:
            os.fsync(stream.fileno())
        if overwrite:
            os.replace(tempPath, target)
        else:
            # Hard-link publication never replaces a concurrently created destination.
            os.link(tempPath, target)
            tempPath.unlink()
        return target
    except (OSError, pikepdf.PdfError) as error:
        raise StudioError(f"PDF konnte nicht gespeichert werden: {error}") from error
    finally:
        if tempPath is not None:
            tempPath.unlink(missing_ok=True)

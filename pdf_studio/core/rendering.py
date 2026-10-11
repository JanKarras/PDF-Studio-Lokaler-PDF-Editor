import pypdfium2 as pdfium

from .errors import StudioError


def renderPage(pageRef, width=240):
    try:
        with pdfium.PdfDocument(str(pageRef.source)) as document:
            with document[pageRef.index] as page:
                pageWidth, pageHeight = page.get_size()
                effectiveWidth = pageHeight if pageRef.rotation % 180 else pageWidth
                scale = min(width / max(effectiveWidth, 1), 2.0, 1600 / max(pageWidth, pageHeight, 1))
                bitmap = page.render(scale=scale, rotation=pageRef.rotation)
                try:
                    image = bitmap.to_pil().convert("RGB")
                    return image.tobytes(), image.width, image.height
                finally:
                    bitmap.close()
    except Exception as error:
        raise StudioError(f"Vorschau konnte nicht erstellt werden: {error}") from error

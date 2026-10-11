from pdf_studio.core.importer import importPdf
from pdf_studio.core.model import rotatedPage
from pdf_studio.core.rendering import renderPage


def testRenderingHonorsOriginalAndAddedRotation(pdfFiles, tmp_path):
    pages = importPdf(pdfFiles[0], tmp_path)
    for page in pages:
        pixels, width, height = renderPage(page, 180)
        assert len(pixels) == width * height * 3
        assert len(set(pixels)) > 1, "Page content must appear in the rendered bitmap"
        _, rotatedWidth, rotatedHeight = renderPage(rotatedPage(page, 90), 180)
        assert (width > height) != (rotatedWidth > rotatedHeight)
        assert max(width, height, rotatedWidth, rotatedHeight) <= 1600

import pikepdf

from pdf_studio.core.exporter import exportPdf
from pdf_studio.core.importer import importPdf
from pdf_studio.core.operations import rotatePages


def testInheritedRotationIsPreservedAndCombined(tmp_path):
    source = tmp_path / "inherited.pdf"
    with pikepdf.Pdf.new() as document:
        document.add_blank_page(page_size=(200, 400))
        document.add_blank_page(page_size=(300, 500))
        document.Root.Pages.Rotate = 90
        document.save(source)
    pages = importPdf(source, tmp_path)
    pages = rotatePages(pages, [pages[1].id], 90)
    target = exportPdf(pages, tmp_path / "output.pdf")
    with pikepdf.open(target) as document:
        assert [int(page.Rotate) for page in document.pages] == [90, 180]
        assert tuple(document.pages[0].MediaBox) == (0, 0, 200, 400)

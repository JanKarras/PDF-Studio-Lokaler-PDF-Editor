"""Capture the real Qt application using a locally generated demo document."""
from pathlib import Path
from tempfile import TemporaryDirectory
import time

import pikepdf
from PySide6.QtWidgets import QApplication

from pdf_studio.ui.window import MainWindow


def createDemo(target):
    with pikepdf.Pdf.new() as document:
        font = document.make_indirect(pikepdf.Dictionary(Type=pikepdf.Name.Font, Subtype=pikepdf.Name.Type1,
                                                       BaseFont=pikepdf.Name.Helvetica))
        titles = ["PROJECT BRIEF", "DESIGN NOTES", "PAGE OPERATIONS", "LOCAL WORKFLOW", "REVIEW", "READY TO EXPORT"]
        for index, title in enumerate(titles):
            page = document.add_blank_page(page_size=(420, 594))
            page.Resources = pikepdf.Dictionary(Font=pikepdf.Dictionary(F1=font))
            content = f"""q 0.12 0.19 0.30 rg 0 460 420 134 re f
0.48 0.67 1 rg 28 485 42 5 re f
BT /F1 10 Tf 1 1 1 rg 28 540 Td (PDF STUDIO / DEMO) Tj ET
BT /F1 24 Tf 1 1 1 rg 28 510 Td ({title}) Tj ET
0.88 0.91 0.96 rg 28 390 364 38 re f
0.32 0.39 0.49 rg
BT /F1 13 Tf 28 404 Td (A clear workspace for every document.) Tj ET
0.86 0.89 0.93 rg 28 345 310 7 re f 28 327 350 7 re f 28 309 270 7 re f
0.94 0.96 0.98 rg 28 125 175 150 re f 215 125 175 150 re f
0.40 0.57 0.88 rg 48 148 22 {35 + index * 12} re f 80 148 22 82 re f 112 148 22 54 re f
BT /F1 11 Tf 0.32 0.39 0.49 rg 28 40 Td (Page {index + 1} / Offline. Private. Yours.) Tj ET Q"""
            page.Contents = document.make_stream(content.encode("ascii"))
        document.save(target)


def capture():
    application = QApplication([])
    application.setStyle("Fusion")
    with TemporaryDirectory() as directory:
        source = Path(directory) / "Projektmappe.pdf"
        createDemo(source)
        window = MainWindow()
        window.resize(1180, 860)
        window.show()
        application.processEvents()
        Path("docs/screenshots").mkdir(exist_ok=True)
        assert window.grab().save("docs/screenshots/empty.png")
        window.addFiles([str(source)])
        deadline = time.monotonic() + 15
        while (window.busy or len(window.thumbnailCache) < 6) and time.monotonic() < deadline:
            application.processEvents()
            time.sleep(0.01)
        assert len(window.thumbnailCache) == 6
        window.grid.clearSelection()
        window.grid.item(1).setSelected(True)
        window.grid.item(2).setSelected(True)
        application.processEvents()
        Path("docs/screenshots").mkdir(exist_ok=True)
        assert window.grab().save("docs/screenshots/workspace.png")
        window.history.saved = window.history.pages
        window.close()
        application.processEvents()


if __name__ == "__main__":
    capture()

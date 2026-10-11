import json
from pathlib import Path
from tempfile import TemporaryDirectory

import pikepdf
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from .core.exporter import exportPdf
from .core.importer import importPdf
from .core.rendering import renderPage
from .ui.window import MainWindow


def runSmoke(arguments):
    report = Path(arguments[arguments.index("--smoke-report") + 1]) if "--smoke-report" in arguments else None
    result = {"status": "failed"}
    try:
        application = QApplication(arguments)
        application.setStyle("Fusion")
        with TemporaryDirectory(prefix="pdf-studio-smoke-") as directory:
            source = Path(directory) / "Prüfung 日本語.pdf"
            with pikepdf.Pdf.new() as document:
                document.add_blank_page(page_size=(240, 360))
                document.save(source)
            pages = importPdf(source, directory)
            pixels, width, height = renderPage(pages[0])
            assert pixels and width > 0 and height > 0
            target = exportPdf(pages, Path(directory) / "export.pdf")
            with pikepdf.open(target) as document:
                assert len(document.pages) == 1
            window = MainWindow()
            window.history.commit(pages, "Smoke")
            window.history.saved = pages
            window.refresh()
            window.show()
            QTimer.singleShot(1500, window.close)
            QTimer.singleShot(10000, application.quit)
            application.exec()
            assert window.closing, "Window did not close normally"
            result = {"status": "passed", "renderSize": [width, height], "pages": 1, "gui": True}
        code = 0
    except Exception as error:
        result["error"] = str(error)
        code = 1
    if report:
        report.write_text(json.dumps(result, ensure_ascii=False), encoding="utf-8")
    return code

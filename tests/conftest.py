import os
from pathlib import Path
import time

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pikepdf
import pytest
from PySide6.QtWidgets import QApplication, QMessageBox


@pytest.fixture
def pdfFiles(tmp_path):
    files = []
    for number, sizes in enumerate([[(240, 360), (420, 250), (300, 500)], [(180, 280), (600, 400)]]):
        path = tmp_path / f"Dokument {number} ä 日本語.pdf"
        with pikepdf.Pdf.new() as document:
            for index, size in enumerate(sizes):
                page = document.add_blank_page(page_size=size)
                page.Rotate = (index * 90) % 360
                page.obj["/StudioMarker"] = f"{number}-{index}"
            document.save(path)
        files.append(path)
    return files


@pytest.fixture
def app():
    return QApplication.instance() or QApplication([])


@pytest.fixture
def window(app, monkeypatch):
    from pdf_studio.ui.window import MainWindow
    instance = MainWindow()
    instance.testErrors = []
    monkeypatch.setattr(QMessageBox, "warning", lambda *args: instance.testErrors.append(str(args[2])))
    instance.show()
    app.processEvents()
    yield instance
    instance.history.saved = instance.history.pages
    instance.close()
    app.processEvents()
    assert not instance.testErrors, instance.testErrors


def waitUntil(app, condition, timeout=10):
    deadline = time.monotonic() + timeout
    while not condition() and time.monotonic() < deadline:
        app.processEvents()
        time.sleep(0.01)
    app.processEvents()
    assert condition(), "Timed out waiting for Qt background work"

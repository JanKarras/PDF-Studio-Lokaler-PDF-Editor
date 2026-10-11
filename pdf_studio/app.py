import sys
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from .ui.window import MainWindow


def main():
    if "--smoke-test" in sys.argv:
        from .smoke import runSmoke
        return runSmoke(sys.argv)
    application = QApplication(sys.argv)
    application.setApplicationName("PDF Studio")
    application.setOrganizationName("PDF Studio")
    application.setStyle("Fusion")
    window = MainWindow()
    window.show()
    paths = [argument for argument in sys.argv[1:] if not argument.startswith("-")]
    if paths:
        QTimer.singleShot(0, lambda: window.addFiles(paths))
    return application.exec()

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QProgressBar, QSlider, QToolBar

from .actions import buildActions


def buildLayout(window):
    window.setCentralWidget(window.grid)
    buildActions(window)
    for title, keys in [("Dateien", ["open", "save", "undo", "redo"]),
                        ("Seiten", ["left", "right", "half", "delete", "extract", "split"])]:
        toolbar = QToolBar(title, window)
        toolbar.setMovable(False)
        toolbar.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        window.addToolBar(toolbar)
        for key in keys:
            toolbar.addAction(window.actionsMap[key])
        if title == "Dateien":
            window.addToolBarBreak()
    window.statusLabel = QLabel("Bereit · Alle Dateien bleiben auf deinem Gerät")
    window.statusBar().addWidget(window.statusLabel, 1)
    window.progressBar = QProgressBar()
    window.progressBar.setMaximumWidth(200)
    window.progressBar.hide()
    window.statusBar().addPermanentWidget(window.progressBar)
    window.statusBar().addPermanentWidget(QLabel("Vorschau"))
    window.zoomSlider = QSlider(Qt.Orientation.Horizontal)
    window.zoomSlider.setRange(120, 300)
    window.zoomSlider.setValue(180)
    window.zoomSlider.setFixedWidth(130)
    window.zoomSlider.setAccessibleName("Größe der Seitenvorschaubilder")
    window.zoomSlider.valueChanged.connect(window.zoomChanged)
    window.statusBar().addPermanentWidget(window.zoomSlider)

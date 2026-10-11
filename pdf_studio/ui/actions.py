from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import QStyle


def createAction(window, text, callback, shortcut=None, icon=None):
    action = QAction(text, window)
    action.triggered.connect(callback)
    if shortcut:
        action.setShortcut(QKeySequence(shortcut))
    if icon:
        action.setIcon(window.style().standardIcon(icon))
    window.addAction(action)
    return action


def buildActions(window):
    standard = QStyle.StandardPixmap
    window.actionsMap = {
        "open": createAction(window, "PDFs öffnen", window.openFiles, "Ctrl+O", standard.SP_DialogOpenButton),
        "save": createAction(window, "Speichern unter", window.saveAll, "Ctrl+S", standard.SP_DialogSaveButton),
        "undo": createAction(window, "Rückgängig", window.undo, "Ctrl+Z", standard.SP_ArrowBack),
        "redo": createAction(window, "Wiederholen", window.redo, "Ctrl+Y", standard.SP_ArrowForward),
        "left": createAction(window, "↶ 90°", lambda: window.rotate(-90), "Ctrl+L"),
        "right": createAction(window, "↷ 90°", lambda: window.rotate(90), "Ctrl+R"),
        "half": createAction(window, "180°", lambda: window.rotate(180)),
        "delete": createAction(window, "Löschen", window.deleteSelected, "Del", standard.SP_TrashIcon),
        "extract": createAction(window, "Extrahieren", window.extract, "Ctrl+E"),
        "split": createAction(window, "Aufteilen", window.split, "Ctrl+Shift+S"),
        "select": createAction(window, "Alle auswählen", window.grid.selectAll, "Ctrl+A"),
        "about": createAction(window, "Über PDF Studio", window.about),
    }
    for title, keys in [("Datei", ["open", "save", "extract", "split"]),
                        ("Bearbeiten", ["undo", "redo", "select", "left", "right", "half", "delete"]),
                        ("Hilfe", ["about"])]:
        menu = window.menuBar().addMenu(title)
        for key in keys:
            menu.addAction(window.actionsMap[key])

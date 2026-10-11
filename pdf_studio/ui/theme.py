STYLE = """
QMainWindow, QWidget { background: #131923; color: #e9eef8; font-family: 'Segoe UI'; font-size: 10pt; }
QToolBar { background: #1b2432; border: 0; spacing: 6px; padding: 8px; }
QToolButton, QPushButton { background: #29364b; border: 1px solid #3b4b63; border-radius: 6px; padding: 7px 11px; }
QToolButton:hover, QPushButton:hover { background: #374b66; border-color: #7fa8ff; }
QToolButton:disabled, QPushButton:disabled { color: #69788e; background: #1b2432; border-color: #263348; }
QListWidget { background: #131923; border: 0; padding: 10px; outline: 0; }
QListWidget::item { background: #202b3b; border: 2px solid transparent; border-radius: 9px; padding: 10px; }
QListWidget::item:hover { background: #29384e; }
QListWidget::item:selected { background: #2d456d; border-color: #88b1ff; }
QStatusBar { background: #1b2432; padding: 5px; }
QMenuBar, QMenu { background: #1b2432; }
QMenu::item:selected { background: #354b6e; }
QLineEdit, QComboBox { background: #202c3e; border: 1px solid #51617a; border-radius: 5px; padding: 7px; }
QProgressBar { border: 0; border-radius: 4px; background: #29364b; text-align: center; }
QProgressBar::chunk { background: #7fa8ff; }
QSlider::groove:horizontal { background: #344259; height: 5px; border-radius: 2px; }
QSlider::handle:horizontal { background: #8ab2ff; width: 14px; margin: -5px 0; border-radius: 7px; }
QScrollBar:vertical { background: #1b2432; width: 13px; }
QScrollBar::handle:vertical { background: #425470; min-height: 24px; border-radius: 5px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
"""

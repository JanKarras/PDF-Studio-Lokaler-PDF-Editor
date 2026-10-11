from collections import OrderedDict
from tempfile import TemporaryDirectory

from PySide6.QtCore import QThreadPool, QTimer
from PySide6.QtWidgets import QMainWindow

from pdf_studio.core.history import History
from .edits import EditActions
from .export_actions import ExportActions
from .grid import PageGrid
from .history_actions import HistoryActions
from .import_actions import ImportActions
from .layout import buildLayout
from .lifecycle import LifecycleActions
from .range_actions import RangeActions
from .task_actions import TaskActions
from .theme import STYLE
from .thumbnails import ThumbnailActions
from .view_actions import ViewActions


class MainWindow(EditActions, ExportActions, HistoryActions, ImportActions, LifecycleActions,
                 RangeActions, TaskActions, ThumbnailActions, ViewActions, QMainWindow):
    def __init__(self):
        super().__init__()
        self.workspace = TemporaryDirectory(prefix="pdf-studio-")
        self.history = History()
        self.busy = False
        self.closing = False
        self.activeTask = None
        self.thumbnailTask = None
        self.thumbnailCache = OrderedDict()
        self.thumbnailErrors = set()
        self.workPool = QThreadPool(self)
        self.workPool.setMaxThreadCount(1)
        self.renderPool = QThreadPool(self)
        self.renderPool.setMaxThreadCount(1)
        self.thumbnailTimer = QTimer(self)
        self.thumbnailTimer.setSingleShot(True)
        self.thumbnailTimer.timeout.connect(self.loadVisibleThumbnails)
        self.grid = PageGrid(self)
        self.grid.filesDropped.connect(self.addFiles)
        self.grid.pagesMoved.connect(self.moveSelected)
        self.grid.itemSelectionChanged.connect(self.updateState)
        self.grid.verticalScrollBar().valueChanged.connect(self.scheduleThumbnails)
        buildLayout(self)
        self.resize(1180, 780)
        self.setMinimumSize(640, 440)
        self.setStyleSheet(STYLE)
        self.updateState()

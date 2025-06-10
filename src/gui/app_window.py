"""Main Window for the application.

Classes:
    - ApplicationWindow: Extends QWidget.

Usage Example:
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.show()
    sys.exit(app.exec())
"""
from PyQt6.QtCore import Qt  # pylint: disable=no-name-in-module
from PyQt6.QtWidgets import (  # pylint: disable=no-name-in-module
    QGraphicsScene,
    QGraphicsView,
    QSplitter,
    QVBoxLayout,
    QWidget
)

from utils.slots import ApplicationService
from .contents_pane import ContentsPane
from .map_pane import MapPane
from .menu_bar import MenuBar


class ApplicationWindow(QWidget):
    """Main App Window. It contains the main layout, menu bar,
    and panes for map and contents."""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Infrastructure Objects Detector")
        self.setMinimumSize(1024, 768)

        self.scene_width = 1024
        self.scene_height = 768
        self.scene = QGraphicsScene(0, 0, self.scene_width, self.scene_height)

        self.map_pane = MapPane(self.scene, self)
        self.map_pane.setSceneRect(0, 0, self.scene_width, self.scene_height)
        self.map_pane.fitInView(self.scene.sceneRect(),Qt.AspectRatioMode.KeepAspectRatio)
        self.map_pane.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        self.menu_bar = MenuBar(self)
        self.contents_pane = ContentsPane(self)
        # TODO: Implement ToolsPane
        # self.tools_pane = ToolsPane(self)
        self.service = ApplicationService(self)

        # TODO: Connect Menu actions ???
        # self.menu_bar.action_save.triggered.connect(self.save)
        # self.menu_bar.action_save_as.triggered.connect(self.save_as)
        # self.menu_bar.action_enter_full_screen.triggered.connect(self.enter_full_screen)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self.contents_pane)
        splitter.addWidget(self.map_pane)
        splitter.setSizes([200, 600])

        # Set up Main layout
        layout = QVBoxLayout(self)
        layout.setMenuBar(self.menu_bar)
        layout.addWidget(splitter)
        # TODO: Add tools_pane widget once implemented
        # layout.addWidget(self.tools_pane)
        self.setLayout(layout)

        # SLOTS
        self.contents_pane.add_image_button.clicked.connect(self.service.add_image)
        self.contents_pane.detect_objects_button.clicked.connect(self.service.detect)
        self.contents_pane.up_button.clicked.connect(self.service.up)
        self.contents_pane.down_button.clicked.connect(self.service.down)
        self.contents_pane.delete_button.clicked.connect(self.service.delete_layer)
        self.contents_pane.reset_button.clicked.connect(self.map_pane.reset_zoom)
        self.contents_pane.layer_list.currentItemChanged.connect(self.service.select_item)

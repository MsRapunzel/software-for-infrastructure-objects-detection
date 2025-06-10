"""Main Application Window for the GUI."""

from PyQt6.QtGui import QAction # pylint: disable=no-name-in-module
from PyQt6.QtWidgets import QMenuBar, QMenu # pylint: disable=no-name-in-module

# from utils.slots import ApplicationService


class MenuBar(QMenuBar):
    """Menu bar contains file and window menus."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.menu_file = QMenu("File", self)
        self.menu_window = QMenu("Window", self)

        self.action_save = QAction("Save", self)
        self.action_save_as = QAction("Save as...", self)
        self.action_enter_full_screen = QAction("Enter Full Screen", self)

        # TODO: Connect actions to slots
        # self.menu_file.addAction(ApplicationService.action_save)
        # self.menu_file.addAction(ApplicationService.action_save_as)
        # self.menu_window.addAction(ApplicationService.action_enter_full_screen)

        self.addMenu(self.menu_file)
        self.addMenu(self.menu_window)

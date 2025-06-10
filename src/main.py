"""Entrypoint of App"""
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication # pylint: disable=no-name-in-module

from gui import ApplicationWindow
from object_detection import label_func # pylint: disable=unused-import

def run():
    """Run the application."""
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    # window.setWindowIcon(QIcon("resources/icons/app_icon.icns"))
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()

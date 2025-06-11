"""Entrypoint of App"""
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from gui import ApplicationWindow
from object_detection import label_func


def run():
    """Run the application."""
    app = QApplication(sys.argv)
    window = ApplicationWindow()
    window.setWindowIcon(QIcon("resources/icons/app_icon.icns"))
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()

"""Entrypoint of App"""
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from gui import ApplicationWindow
from object_detection import label_func
from utils.logger_config import logger, cleanup


def run():
    """Run the application."""
    try:
        app = QApplication(sys.argv)
        window = ApplicationWindow()
        icon_path = "resources/icons/app_icon.icns"
        window.setWindowIcon(QIcon(icon_path))
        window.show()

        app.aboutToQuit.connect(cleanup)
        logger.info("Application started successfully.")
        sys.exit(app.exec())

    except Exception as e:
        logger.exception("Application failed to start: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    run()

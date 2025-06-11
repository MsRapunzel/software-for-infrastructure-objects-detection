"""
Contents pane for the application.
Contains control buttons and a list of layers.

Classes:
    - ContentsPane: Extends QWidget.

Usage Example:
    contents_pane = ContentsPane()
    conents_pane.show()
"""
from PyQt6.QtWidgets import (
    QListWidget,
    QPushButton,
    QProgressBar,
    QVBoxLayout,
    QWidget
)


class ContentsPane(QWidget):
    """Class that provides a pane for controlling the layers on the map."""
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)

        self.add_image_button = QPushButton("Add Image")
        layout.addWidget(self.add_image_button)

        self.detect_objects_button = QPushButton("Detect Objects")
        layout.addWidget(self.detect_objects_button)

        self.up_button = QPushButton("Up")
        layout.addWidget(self.up_button)

        self.down_button = QPushButton("Down")
        layout.addWidget(self.down_button)

        self.delete_button = QPushButton("Delete Layer")
        layout.addWidget(self.delete_button)

        self.reset_button = QPushButton("Reset Zoom")
        layout.addWidget(self.reset_button)

        self.layer_list = QListWidget()
        layout.addWidget(self.layer_list)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        # Note: QMacStyle never draws the text. Read more at:
        # https://doc.qt.io/qt-6/qprogressbar.html#textVisible-prop
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("Progress: %p")
        layout.addWidget(self.progress_bar)

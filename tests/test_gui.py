from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGraphicsPixmapItem,
    QListWidgetItem,
    QFileDialog,
)
import pytest

from gui import ApplicationWindow  # type: ignore
from utils.helpers import get_resource_path, compute_zoom  # type: ignore


@pytest.fixture
def app_window(qtbot):
    window = ApplicationWindow()
    qtbot.addWidget(window)
    return window


def test_window_title(app_window):
    """Test that window title is set correctly."""
    assert app_window.windowTitle() == "Infrastructure Objects Detector"


def test_window_minimum_size(app_window):
    """Test minimum window size requirements."""
    min_size = app_window.minimumSize()
    assert min_size.width() == 1024
    assert min_size.height() == 768


def test_scene_initialization(app_window):
    """Test that graphics scene is initialized with correct dimensions."""
    scene = app_window.scene
    assert scene.width() == 1024
    assert scene.height() == 768


def test_compute_zoom():
    """Test zoom computation function."""
    zoom_factor, zoom_in = compute_zoom(120, 0)
    assert zoom_factor == 1.25
    assert zoom_in == 1

    zoom_factor, zoom_out = compute_zoom(-120, 0)
    assert zoom_factor == 0.8
    assert zoom_out == -1

    zoom_factor, zoom_limit = compute_zoom(120, 20)
    assert zoom_factor is None
    assert zoom_limit == 20


def test_add_image(app_window, qtbot):
    """Test adding an image layer."""
    image_path = str(Path(get_resource_path("resources/demo_images/0_image.tif")))

    def mock_get_open_filename(*args, **kwargs):
        return image_path, "Images (*.png *.jpg *.tif)"

    original_dialog = QFileDialog.getOpenFileName
    QFileDialog.getOpenFileName = mock_get_open_filename

    qtbot.mouseClick(app_window.contents_pane.add_image_button, Qt.MouseButton.LeftButton)

    assert len(app_window.scene.items()) == 1
    assert isinstance(app_window.scene.items()[0], QGraphicsPixmapItem)
    assert app_window.contents_pane.layer_list.count() == 1

    QFileDialog.getOpenFileName = original_dialog


def test_layer_controls(app_window, qtbot):
    """Test layer control buttons."""
    item = QGraphicsPixmapItem()
    app_window.scene.addItem(item)
    list_item = QListWidgetItem("Test Layer")
    list_item.setData(Qt.ItemDataRole.UserRole, {"item": item})
    app_window.contents_pane.layer_list.addItem(list_item)

    app_window.contents_pane.layer_list.setCurrentRow(0)

    qtbot.mouseClick(app_window.contents_pane.delete_button, Qt.MouseButton.LeftButton)

    assert len(app_window.scene.items()) == 0
    assert app_window.contents_pane.layer_list.count() == 0

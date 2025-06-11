"""This module contains helper functions for the application.
It includes functions to manage graphics items, reorder layers, and display dialog boxes."""
import os
from operator import itemgetter
from pathlib import Path
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QGraphicsPixmapItem,
    QGraphicsPolygonItem,
    QListWidgetItem,
    QMessageBox,
)

def unwrap_item(data: dict) -> QGraphicsPixmapItem | QGraphicsPolygonItem:
    """
    Helper function.

    :returns: QGraphics item representation
    :rtype: :class:`QGraphicsPixmapItem` or :class:`QGraphicsItemGroup`
    """
    if isinstance(data, dict):
        item = data.get("item")
    else:
        item = data
    return item

def get_next_z(self) -> int:
    """
    Determine the next highest Z-value to assign a new graphics item.

    Returns:
        int: One greater than the current maximum Z-value in the scene.
    """
    return max((i.zValue() for i in self.scene.items()), default=-1) + 1

def reorder_list_by_z(layer_list):
    """
    Reorders the layer list to match the Z-order of items in the scene.
    """
    # Extract all items with their graphics items and labels
    items_data = []
    for i in range(layer_list.count()):
        list_item = layer_list.item(i)
        data = list_item.data(Qt.ItemDataRole.UserRole)
        graphics_item = unwrap_item(data)
        if data:
            items_data.append(
                (graphics_item.zValue(), list_item.text(), list_item, data)
            )

    # Sort in descending z-value order (topmost first)
    items_data.sort(reverse=True, key=itemgetter(0))

    # Assign new z-values: topmost gets highest z, bottommost gets 0
    for new_z, (_, _, list_item, data) in enumerate(reversed(items_data)):
        if isinstance(data, dict):
            data["item"].setZValue(new_z)
        else:
            data.setZValue(new_z)

    # Sort again with updated z-values
    items_data.sort(
        reverse=True,
        key=lambda t: (
            t[2].data(Qt.ItemDataRole.UserRole)["item"].zValue()
            if isinstance(t[3], dict)
            else t[2].data(Qt.ItemDataRole.UserRole).zValue()
        ),
    )

    # Rebuild the QListWidget to match new z-value order
    layer_list.clear()
    for _, label, _, data in items_data:
        new_item = QListWidgetItem(label)
        new_item.setData(Qt.ItemDataRole.UserRole, data)
        layer_list.addItem(new_item)

def show_dialog_box(
    self,
    window_title="None",
    text="None",
    button=QMessageBox.StandardButton.Ok,
    icon=QMessageBox.Icon.NoIcon,
):
    """
    Display a custom message box to the user.

    Args:
        window_title (str): Title of the dialog window.
        text (str): Main message text.
        button (QMessageBox.StandardButton): Button type (e.g., Ok, Cancel).
        icon (QMessageBox.Icon): Icon to display in the message box.
    """
    dlg = QMessageBox(self)
    dlg.setWindowTitle(window_title)
    dlg.setText(text)
    dlg.StandardButton(button)
    dlg.setIcon(icon)
    button = dlg.exec()
    # Look up the button enum entry for the result.
    # button = QMessageBox.StandardButton(button)
    # if button == QMessageBox.StandardButton.Yes:
    #     print("Yes!")
    # else:
    #     print("No!")

def get_image_path(layer_list) -> Path | None:
    """
    Retrieve the file path of the currently selected image layer.

    Returns:
        :class:`str` or `None`: The file path if available, otherwise `None`.
    """
    current = layer_list.currentItem()
    if current:
        data = current.data(Qt.ItemDataRole.UserRole)
        try:
            file_path = data.get("file_path")
        except AttributeError:
            print("AttributeError: Impossible to detect object on polygon layer.")
            return None
        return file_path
    return None

def get_image_item(layer_list):
    """
    Retrieve the currently displayed image item from the layer list.

    This function iterates through the items in the provided QListWidget,
    checks if the item's data (specifically, the 'layer_type' under the UserRole)
    indicates that the item is an image, and returns the associated QGraphicsPixmapItem.

    Args:
    layer_list (QListWidget): The QListWidget containing the layers.

    Returns:
    QGraphicsPixmapItem or None: The QGraphicsPixmapItem if found, otherwise None.
    """
    for i in range(layer_list.count()):
        item = layer_list.item(i)
        layer_data = item.data(Qt.ItemDataRole.UserRole)
        if layer_data and layer_data.get("layer_type") == "image":
            return layer_data["item"]
    return None

def compute_zoom(event_delta_y: int, current_zoom: int, min_zoom=-10, max_zoom=20):
    zoom_in_factor = 1.25
    zoom_out_factor = 1 / zoom_in_factor

    if event_delta_y > 0:
        zoom_factor = zoom_in_factor
        new_zoom = current_zoom + 1
    else:
        zoom_factor = zoom_out_factor
        new_zoom = current_zoom - 1

    if new_zoom < min_zoom or new_zoom > max_zoom:
        return None, current_zoom

    return zoom_factor, new_zoom

def get_resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    
    Args:
        relative_path (str): The path relative to the application root
        
    Returns:
        str: The absolute path to the resource
    """
    if getattr(sys, 'frozen', False):
        # Running in a bundle
        base_path = sys._MEIPASS
    else:
        # Running in normal Python environment
        base_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    return os.path.join(base_path, relative_path)

def get_file(self, initial_dir, filters):
    # initial_dir = get_resource_path(resource_path)
    # filters = "Images (*.png *.jpg *.jpeg *.tif *.tiff);; All files (*.*)"
    file_path, _ = QFileDialog.getOpenFileName(
        self, 
        caption="Open File", 
        directory=initial_dir,
        filter=filters
    )

    if not file_path:
        show_dialog_box(
            self.parent,
            window_title="Warning",
            text="File could not be opened. Please, try again.",
            button=QMessageBox.StandardButton.Discard,
            icon=QMessageBox.Icon.Critical,
        )
        return
    return file_path
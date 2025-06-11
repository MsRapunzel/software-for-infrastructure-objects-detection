import os
from random import random
from typing import Optional

from PyQt6.QtWidgets import (
    QFileDialog,
    QGraphicsItemGroup,
    QGraphicsPixmapItem,
    QGraphicsPolygonItem,
    QListWidgetItem,
    QMessageBox,
    QWidget,
)
from PyQt6.QtGui import QAction, QColor, QPen, QPixmap, QPolygonF
from PyQt6.QtCore import QPointF, Qt

from . import helpers as hp
from object_detection.object_detection import label_func, get_model, predict_polygons


class ApplicationService:
    def __init__(self, parent_widget: Optional[QWidget] = None):
        self.parent = parent_widget

        self.scene = parent_widget.scene
        self.layer_list = parent_widget.contents_pane.layer_list
        self.view = parent_widget.map_pane
        self.scene_width = parent_widget.scene_width
        self.scene_height = parent_widget.scene_height

    def add_image(self):
        """Slot. Select an image from a file dialog and add it to the `QGraphicsScene`."""
        initial_dir = hp.get_resource_path("resources/demo_images")
        filters = "Images (*.png *.jpg *.jpeg *.tif *.tiff);; All files (*.*)"
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            caption="Open Image",
            directory=initial_dir,
            filter=filters
        )

        if not file_path:
            hp.show_dialog_box(
                self.parent,
                window_title="Warning",
                text="Image could not be opened. Please, try again.",
                button=QMessageBox.StandardButton.Discard,
                icon=QMessageBox.Icon.Critical,
            )
            return

        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            return

        scaled_pixmap = pixmap.scaled(
            self.scene_width,
            self.scene_height,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        graphics_pixmap = QGraphicsPixmapItem(scaled_pixmap)
        graphics_pixmap.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        graphics_pixmap.setPos(
            (self.scene_width - scaled_pixmap.width()) / 2,
            (self.scene_height - scaled_pixmap.height()) / 2,
        )

        graphics_pixmap.setZValue(hp.get_next_z(self.parent))
        graphics_pixmap.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable)
        self.scene.addItem(graphics_pixmap)

        list_item = QListWidgetItem(f"Image: {os.path.basename(file_path)}")
        layer_metadata = {
            "item": graphics_pixmap,
            "file_path": file_path,
            "layer_type": "image",
            "extra": {},
        }
        list_item.setData(Qt.ItemDataRole.UserRole, layer_metadata)
        self.layer_list.addItem(list_item)
        hp.reorder_list_by_z(self.layer_list)
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

    def add_polygon_layer(self, polygons_data):
        """
        Display the specified annotations, scaling them to match the current image size.
        :param anns (array of object): annotations to display
        :return: None
        Add a polygon layer from a list of flat coordinate lists.
        :param polygons_data: List of polygons, where each is [x1, y1, x2, y2, ...]
        Adapted from pycocotools coco.py line 228 (.showAnns(self, anns)).
        """
        image_item = hp.get_image_item(self.layer_list)
        if not image_item:
            hp.show_dialog_box(
                self.parent,
                window_title="Warning",
                text="No image found. Please add an image first.",
                button=QMessageBox.StandardButton.Discard,
                icon=QMessageBox.Icon.Critical,
            )
            return

        image_width = image_item.pixmap().width()
        image_height = image_item.pixmap().height()

        items = []

        for coords in polygons_data:
            if len(coords) < 6:
                continue

            points = [QPointF(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
            polygon_item = QGraphicsPolygonItem(QPolygonF(points))

            r, g, b = [int((random() * 0.6 + 0.4) * 255) for _ in range(3)]
            polygon_item.setBrush(Qt.GlobalColor.transparent)
            polygon_item.setPen(QPen(QColor(r, g, b), 2))
            polygon_item.setBrush(QColor(r, g, b, int(0.4 * 255)))

            items.append(polygon_item)

        if not items:
            return

        group = self.scene.createItemGroup(items)
        next_z = max((i.zValue() for i in self.scene.items()), default=-1) + 1
        group.setZValue(next_z)

        rect = group.boundingRect()

        scale_x = image_width / rect.width()
        scale_y = image_height / rect.height()

        scale = min(scale_x, scale_y)

        group.setScale(scale)

        image_x = image_item.x()
        image_y = image_item.y()

        group.setPos(image_x, image_y)

        group.setAcceptedMouseButtons(Qt.MouseButton.NoButton)
        group.setFlag(QGraphicsItemGroup.GraphicsItemFlag.ItemIsSelectable)

        list_item = QListWidgetItem("Polygons Layer")
        layer_metadata = {
            "item": group,
            "layer_type": "polygon",
            "extra": {},
        }
        list_item.setData(Qt.ItemDataRole.UserRole, layer_metadata)
        self.layer_list.addItem(list_item)
        hp.reorder_list_by_z(self.layer_list)

    def detect(self):
        """
        Run object detection on the currently selected image.

        Loads a detection model, predicts polygons on the image,
        displays a success dialog, and adds the polygon layer to the scene.
        """
        initial_dir = hp.get_resource_path("resources/model")
        filters = "Deep Learning Models (*.pkl)"
        model_path, _ = QFileDialog.getOpenFileName(
            self.parent,
            caption="Open Deep Learning Model",
            directory=initial_dir,
            filter=filters
        )

        if not model_path:
            hp.show_dialog_box(
                self.parent,
                window_title="Warning",
                text="Model could not be opened. Please, try again.",
                button=QMessageBox.StandardButton.Discard,
                icon=QMessageBox.Icon.Critical,
            )
            return

        model = get_model(model_path)

        progress_bar = self.parent.contents_pane.progress_bar
        progress_bar.setVisible(True)
        progress_bar.setValue(10)

        img_path = hp.get_image_path(self.layer_list)
        if not img_path:
            hp.show_dialog_box(
                self.parent,
                window_title="Warning",
                text="The chosen layer is not an image. Please, try again.",
                button=QMessageBox.StandardButton.Discard,
                icon=QMessageBox.Icon.Critical,
            )
            progress_bar.setVisible(False)
            return

        progress_bar.setValue(30)

        try:
            polygons = predict_polygons(img_path, model, progress_callback=lambda x: progress_bar.setValue(x))
            progress_bar.setValue(80)
            self.add_polygon_layer(polygons)

            progress_bar.setValue(100)
            hp.show_dialog_box(self.parent, "Success", "The object detection is finished.")

        except Exception as e:
            hp.show_dialog_box(
                self.parent,
                window_title="Error",
                text=f"An error occurred during detection: {str(e)}",
                button=QMessageBox.StandardButton.Discard,
                icon=QMessageBox.Icon.Critical,
            )
            progress_bar.setVisible(False)
            return

    def up(self):
        """Move the currently selected layer up in Z-order."""
        current = self.layer_list.currentItem()

        if not current:
            return

        layer = current.data(Qt.ItemDataRole.UserRole)
        item = hp.unwrap_item(layer)
        if layer:
            layers = sorted(self.scene.items(), key=lambda i: i.zValue())
            index = layers.index(item)
            if index < len(layers) - 1:
                above_item = layers[index + 1]
                z1, z2 = item.zValue(), above_item.zValue()
                item.setZValue(z2)
                above_item.setZValue(z1)
                hp.reorder_list_by_z(self.layer_list)

    def down(self):
        """Move currently selected layer down in Z-order."""
        current = self.layer_list.currentItem()

        if not current:
            return

        layer = current.data(Qt.ItemDataRole.UserRole)
        item = hp.unwrap_item(layer)
        if item:
            items = sorted(self.scene.items(), key=lambda i: i.zValue())
            index = items.index(item)
            if index > 0:
                below_item = items[index - 1]
                z1, z2 = item.zValue(), below_item.zValue()
                item.setZValue(z2)
                below_item.setZValue(z1)
                hp.reorder_list_by_z(self.layer_list)

    def delete_layer(self):
        """
        Remove currently selected layer from both the scene and the layer list.

        After deletion, the remaining layers are reordered to maintain consistent Z-values.
        """
        current = self.layer_list.currentItem()
        if not current:
            return

        layer_data = current.data(Qt.ItemDataRole.UserRole)
        item = hp.unwrap_item(layer_data)
        self.scene.removeItem(item)
        self.layer_list.takeItem(self.layer_list.row(current))
        hp.reorder_list_by_z(self.layer_list)

    def select_item(self, current, _):
        """
        Slot. Handles item selection from a view.

        When an item is selected in a view or list, this function retrieves the
        associated data stored under Qt.UserRole, validates it, and if it's a
        valid graphics item, selects it and prints its z-value.

        Args:
            current: The currently selected item or index (e.g., QTreeWidgetItem or QModelIndex).
            _: Unused parameter (previous item in selection signals).
        """
        if current:
            data = current.data(Qt.ItemDataRole.UserRole)
            item = hp.unwrap_item(data)

            if item:
                item.setSelected(True)

    def create_action_save(parent, slot):
        action = QAction("Save", parent)
        action.setShortcut("Ctrl+S")
        action.triggered.connect(slot)
        return action

    def action_save(self):
        pass

    def action_save_as(self):
        pass

    def action_enter_full_screen(self):
        pass

"""
Define the InteractiveGraphicsView class, a customized QGraphicsView.
Provides interactive features: smooth zooming with
the mouse wheel and scroll-hand panning.

Classes:
    - InteractiveGraphicsView: Extends QGraphicsView

Usage Example:
    view = InteractiveGraphicsView(scene)
    view.show()
"""
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QWheelEvent
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QWidget,
)

from utils.helpers import compute_zoom


class MapPane(QGraphicsView):
    """A custom QGraphicsView that supports interactive zooming with the mouse wheel."""

    def __init__(self, scene: QGraphicsScene, parent: QWidget = None):
        """
        Initialize the interactive graphics view.

        Args:
            scene (`QGraphicsScene`): The graphics scene to visualize.
            parent (`QWidget`): The parent widget, if any.
        """
        super().__init__(scene, parent)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._zoom = 0
        self._min_zoom = -10
        self._max_zoom = 10

    def wheelEvent(self, event: QWheelEvent):
        """
        Handle mouse wheel events to perform zooming in/out.

        Args:
            event (`QWheelEvent`): The wheel event triggered by mouse input.
        """
        zoom_factor, new_zoom = compute_zoom(event.angleDelta().y(), self._zoom)

        if zoom_factor is None:
            return

        if not (self._min_zoom <= new_zoom <= self._max_zoom):
            return

        self._zoom = new_zoom
        self.scale(zoom_factor, zoom_factor)

    def reset_zoom(self):
        # NOTE: Changing anchor to center
        # to avoid cursor-relative zoom reset
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)

        self.resetTransform()
        self._zoom = 0

        scene_rect = self.scene().sceneRect()
        if not scene_rect.isNull():
            self.centerOn(scene_rect.center())

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

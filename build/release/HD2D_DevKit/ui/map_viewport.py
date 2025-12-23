from PyQt6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPixmap, QPen, QBrush, QColor, QMouseEvent, QWheelEvent
import numpy as np

class MapViewport(QGraphicsView):
    tile_placed = pyqtSignal(int, int, str)
    entity_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Editor state
        self.grid_size = 32
        self.show_grid = True
        self.current_layer = 0
        self.current_tool = "paint"  # paint, erase, select
        self.selected_tile = None
        
        # Map data
        self.map_data = None
        self.layers = []
        self.grid_lines = []
        
        # View settings
        self.zoom_level = 1.0
        self.setRenderHint(self.renderHints().Antialiasing)
        self.setOptimizationFlag(self.OptimizationFlag.DontSavePainterState)
        self.setViewportUpdateMode(self.ViewportUpdateMode.FullViewportUpdate)
        
        # Background
        self.scene.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
        
        self.setup_scene()
    
    def setup_scene(self):
        """Initialize the scene with grid"""
        self.draw_grid()
    
    def draw_grid(self):
        """Draw the grid overlay"""
        # Clear existing grid lines
        for line in self.grid_lines:
            self.scene.removeItem(line)
        self.grid_lines.clear()
        
        if not self.show_grid or not self.map_data:
            return
        
        pen = QPen(QColor(60, 60, 60))
        pen.setWidth(1)
        
        width = self.map_data["width"] * self.grid_size
        height = self.map_data["height"] * self.grid_size
        
        # Vertical lines
        for x in range(0, width + 1, self.grid_size):
            line = self.scene.addLine(x, 0, x, height, pen)
            self.grid_lines.append(line)
        
        # Horizontal lines
        for y in range(0, height + 1, self.grid_size):
            line = self.scene.addLine(0, y, width, y, pen)
            self.grid_lines.append(line)
    
    def load_project(self, project: dict):
        """Load a project into the viewport"""
        self.map_data = project
        self.grid_size = project.get("tile_size", 32)
        
        # Clear scene
        self.scene.clear()
        self.layers.clear()
        self.grid_lines.clear()
        
        # Create layers
        for i, layer_data in enumerate(project.get("layers", [])):
            layer = self.scene.createItemGroup([])
            layer.setZValue(i)
            self.layers.append(layer)
        
        # Draw grid
        self.draw_grid()
        
        # Set scene rect
        width = project["width"] * self.grid_size
        height = project["height"] * self.grid_size
        self.scene.setSceneRect(QRectF(0, 0, width, height))
        
        self.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
    
    def toggle_grid(self):
        """Toggle grid visibility"""
        self.show_grid = not self.show_grid
        self.draw_grid()
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse clicks for painting"""
        if not self.map_data or event.button() != Qt.MouseButton.LeftButton:
            super().mousePressEvent(event)
            return
        
        scene_pos = self.mapToScene(event.position().toPoint())
        grid_x = int(scene_pos.x() // self.grid_size)
        grid_y = int(scene_pos.y() // self.grid_size)
        
        if self.current_tool == "paint" and self.selected_tile:
            self.place_tile(grid_x, grid_y, self.selected_tile)
        elif self.current_tool == "erase":
            self.erase_tile(grid_x, grid_y)
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse drag for continuous painting"""
        if not self.map_data or event.buttons() != Qt.MouseButton.LeftButton:
            super().mouseMoveEvent(event)
            return
        
        scene_pos = self.mapToScene(event.position().toPoint())
        grid_x = int(scene_pos.x() // self.grid_size)
        grid_y = int(scene_pos.y() // self.grid_size)
        
        if self.current_tool == "paint" and self.selected_tile:
            self.place_tile(grid_x, grid_y, self.selected_tile)
        
        super().mouseMoveEvent(event)
    
    def wheelEvent(self, event: QWheelEvent):
        """Handle zoom with mouse wheel"""
        zoom_factor = 1.15
        if event.angleDelta().y() < 0:
            zoom_factor = 1.0 / zoom_factor
        
        self.zoom_level *= zoom_factor
        self.zoom_level = max(0.1, min(5.0, self.zoom_level))
        
        self.resetTransform()
        self.scale(self.zoom_level, self.zoom_level)
    
    def place_tile(self, x: int, y: int, tile_id: str):
        """Place a tile on the map"""
        if x < 0 or y < 0 or x >= self.map_data["width"] or y >= self.map_data["height"]:
            return
        
        # Remove existing tile at position
        self.erase_tile(x, y, silent=True)
        
        # Add new tile (placeholder - would use actual tile pixmap)
        rect_item = self.scene.addRect(
            x * self.grid_size, y * self.grid_size,
            self.grid_size, self.grid_size,
            QPen(Qt.PenStyle.NoPen), QBrush(QColor(100, 150, 200))
        )
        rect_item.setZValue(self.current_layer)
        
        if self.current_layer < len(self.layers):
            self.layers[self.current_layer].addToGroup(rect_item)
        
        self.tile_placed.emit(x, y, tile_id)
    
    def erase_tile(self, x: int, y: int, silent: bool = False):
        """Remove tile at position"""
        items = self.scene.items(
            x * self.grid_size, y * self.grid_size,
            self.grid_size, self.grid_size,
            Qt.ItemSelectionMode.ContainsShape
        )
        
        for item in items:
            if isinstance(item, type(self.scene.addRect(0,0,1,1))):
                self.scene.removeItem(item)
    
    def set_current_layer(self, layer_index: int):
        """Set the active layer for painting"""
        self.current_layer = layer_index
    
    def set_selected_tile(self, tile_id: str):
        """Set the tile to paint with"""
        self.selected_tile = tile_id

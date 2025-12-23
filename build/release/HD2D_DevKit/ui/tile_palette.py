from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QListWidget,
                           QListWidgetItem, QPushButton, QComboBox, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon
from core.tile_manager import TileManager

class TilePalette(QWidget):
    tile_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.tile_manager = TileManager()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Tileset selector
        tileset_layout = QHBoxLayout()
        tileset_layout.addWidget(QLabel("Tileset:"))
        self.tileset_combo = QComboBox()
        self.tileset_combo.currentTextChanged.connect(self.load_tileset)
        tileset_layout.addWidget(self.tileset_combo)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.scan_tilesets)
        tileset_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(tileset_layout)
        
        # Tile list
        self.tile_list = QListWidget()
        self.tile_list.setViewMode(QListWidget.ViewMode.IconMode)
        self.tile_list.setIconSize(64, 64)
        self.tile_list.setGridSize(80, 80)
        self.tile_list.itemClicked.connect(self.on_tile_selected)
        layout.addWidget(self.tile_list)
        
        # Load tilesets button
        load_btn = QPushButton("Load New Tileset")
        load_btn.clicked.connect(self.load_new_tileset)
        layout.addWidget(load_btn)
        
        self.setLayout(layout)
        self.scan_tilesets()
    
    def scan_tilesets(self):
        """Scan assets/tiles directory for tilesets"""
        import os
        self.tileset_combo.clear()
        tiles_dir = "assets/tiles"
        if os.path.exists(tiles_dir):
            for file in os.listdir(tiles_dir):
                if file.lower().endswith(('.png', '.jpg', '.bmp')):
                    self.tileset_combo.addItem(file)
    
    def load_tileset(self, filename: str):
        """Load selected tileset into the palette"""
        if not filename:
            return
        
        path = f"assets/tiles/{filename}"
        # Assume 32px tiles by default - could add UI to configure
        tiles = self.tile_manager.load_tileset(filename, path, 32)
        
        self.tile_list.clear()
        for tile_id, qimage in tiles.items():
            pixmap = QPixmap.fromImage(qimage)
            item = QListWidgetItem(QIcon(pixmap), "")
            item.setData(Qt.ItemDataRole.UserRole, tile_id)
            self.tile_list.addItem(item)
    
    def load_new_tileset(self):
        """Open file dialog to load new tileset"""
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Tileset", "", "Images (*.png *.jpg *.bmp)"
        )
        if file_path:
            # Copy to assets folder
            import shutil
            filename = file_path.split("/")[-1]
            shutil.copy(file_path, f"assets/tiles/{filename}")
            self.scan_tilesets()
    
    def on_tile_selected(self, item: QListWidgetItem):
        """Emit signal when tile is selected"""
        tile_id = item.data(Qt.ItemDataRole.UserRole)
        self.tile_selected.emit(tile_id)

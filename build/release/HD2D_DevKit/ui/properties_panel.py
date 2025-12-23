from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QLineEdit,
                           QSpinBox, QDoubleSpinBox, QCheckBox, QLabel, QGroupBox)
from PyQt6.QtCore import pyqtSignal

class PropertiesPanel(QWidget):
    properties_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.current_entity = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Entity Properties Group
        entity_group = QGroupBox("Entity Properties")
        entity_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        entity_layout.addRow("Name:", self.name_edit)
        
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setRange(-9999, 9999)
        entity_layout.addRow("X:", self.x_spin)
        
        self.y_spin = QDoubleSpinBox()
        self.y_spin.setRange(-9999, 9999)
        entity_layout.addRow("Y:", self.y_spin)
        
        self.layer_spin = QSpinBox()
        self.layer_spin.setRange(0, 99)
        entity_layout.addRow("Layer:", self.layer_spin)
        
        self.visible_check = QCheckBox("Visible")
        entity_layout.addRow("", self.visible_check)
        
        self.collidable_check = QCheckBox("Collidable")
        entity_layout.addRow("", self.collidable_check)
        
        entity_group.setLayout(entity_layout)
        layout.addWidget(entity_group)
        
        # Map Properties Group
        map_group = QGroupBox("Map Properties")
        map_layout = QFormLayout()
        
        self.map_width_label = QLabel("-")
        map_layout.addRow("Width:", self.map_width_label)
        
        self.map_height_label = QLabel("-")
        map_layout.addRow("Height:", self.map_height_label)
        
        self.tile_size_label = QLabel("-")
        map_layout.addRow("Tile Size:", self.tile_size_label)
        
        map_group.setLayout(map_layout)
        layout.addWidget(map_group)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def load_entity(self, entity_data: dict):
        """Load entity data into properties panel"""
        self.current_entity = entity_data
        
        self.name_edit.setText(entity_data.get("name", ""))
        self.x_spin.setValue(entity_data.get("x", 0))
        self.y_spin.setValue(entity_data.get("y", 0))
        self.layer_spin.setValue(entity_data.get("properties", {}).get("layer", 0))
        self.visible_check.setChecked(entity_data.get("properties", {}).get("visible", True))
        self.collidable_check.setChecked(entity_data.get("properties", {}).get("collidable", False))
    
    def load_map_properties(self, map_data: dict):
        """Load map metadata"""
        self.map_width_label.setText(str(map_data.get("width", "-")))
        self.map_height_label.setText(str(map_data.get("height", "-")))
        self.tile_size_label.setText(str(map_data.get("tile_size", "-")) + "px")

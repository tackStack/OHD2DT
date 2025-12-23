from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QListWidget,
                           QListWidgetItem, QHBoxLayout, QCheckBox, QSpinBox)
from PyQt6.QtCore import pyqtSignal

class LayerPanel(QWidget):
    layer_selected = pyqtSignal(int)
    layer_visibility_changed = pyqtSignal(int, bool)
    
    def __init__(self):
        super().__init__()
        self.layers = []
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Layer controls
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add Layer")
        self.add_btn.clicked.connect(self.add_layer)
        btn_layout.addWidget(self.add_btn)
        
        self.remove_btn = QPushButton("Remove")
        self.remove_btn.clicked.connect(self.remove_layer)
        btn_layout.addWidget(self.remove_btn)
        
        layout.addLayout(btn_layout)
        
        # Layer list
        self.layer_list = QListWidget()
        self.layer_list.itemClicked.connect(self.on_layer_selected)
        layout.addWidget(self.layer_list)
        
        # Layer properties
        props_layout = QVBoxLayout()
        
        self.parallax_spin = QSpinBox()
        self.parallax_spin.setRange(0, 100)
        self.parallax_spin.setSuffix("%")
        props_layout.addWidget(self.parallax_spin)
        
        layout.addLayout(props_layout)
        
        self.setLayout(layout)
    
    def add_layer(self):
        """Add a new layer"""
        layer_name = f"Layer {len(self.layers)}"
        item = QListWidgetItem(layer_name)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(Qt.CheckState.Checked)
        self.layer_list.insertItem(0, item)
        self.layers.append({"name": layer_name, "visible": True, "parallax": 100})
        
        # Auto-select new layer
        self.layer_list.setCurrentRow(0)
        self.layer_selected.emit(0)
    
    def remove_layer(self):
        """Remove selected layer"""
        row = self.layer_list.currentRow()
        if row >= 0:
            self.layer_list.takeItem(row)
            del self.layers[row]
    
    def on_layer_selected(self, item):
        """Handle layer selection"""
        row = self.layer_list.row(item)
        self.layer_selected.emit(row)
    
    def on_layer_visibility_changed(self, item):
        """Handle visibility toggle"""
        row = self.layer_list.row(item)
        visible = item.checkState() == Qt.CheckState.Checked
        self.layers[row]["visible"] = visible
        self.layer_visibility_changed.emit(row, visible)

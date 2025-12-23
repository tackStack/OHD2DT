from PyQt6.QtWidgets import QToolBar, QComboBox, QAction, QButtonGroup
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import pyqtSignal

class EditorToolbar(QToolBar):
    tool_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__("Tools")
        self.init_ui()
    
    def init_ui(self):
        # Tool selection group
        self.tool_group = QButtonGroup(self)
        self.tool_group.buttonClicked.connect(self.on_tool_selected)
        
        # Paint tool
        self.paint_action = self.addAction(QIcon("assets/icons/paint.png"), "Paint (P)")
        self.paint_action.setCheckable(True)
        self.paint_action.setChecked(True)
        
        # Erase tool
        self.erase_action = self.addAction(QIcon("assets/icons/erase.png"), "Erase (E)")
        self.erase_action.setCheckable(True)
        
        # Select tool
        self.select_action = self.addAction(QIcon("assets/icons/select.png"), "Select (S)")
        self.select_action.setCheckable(True)
        
        self.addSeparator()
        
        # Zoom controls
        self.zoom_in_action = self.addAction(QIcon("assets/icons/zoom_in.png"), "Zoom In")
        self.zoom_out_action = self.addAction(QIcon("assets/icons/zoom_out.png"), "Zoom Out")
        self.zoom_fit_action = self.addAction(QIcon("assets/icons/zoom_fit.png"), "Fit to View")
    
    def on_tool_selected(self, action):
        """Emit tool change signal"""
        tool_map = {
            self.paint_action: "paint",
            self.erase_action: "erase",
            self.select_action: "select"
        }
        tool = tool_map.get(action, "paint")
        self.tool_changed.emit(tool)

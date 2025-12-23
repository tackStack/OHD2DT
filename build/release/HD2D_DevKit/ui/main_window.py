from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                           QMenuBar, QMenu, QToolBar, QFileDialog, QMessageBox,
                           QDockWidget, QSplitter, QStatusBar)
from PyQt6.QtCore import Qt
from .map_viewport import MapViewport
from .tile_palette import TilePalette
from .layer_panel import LayerPanel
from .properties_panel import PropertiesPanel
from .toolbar import EditorToolbar

class MainWindow(QMainWindow):
    def __init__(self, project_manager):
        super().__init__()
        self.project_manager = project_manager
        self.setWindowTitle("HD2D DevKit - Advanced Map Editor")
        self.setGeometry(100, 100, 1600, 900)
        
        self.setup_ui()
        self.setup_menu()
        self.setup_toolbar()
        self.setup_status_bar()
    
    def setup_ui(self):
        # Create central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left panel - Tile Palette
        self.tile_palette = TilePalette()
        tile_dock = QDockWidget("Tile Palette", self)
        tile_dock.setWidget(self.tile_palette)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, tile_dock)
        
        # Center - Map Viewport
        self.map_viewport = MapViewport()
        main_splitter.addWidget(self.map_viewport)
        
        # Right panel - Layers & Properties
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        
        self.layer_panel = LayerPanel()
        layer_dock = QDockWidget("Layers", self)
        layer_dock.setWidget(self.layer_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, layer_dock)
        
        self.properties_panel = PropertiesPanel()
        props_dock = QDockWidget("Properties", self)
        props_dock.setWidget(self.properties_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, props_dock)
        
        self.tabifyDockWidget(layer_dock, props_dock)
        layer_dock.raise_()
    
    def setup_menu(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("&File")
        
        new_project = file_menu.addAction("&New Project")
        new_project.setShortcut("Ctrl+N")
        new_project.triggered.connect(self.new_project)
        
        open_project = file_menu.addAction("&Open Project")
        open_project.setShortcut("Ctrl+O")
        open_project.triggered.connect(self.open_project)
        
        file_menu.addSeparator()
        
        save_project = file_menu.addAction("&Save Project")
        save_project.setShortcut("Ctrl+S")
        save_project.triggered.connect(self.save_project)
        
        # Edit Menu
        edit_menu = menubar.addMenu("&Edit")
        
        undo_action = edit_menu.addAction("&Undo")
        undo_action.setShortcut("Ctrl+Z")
        
        redo_action = edit_menu.addAction("&Redo")
        redo_action.setShortcut("Ctrl+Y")
        
        # Tools Menu
        tools_menu = menubar.addMenu("&Tools")
        
        grid_toggle = tools_menu.addAction("Toggle &Grid")
        grid_toggle.setShortcut("G")
        grid_toggle.triggered.connect(self.map_viewport.toggle_grid)
        
        # View Menu
        view_menu = menubar.addMenu("&View")
        view_menu.addAction(layer_dock.toggleViewAction())
        view_menu.addAction(props_dock.toggleViewAction())
        view_menu.addAction(tile_dock.toggleViewAction())
    
    def setup_toolbar(self):
        self.toolbar = EditorToolbar()
        self.addToolBar(self.toolbar)
    
    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - No project loaded")
    
    def new_project(self):
        from PyQt6.QtWidgets import QDialog, QFormLayout, QSpinBox, QLineEdit, QDialogButtonBox
        
        dialog = QDialog(self)
        dialog.setWindowTitle("New Project")
        layout = QFormLayout()
        
        name_edit = QLineEdit("MyGame")
        width_spin = QSpinBox()
        width_spin.setRange(10, 1000)
        width_spin.setValue(100)
        height_spin = QSpinBox()
        height_spin.setRange(10, 1000)
        height_spin.setValue(100)
        tile_size_spin = QSpinBox()
        tile_size_spin.setRange(8, 256)
        tile_size_spin.setValue(32)
        
        layout.addRow("Project Name:", name_edit)
        layout.addRow("Map Width:", width_spin)
        layout.addRow("Map Height:", height_spin)
        layout.addRow("Tile Size:", tile_size_spin)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            project = self.project_manager.create_project(
                name_edit.text(),
                width_spin.value(),
                height_spin.value(),
                tile_size_spin.value()
            )
            self.map_viewport.load_project(project)
            self.status_bar.showMessage(f"Project '{project['name']}' created")
    
    def open_project(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "assets/projects", "HD2D Files (*.h2d)"
        )
        if file_path:
            project = self.project_manager.load_project(file_path)
            self.map_viewport.load_project(project)
            self.status_bar.showMessage(f"Loaded project: {project['name']}")
    
    def save_project(self):
        if self.project_manager.current_project:
            self.project_manager.save_project(self.project_manager.current_project)
            self.status_bar.showMessage("Project saved successfully")

# HD2D_DevKit
"Official" HD2D Tool Kit. 
Features
HD2D Rendering:
High-resolution tile support (8px to 256px)
Multiple layer parallax scrolling for depth effects
Entity/component system for game objects
Dynamic property editing with live preview

Advanced Map Editor UI:
Dockable panels - Customize your workspace
Tile palette with drag-and-drop
Layer management with visibility toggles
Real-time property inspector
Zoom & pan viewport with grid snapping
Tool system (Paint, Erase, Select)
Project serialization (JSON format)

One-Click Deployment:
Single-file executable generation
Asset bundling - all resources included
Cross-platform support (Windows, macOS, Linux)

Requirements:
Python 3.8 or higher
pip (Python package manager)

Quick Start:

Option 1: Simple Build (Recommended)
Run the automated build script:
python build_simple.py

This installs dependencies, creates assets, and builds the EXE automatically.

Option 2: Manual Setup
Clone the repository:
git clone https://github.com/tackStack/HD2D_DevKit.git
cd HD2D_DevKit

Install dependencies:
pip install -r requirements.txt

Create placeholder assets:
python create_icons.py

Run the editor:
python src/main.py

Build exe:
python build.py

 Project Structure:
HD2D_DevKit/
├── src/
│   ├── main.py                 # Application entry point
│   ├── core/                   # Core engine modules
│   │   ├── map_engine.py       # Map rendering logic
│   │   ├── tile_manager.py     # Tileset management
│   │   ├── entity_system.py    # Entity/component system
│   │   └── project_manager.py  # Project save/load
│   ├── ui/                     # User interface
│   │   ├── main_window.py      # Main window layout
│   │   ├── map_viewport.py     # Interactive map view
│   │   ├── tile_palette.py     # Tile selection panel
│   │   ├── layer_panel.py      # Layer management
│   │   ├── properties_panel.py # Property editor
│   │   └── toolbar.py          # Tool selection
│   └── utils/                  # Utilities
│       └── asset_loader.py     # Asset loading helpers
├── assets/
│   ├── tiles/                  # Tileset images (*.png)
│   ├── entities/               # Entity sprites
│   └── projects/               # Saved project files (*.h2d)
├── build/
│   ├── release/                # Final EXE output
│   └── temp/                   # Build temporary files
├── requirements.txt            # Python dependencies
├── build.py                    # Manual build script
├── build_simple.py            # Automated build script
└── README.md                  # This file





 Usage Guide:
Creating Your First Project
Launch the editor (HD2D_DevKit.exe or python src/main.py)
File → New Project (or press Ctrl+N)
Set your map dimensions and tile size (default 32px)
Load a tileset:
Click "Load New Tileset" in the Tile Palette
Select a PNG image with tiles in a grid
Start mapping:
Select a tile from the palette
Choose a tool (Paint/Erase)
Click/drag on the map viewport
Manage layers:
Add layers for background, foreground, etc.
Toggle visibility with checkboxes
Save your project (Ctrl+S)

Key       Action
Ctrl+N	New Project
Ctrl+O	Open Project
Ctrl+S	Save Project
G	Toggle Grid
P	Paint Tool
E	Erase Tool
S	Select Tool
Mouse Wheel	Zoom In/Out
Middle Click + Drag	Pan Viewport


Working with Entities
Place entities using the entity tool (coming in v1.1)
Select entities to edit properties in the Properties panel
Add components for behavior (physics, animation, etc.)
Set collision flags for gameplay logic

 Building the Executable:
Automated Build
python build_simple.py

Creates build/release/HD2D_DevKit.exe with all assets bundled.

Manual Build
python build.py

For custom build configurations.

Build Requirements
PyInstaller (installed automatically)
Windows: Visual C++ Redistributable (usually pre-installed)
macOS: Xcode Command Line Tools
Linux: python3-dev package
  

Troubleshooting:

Installation Issues
"pip not found": Use py -m pip (Windows) or python3 -m pip (macOS/Linux)
Permission errors: Add --user flag: pip install --user -r requirements.txt
Build tools missing: Install Visual Studio Build Tools (Windows) or python3-dev (Linux)
Runtime Issues
"Module not found": Ensure you're in the project root directory
Assets not loading: Check assets/ folder exists and contains files
Black screen: Verify your graphics drivers are up to date
Build Issues
PyInstaller fails: Run pip install --upgrade pyinstaller
Missing DLLs: Install Visual C++ Redistributable
Large file size: Use UPX compression (add --upx-dir=path/to/upx to build.py)



Creating HD2D Assets:
Tileset Guidelines
Size: Power of 2 (16x16, 32x32, 64x64, 128x128)
Format: PNG with transparency
Layout: Grid-based, evenly spaced
Style: Mix 2D sprites with 3D lighting effects for HD2D look

Recommended Tools:
Aseprite: Pixel art & animation ($)
Krita: Free digital painting
Tiled: Alternative map editor (export to PNG)
Blender: Render 3D assets as 2D sprites


MIT License - feel free to use for commercial and personal projects.



Fork the repository
Create a feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

 v1.1: Entity placement & editing tools
 v1.2: Animation editor & timeline
 v1.3: Shader support for HD2D effects
 v1.4: Export to Unity/Godot plugins
 v1.5: Collaborative editing & version control




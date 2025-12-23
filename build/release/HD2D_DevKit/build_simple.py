import subprocess
import sys
import os
import shutil
from pathlib import Path

def run_command(cmd, description):
    """Run a command and show progress"""
    print(f"📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Done!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Failed!")
        print(f"Error: {e.stderr}")
        return False

def create_placeholder_assets():
    """Create minimal required assets"""
    print("🎨 Creating placeholder assets...")
    
    # Create directories
    dirs = ["assets/tiles", "assets/icons", "assets/projects"]
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    
    # Create simple colored tileset
    from PIL import Image, ImageDraw
    
    # Create a 3x3 tileset (96x96px, 32px tiles)
    tileset = Image.new('RGBA', (96, 96), (0, 0, 0, 0))
    draw = ImageDraw.Draw(tileset)
    
    colors = ["red", "green", "blue", "yellow", "purple", "orange", "cyan", "magenta", "white"]
    for i, color in enumerate(colors):
        x = (i % 3) * 32
        y = (i // 3) * 32
        draw.rectangle([x, y, x+30, y+30], fill=color)
    
    tileset.save("assets/tiles/default.png")
    
    # Create app icon
    icon = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    draw.rectangle([4, 4, 28, 28], fill="cyan")
    icon.save("assets/icons/app.png")
    
    # Convert PNG to ICO for Windows
    try:
        from PIL import Image
        img = Image.open("assets/icons/app.png")
        img.save("assets/icons/app.ico")
    except:
        pass
    
    print("✅ Assets created!")

def main():
    print("=" * 50)
    print("HD2D DevKit - EXE Builder")
    print("=" * 50)
    
    # Step 1: Install dependencies
    print("\n🔧 Step 1: Installing dependencies...")
    deps = ["PyQt6==6.6.1", "Pillow==10.2.0", "numpy==1.26.4", "pyinstaller==6.4.0"]
    
    for dep in deps:
        if not run_command(f"{sys.executable} -m pip install {dep}", f"Installing {dep}"):
            print("\n⚠️  Installation failed. Try running as Administrator or with sudo.")
            sys.exit(1)
    
    # Step 2: Create assets
    print("\n🎨 Step 2: Setting up assets...")
    create_placeholder_assets()
    
    # Step 3: Create main.py if it doesn't exist
    if not os.path.exists("src/main.py"):
        print("\n⚠️  src/main.py not found! Creating minimal version...")
        os.makedirs("src", exist_ok=True)
        
        minimal_main = '''import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HD2D DevKit")
        self.setGeometry(100, 100, 800, 600)
        
        label = QLabel("HD2D DevKit is working!\\n\\nPlace your main.py in the src folder.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)

if __name__ == "__main__":
    from PyQt6.QtCore import Qt
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
'''
        with open("src/main.py", "w") as f:
            f.write(minimal_main)
    
    # Step 4: Build EXE
    print("\n🔨 Step 3: Building executable...")
    
    # Clean previous builds
    if os.path.exists("build/release"):
        shutil.rmtree("build/release")
    
    # PyInstaller command
    pyinstaller_cmd = f'''
    {sys.executable} -m PyInstaller 
    src/main.py 
    --name=HD2D_DevKit 
    --onefile 
    --windowed 
    --icon=assets/icons/app.ico 
    --add-data=assets;assets 
    --add-data=src;src 
    --hidden-import=PyQt6 
    --hidden-import=PIL 
    --hidden-import=numpy 
    --clean 
    --noconfirm 
    --distpath=./build/release 
    --workpath=./build/temp
    '''
    
    # Remove newlines for execution
    pyinstaller_cmd = pyinstaller_cmd.replace('\n', ' ')
    
    if run_command(pyinstaller_cmd, "Building EXE with PyInstaller"):
        print("\n" + "=" * 50)
        print("🎉 SUCCESS!")
        print(f"📁 EXE location: {os.path.abspath('build/release/HD2D_DevKit.exe')}")
        print("=" * 50)
    else:
        print("\n❌ Build failed. Check errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

import PyInstaller.__main__
import os
import shutil

def build_exe():
    # Clean previous build
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    if os.path.exists("build"):
        shutil.rmtree("build")
    
    # PyInstaller configuration
    PyInstaller.__main__.run([
        'src/main.py',
        '--name=HD2D_DevKit',
        '--onefile',
        '--windowed',
        '--icon=assets/icons/app.ico',
        '--add-data=assets;assets',
        '--add-data=src;src',
        '--hidden-import=PyQt6',
        '--hidden-import=PIL',
        '--hidden-import=numpy',
        '--clean',
        '--noconfirm',
        '--distpath=./build/release',
        '--workpath=./build/temp',
    ])
    
    print("Build complete! Executable at: build/release/HD2D_DevKit.exe")

if __name__ == "__main__":
    build_exe()

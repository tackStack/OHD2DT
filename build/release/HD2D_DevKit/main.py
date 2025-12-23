import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.project_manager import ProjectManager

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("HD2D DevKit")
    app.setOrganizationName("GameDevStudio")
    
    # Initialize project manager
    project_manager = ProjectManager()
    
    # Create and show main window
    window = MainWindow(project_manager)
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

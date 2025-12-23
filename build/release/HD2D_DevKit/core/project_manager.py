import json
import os
from pathlib import Path

class ProjectManager:
    def __init__(self):
        self.current_project = None
        self.projects_dir = Path("assets/projects")
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def create_project(self, name: str, width: int, height: int, tile_size: int = 32):
        project = {
            "name": name,
            "width": width,
            "height": height,
            "tile_size": tile_size,
            "layers": [],
            "entities": []
        }
        
        project_path = self.projects_dir / f"{name}.h2d"
        with open(project_path, 'w') as f:
            json.dump(project, f, indent=2)
        
        self.current_project = project
        return project
    
    def load_project(self, path: str):
        with open(path, 'r') as f:
            self.current_project = json.load(f)
        return self.current_project
    
    def save_project(self, project: dict, path: str = None):
        save_path = path or self.projects_dir / f"{project['name']}.h2d"
        with open(save_path, 'w') as f:
            json.dump(project, f, indent=2)

from PIL import Image, ImageQt
from pathlib import Path
import json

class TileManager:
    def __init__(self):
        self.tiles = {}
        self.tilesets = {}
        self.assets_dir = Path("assets/tiles")
        self.assets_dir.mkdir(parents=True, exist_ok=True)
    
    def load_tileset(self, name: str, path: str, tile_size: int):
        """Load a tileset image and split into individual tiles"""
        img = Image.open(path).convert("RGBA")
        tiles = {}
        
        for y in range(0, img.height, tile_size):
            for x in range(0, img.width, tile_size):
                tile_id = f"{name}_{x}_{y}"
                tile_img = img.crop((x, y, x + tile_size, y + tile_size))
                tiles[tile_id] = ImageQt.ImageQt(tile_img)
        
        self.tilesets[name] = {
            "path": path,
            "tile_size": tile_size,
            "tiles": tiles
        }
        return tiles
    
    def get_tile(self, tileset: str, x: int, y: int):
        """Get a specific tile from a tileset"""
        tile_id = f"{tileset}_{x}_{y}"
        return self.tilesets.get(tileset, {}).get("tiles", {}).get(tile_id)

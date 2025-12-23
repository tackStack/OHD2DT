import uuid
from typing import Dict, List, Any

class Entity:
    def __init__(self, name: str, x: float, y: float, entity_type: str = "sprite"):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.x = x
        self.y = y
        self.type = entity_type
        self.components = {}
        self.properties = {
            "visible": True,
            "collidable": False,
            "layer": 1
        }
    
    def add_component(self, component: 'Component'):
        self.components[component.name] = component
    
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "x": self.x,
            "y": self.y,
            "type": self.type,
            "properties": self.properties,
            "components": {k: v.to_dict() for k, v in self.components.items()}
        }

class Component:
    def __init__(self, name: str, data: dict):
        self.name = name
        self.data = data
    
    def to_dict(self) -> dict:
        return self.data

class EntitySystem:
    def __init__(self):
        self.entities: Dict[str, Entity] = {}
    
    def create_entity(self, name: str, x: float, y: float, entity_type: str = "sprite") -> Entity:
        entity = Entity(name, x, y, entity_type)
        self.entities[entity.id] = entity
        return entity
    
    def get_entity(self, entity_id: str) -> Entity:
        return self.entities.get(entity_id)
    
    def remove_entity(self, entity_id: str):
        if entity_id in self.entities:
            del self.entities[entity_id]
    
    def get_all_entities(self) -> List[Entity]:
        return list(self.entities.values())
    
    def serialize(self) -> list:
        return [entity.to_dict() for entity in self.entities.values()]

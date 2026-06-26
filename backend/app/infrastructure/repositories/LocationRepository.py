import json
from pathlib import Path
from typing import List
from dataclasses import replace
from app.domain.models.LocationEntity import LocationEntity

class LocationRepository:

    instance = None
    locations: List[LocationEntity] = []
    loaded: bool = False

    def __new__(cls, *args, **kwargs) -> 'LocationRepository':
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self, path: str = "data/locations.json"):
        if not self.loaded:
            self.file_path = Path(path)
            self.load_locations()

    def load_locations(self) -> None:
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                raw_locations = json.load(f)

            self.locations = [LocationEntity.from_dict(loc) for loc in raw_locations]
            self.loaded = True
        except FileNotFoundError:
            raise FileNotFoundError("Archivo no encontrado")
        except json.JSONDecodeError as e:
            raise ValueError("Error al parsear JSON")

    def get_locations(self):
        return self.locations

    def get_by_zone(self, zone: str):
        return [loc for loc in self.locations if loc.zone == zone]

    def get_by_tags_all(self, tags: list[str]):
        non_repeated = set(tags)
        devolver = []

        for loc in self.locations:
            loc_tags = loc.tags
            if all(loc_tags.get(tag, False) for tag in non_repeated):
                devolver.append(loc)

        return devolver

    def get_by_tags_any(self, tags: list[str]):
        non_repeated = set(tags)
        devolver = []

        for loc in self.locations:
            loc_tags = loc.tags
            if any(loc_tags.get(tag, False) for tag in non_repeated):
                devolver.append(loc)

        return devolver

    def get_by_id(self, id: str):
        for loc in self.locations:
            if loc.id == id:
                return replace(loc)
        return None

    def reload(self):
        self.loaded = False
        self.load_locations()
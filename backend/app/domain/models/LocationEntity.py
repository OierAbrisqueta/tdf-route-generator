from dataclasses import dataclass
from typing import List, Optional

@dataclass()
class LocationEntity:
    id: str
    name: str
    country: str
    lat: float
    lon: float
    zone: str
    tags: List[str]

    @classmethod
    def from_dict(cls, data: dict):
        devolver = cls(
            id = data.get("id", ""),
            name = data.get("name", ""),
            country = data.get("country", ""),
            lat = data.get("lat", 0.0),
            lon = data.get("lon", 0.0),
            zone = data.get("zone", ""),
            tags = data.get("tags", [])
        )
        return devolver

    @classmethod
    def to_dict(cls):
        devolver = {
            "id": cls.id,
            "name": cls.name,
            "country": cls.country,
            "lat": cls.lat,
            "lon": cls.lon,
            "zone": cls.zone,
            "tags": cls.tags
        }
        return devolver
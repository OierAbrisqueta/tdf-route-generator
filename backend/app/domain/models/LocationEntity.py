from dataclasses import dataclass
from typing import List

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

    def to_dict(self):
        devolver = {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "lat": self.lat,
            "lon": self.lon,
            "zone": self.zone,
            "tags": self.tags
        }
        return devolver
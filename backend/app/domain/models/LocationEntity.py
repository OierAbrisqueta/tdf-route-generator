from dataclasses import dataclass
from typing import Dict

@dataclass()
class LocationEntity:
    id: str
    name: str
    country: str
    lat: float
    lon: float
    zone: str
    tags: Dict[str, bool]

    @classmethod
    def from_dict(cls, data: dict) -> "LocationEntity":
        devolver = cls(
            id = data.get("id", ""),
            name = data.get("name", ""),
            country = data.get("country", ""),
            lat = data.get("lat", 0.0),
            lon = data.get("lon", 0.0),
            zone = data.get("zone", ""),
            tags = data.get("tags", {})
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
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class StageType(str, Enum):
    FLAT = "FLAT"
    HILLY = "HILLY"
    MOUNTAIN = "MOUNTAIN"
    ITT = "ITT"
    TTT = "TTT"


class Location(BaseModel):
    """Una ciudad o sede."""
    id: str
    name: str
    country: str
    zone: str
    lat: float
    lon: float


class Stage(BaseModel):
    """Una etapa del Tour."""
    stage_number: int
    stage_type: StageType
    start_location: Location
    finish_location: Location
    distance_km: float
    transfer_km: float  # Distancia desde el final de la etapa anterior
    rest_day_after: bool = False


class TourSummary(BaseModel):
    """Resumen del Tour generado."""
    total_stages: int
    total_distance_km: float
    countries_visited: List[str]
    stages_by_type: dict  # {"FLAT": 8, "HILLY": 6, ...}
    score: float


class GenerateResponse(BaseModel):
    """Respuesta completa del endpoint /generate."""
    seed: int
    settings: dict
    stages: List[Stage]
    summary: TourSummary
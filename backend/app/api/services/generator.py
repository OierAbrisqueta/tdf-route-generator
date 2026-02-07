import random
from typing import List
from ..schemas.response import (
    StageType,
    Location,
    Stage,
    TourSummary,
    GenerateResponse,
)
from ..schemas.requests import GenerateRequest

# Datos dummy para el MVP
SAMPLE_LOCATIONS = [
    Location(id="bilbao", name="Bilbao", country="Spain", zone="FOREIGN", lat=43.263, lon=-2.935),
    Location(id="san_sebastian", name="San Sebastián", country="Spain", zone="FOREIGN", lat=43.318, lon=-1.981),
    Location(id="bayonne", name="Bayonne", country="France", zone="PYRENEES", lat=43.493, lon=-1.475),
    Location(id="pau", name="Pau", country="France", zone="PYRENEES", lat=43.295, lon=-0.370),
    Location(id="toulouse", name="Toulouse", country="France", zone="SOUTH", lat=43.604, lon=1.444),
    Location(id="montpellier", name="Montpellier", country="France", zone="SOUTH", lat=43.611, lon=3.877),
    Location(id="alpe_dhuez", name="Alpe d'Huez", country="France", zone="ALPS", lat=45.092, lon=6.071),
    Location(id="grenoble", name="Grenoble", country="France", zone="ALPS", lat=45.188, lon=5.724),
    Location(id="lyon", name="Lyon", country="France", zone="CENTRAL", lat=45.764, lon=4.835),
    Location(id="dijon", name="Dijon", country="France", zone="CENTRAL", lat=47.322, lon=5.041),
    Location(id="paris", name="Paris", country="France", zone="PARIS", lat=48.856, lon=2.352),
]


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calcula distancia aproximada en km entre dos puntos."""
    from math import radians, sin, cos, sqrt, atan2

    R = 6371  # Radio de la Tierra en km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c


def generate_tour(request: GenerateRequest) -> GenerateResponse:
    """
    Genera un Tour basado en los settings.
    Por ahora: versión simplificada / placeholder.
    """
    # Seed para reproducibilidad
    seed = request.seed if request.seed is not None else random.randint(1, 999999)
    random.seed(seed)

    # Generar etapas dummy (simplificado)
    stages: List[Stage] = []
    locations = SAMPLE_LOCATIONS.copy()

    # Asegurar que París es el final
    paris = next(loc for loc in locations if loc.id == "paris")
    other_locations = [loc for loc in locations if loc.id != "paris"]
    random.shuffle(other_locations)

    # Crear secuencia simple: otras ciudades + París al final
    num_stages = min(request.stages, len(other_locations))
    route_locations = other_locations[:num_stages] + [paris]

    # Tipos de etapa (distribución simple)
    stage_types = (
            [StageType.FLAT] * 4 +
            [StageType.HILLY] * 3 +
            [StageType.MOUNTAIN] * 3 +
            [StageType.ITT] * request.itt_count
    )
    if request.ttt_enabled:
        stage_types.append(StageType.TTT)

    # Ajustar al número de etapas
    while len(stage_types) < num_stages + 1:
        stage_types.append(random.choice([StageType.FLAT, StageType.HILLY]))
    stage_types = stage_types[:num_stages + 1]
    stage_types[-1] = StageType.FLAT  # Última etapa siempre llana (París)
    random.shuffle(stage_types[:-1])  # Shuffle todo menos la última

    # Construir etapas
    prev_finish = None
    for i in range(len(route_locations) - 1):
        start_loc = route_locations[i]
        finish_loc = route_locations[i + 1]

        # Calcular distancias
        stage_distance = haversine_km(
            start_loc.lat, start_loc.lon,
            finish_loc.lat, finish_loc.lon
        ) * random.uniform(1.1, 1.4)  # Factor de "carretera real"

        transfer_km = 0.0
        if prev_finish:
            transfer_km = haversine_km(
                prev_finish.lat, prev_finish.lon,
                start_loc.lat, start_loc.lon
            )

        stage = Stage(
            stage_number=i + 1,
            stage_type=stage_types[i],
            start_location=start_loc,
            finish_location=finish_loc,
            distance_km=round(stage_distance, 1),
            transfer_km=round(transfer_km, 1),
            rest_day_after=(i + 1) in [9, 15],  # Descanso tras etapas 9 y 15
        )
        stages.append(stage)
        prev_finish = finish_loc

    # Resumen
    countries = list(set(s.start_location.country for s in stages) |
                     set(s.finish_location.country for s in stages))

    stages_by_type = {}
    for s in stages:
        stages_by_type[s.stage_type.value] = stages_by_type.get(s.stage_type.value, 0) + 1

    summary = TourSummary(
        total_stages=len(stages),
        total_distance_km=round(sum(s.distance_km for s in stages), 1),
        countries_visited=sorted(countries),
        stages_by_type=stages_by_type,
        score=random.uniform(70, 100),  # Placeholder
    )

    return GenerateResponse(
        seed=seed,
        settings=request.model_dump(),
        stages=stages,
        summary=summary,
    )
from typing import List, Dict, Any
import random
from ...infrastructure.repositories.LocationRepository import LocationRepository
from ..schemas.requests import GenerateRequest
from ..schemas.response import GenerateResponse, Stage, StageType, Location, TourSummary

class RouteGenerator:

    def __init__(self, location_repository):
        self.location_repository = location_repository

    def generate(self, request: GenerateRequest) -> GenerateResponse:
        if request.seed is not None:
            seed = request.seed
        else:
            seed = random.randint(0, 2**31 - 1)

        random.seed(seed)

        stages: List[Stage] = []

        start_locations = self._get_start_locations()
        mountain_finishes = self._get_mountain_finishes()
        tt_locations = self._get_tt_locations()
        all_finish_locations = self._get_finish_locations()

        #Select initial location
        if request.foreign_start:
            foreign_starts = [loc for loc in start_locations if loc.get("zone") == "FOREIGN"]
            start_location = random.choice(foreign_starts) if foreign_starts else random.choice(start_locations)
        else:
            france_starts = [loc for loc in start_locations if loc.get("zone") != "FOREIGN"]
            start_location = random.choice(france_starts) if france_starts else random.choice(start_locations)

        #Generate stages
        previous_location = start_location
        foreign_stages_count = 0
        foreign_stages_target = random.randint(request.foreign_stages_min, request.foreign_stages_max)
        itt_remaining = request.itt_count
        ttt_done = not request.ttt_enabled

        for stage_num in range(1, request.stages + 1):
            stage_type = self._determine_stage_type(
                stage_num=stage_num,
                total_stages=request.stages,
                mountain_bias=request.mountain_bias,
                itt_remaining=itt_remaining,
                ttt_done=ttt_done
            )

            if stage_type == StageType.ITT:
                itt_remaining -= 1
            elif stage_type == StageType.TTT:
                ttt_done = True

            finish_location = self._select_finish_location(
                stage_type=stage_type,
                stage_num=stage_num,
                total_stages=request.stages,
                foreign_stages_count=foreign_stages_count,
                foreign_stages_target=foreign_stages_target,
                mountain_finishes=mountain_finishes,
                tt_locations=tt_locations,
                all_finish_locations=all_finish_locations,
                previous_location=previous_location
            )

            if finish_location.get("zone") == "FOREIGN":
                foreign_stages_count += 1

            #This distances are orientative
            distance_km = self._calculate_stage_distance(previous_location, finish_location, stage_type)
            transfer_km = self._calculate_transfer_distance(previous_location, start_location) if stage_num > 1 else 0.0

            rest_day_after = self._should_have_rest_day(stage_num, request.stages)

            stage = Stage(
                stage_number=stage_num,
                stage_type=stage_type,
                start_location=self._location_dict_to_schema(
                    previous_location if stage_num > 1 else start_location
                ),
                finish_location=self._location_dict_to_schema(finish_location),
                distance_km=distance_km,
                transfer_km=transfer_km,
                rest_day_after=rest_day_after
            )
            stages.append(stage)
            previous_location = finish_location

        summary = self._create_summary(stages)

        return GenerateResponse(
            seed=seed,
            settings=request.model_dump(),
            stages=stages,
            summary=summary
        )



    def _get_start_locations(self, include_foreigns: bool = True) -> List[Dict[str, Any]]:
        all_locations = self.location_repository.get_locations()
        start_locations = [
            loc for loc in all_locations
            if loc.get("tags", {}).get("can_start", False)
        ]
        if not include_foreigns:
            start_locations = [
                loc for loc in start_locations
                if loc.get("zone") != "FOREIGN"
            ]
        return start_locations

    def _get_finish_locations(self) -> List[Dict[str, Any]]:
        all_locations = self.location_repository.get_locations()
        finish = [
            loc for loc in all_locations
            if loc.get("tags", {}).get("can_finish", False)
        ]
        return finish

    def _get_mountain_finishes(self) -> List[Dict[str, Any]]:
        all_locations = self.location_repository.get_locations()
        return [
            loc for loc in all_locations
            if loc.get("tags", {}).get("mountain_finish", False)
        ]

    def _get_tt_locations(self) -> List[Dict[str, Any]]:
        all_locations = self.location_repository.get_locations()
        return [
            loc for loc in all_locations
            if loc.get("tags", {}).get("tt_ok", False)
        ]

    def _get_locations_by_zone(self, zone: str) -> List[Dict[str, Any]]:
        return self.location_repository.get_by_zone(zone)

    def _determine_stage_type(self, stage_num: int, total_stages: int, mountain_bias: float,
            itt_remaining: int, ttt_done: bool) -> StageType:
        #The first stage could be a ttt(team time trial)
        if stage_num == 1 and not ttt_done:
            if random.random() < 0.5:
                return StageType.TTT

        #There usually is an individual time trial at the end
        if itt_remaining > 0 and stage_num > total_stages - 5:
            if random.random() < 0.4:
                return StageType.ITT

        #Determines the type based on the mountain_bias
        roll = random.random()
        if roll < mountain_bias * 0.4:
            return StageType.MOUNTAIN
        elif roll < mountain_bias * 0.4 + 0.3:
            return StageType.HILLY
        else:
            return StageType.FLAT

    def _select_finish_location(self, stage_type: StageType, stage_num: int, total_stages: int, foreign_stages_count: int,
            foreign_stages_target: int, mountain_finishes: List[Dict[str, Any]], tt_locations: List[Dict[str, Any]], all_finish_locations: List[Dict[str, Any]],
            previous_location: Dict[str, Any]) -> Dict[str, Any]:

        candidates = []

        if stage_type == StageType.MOUNTAIN:
            candidates = mountain_finishes
        elif stage_type in (StageType.ITT, StageType.TTT):
            candidates = tt_locations
        else:
            candidates = all_finish_locations

        #Filter foreign stages
        if foreign_stages_count >= foreign_stages_target:
            candidates = [loc for loc in candidates if loc.get("zone") != "FOREIGN"]

        #Last stage has to be Paris
        if stage_num == total_stages:
            paris = [loc for loc in all_finish_locations if loc.get("name", "").lower() == "paris"]
            if paris:
                return paris[0]

        #Do not repeat location
        candidates = [loc for loc in candidates if loc.get("id") != previous_location.get("id")]

        if not candidates:
            candidates = all_finish_locations

        return random.choice(candidates)

    def _calculate_stage_distance(self, start: Dict[str, Any], finish: Dict[str, Any], stage_type: StageType) -> float:
        #Calculate line distance between places (orientative)
        from math import radians, sin, cos, sqrt, atan2

        lat1, lon1 = radians(start.get("lat", 0)), radians(start.get("lon", 0))
        lat2, lon2 = radians(finish.get("lat", 0)), radians(finish.get("lon", 0))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        r = 6371  # Earth Radius

        straight_line = r * c

        #Based on stage type
        if stage_type == StageType.ITT:
            return max(20.0, min(60.0, straight_line * 0.5))
        elif stage_type == StageType.TTT:
            return max(25.0, min(55.0, straight_line * 0.5))
        elif stage_type == StageType.MOUNTAIN:
            return max(100.0, min(200.0, straight_line * 1.5))
        else:
            return max(150.0, min(250.0, straight_line * 1.3))

    def _calculate_transfer_distance(self, previous_finish: Dict[str, Any], current_start: Dict[str, Any]) -> float:
        #Calculates de transfer distance
        from math import radians, sin, cos, sqrt, atan2

        lat1, lon1 = radians(previous_finish.get("lat", 0)), radians(previous_finish.get("lon", 0))
        lat2, lon2 = radians(current_start.get("lat", 0)), radians(current_start.get("lon", 0))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        r = 6371

        return r * c

    def _should_have_rest_day(self, stage_num: int, total_stages: int) -> bool:
        """Determina si debe haber día de descanso después de esta etapa."""
        # Días de descanso típicos en el Tour: después de etapas 9 y 15
        if total_stages >= 21:
            return stage_num in [9, 15]
        elif total_stages >= 14:
            return stage_num in [7, 12]
        elif total_stages >= 7:
            return stage_num == 5
        return False

    def _is_rest_day(self, stage_num: int) -> bool:
        return stage_num in [9, 15]

    def _location_dict_to_schema(self, loc: Dict[str, Any]) -> Location:
        return Location(
            id=loc.get("id", ""),
            name=loc.get("name", ""),
            country=loc.get("country", ""),
            zone=loc.get("zone", ""),
            lat=loc.get("lat", 0.0),
            lon=loc.get("lon", 0.0)
        )

    def _create_summary(self, stages: List[Stage]) -> TourSummary:
        total_distance = sum(stage.distance_km for stage in stages)
        countries = list(set(
            stage.finish_location.country for stage in stages
        ) | set(
            stage.start_location.country for stage in stages
        ))

        stages_by_type = {}
        for stage in stages:
            type_name = stage.stage_type.value
            stages_by_type[type_name] = stages_by_type.get(type_name, 0) + 1

        score = self._calculate_score(stages, countries)

        return TourSummary(
            total_stages=len(stages),
            total_distance_km=round(total_distance, 1),
            countries_visited=countries,
            stages_by_type=stages_by_type,
            score=round(score, 2)
        )

    def _calculate_score(self, stages: List[Stage], countries: List[str]) -> float:
        score: float = 50

        score += len(countries) * 5

        stage_types = set(stage.stage_type for stage in stages)
        score += len(stage_types) * 5

        for stage in stages:
            if stage.distance_km < 100 and stage.stage_type not in (StageType.ITT, StageType.TTT):
                score -= 2
            elif stage.distance_km > 250:
                score -= 2

        if len(countries) > 5:
            return 0

        return min(100, max(0, score))

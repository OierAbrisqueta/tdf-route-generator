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
        all_locations = self.location_repo.get_locations()
        return [
            loc for loc in all_locations
            if loc.get("tags", {}).get("mountain_finish", False)
        ]

    def _get_tt_locations(self) -> List[Dict[str, Any]]:
        all_locations = self.location_repo.get_locations()
        return [
            loc for loc in all_locations
            if loc.get("tags", {}).get("tt_ok", False)
        ]

    def _get_locations_by_zone(self, zone: str) -> List[Dict[str, Any]]:
        return self.location_repo.get_by_zone(zone)

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
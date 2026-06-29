from typing import List
import random
from app.api.schemas.requests import GenerateRequest
from app.api.schemas.response import GenerateResponse, Stage, StageType, Location, TourSummary
from app.domain.models.LocationEntity import LocationEntity

DISTANCE_RULES = {
        StageType.ITT: {20, 50},
        StageType.TTT: {20, 40},
        StageType.MOUNTAIN: {130, 220},
        StageType.HILLY: {160, 210},
        StageType.FLAT: {170, 230}
    }

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
            foreign_starts = [loc for loc in start_locations if loc.zone == "FOREIGN"]
            start_location = random.choice(foreign_starts) if foreign_starts else random.choice(start_locations)
        else:
            france_starts = [loc for loc in start_locations if loc.zone != "FOREIGN"]
            start_location = random.choice(france_starts) if france_starts else random.choice(start_locations)

        #Determine the number of stages of the foreign start
        if request.foreign_start:
            number_foreign_stages = random.randint(request.foreign_stages_min, request.foreign_stages_max)
        else:
            number_foreign_stages = 0

        #Generate stages
        previous_location = start_location
        itt_remaining = request.itt_count
        ttt_done = not request.ttt_enabled

        for stage_num in range(1, request.stages + 1):

            in_foreign_block = stage_num <= number_foreign_stages

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
                stage_type = stage_type,
                stage_num = stage_num,
                total_stages = request.stages,
                in_foreign_block = in_foreign_block,
                mountain_finishes = mountain_finishes,
                tt_locations = tt_locations,
                all_finish_locations = all_finish_locations,
                previous_location = previous_location
            )

            stage_start_location = previous_location if stage_num > 1 else start_location

            #This distances are orientative
            distance_km = self._calculate_stage_distance(stage_start_location, finish_location, stage_type)
            transfer_km = (
                self._calculate_transfer_distance(previous_location, stage_start_location)
                if stage_num > 1
                else 0.0
            )

            rest_day_after = self._should_have_rest_day(stage_num, request.stages)

            stage = Stage(
                stage_number=stage_num,
                stage_type=stage_type,
                start_location=self._location_entity_to_schema(stage_start_location),
                finish_location=self._location_entity_to_schema(finish_location),
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

    def _get_start_locations(self) -> List[LocationEntity]:
        all_locations = self.location_repository.get_locations()
        start_locations = [
            loc for loc in all_locations
            if loc.tags.get("can_start", False)
        ]
        return start_locations

    def _get_finish_locations(self) -> List[LocationEntity]:
        all_locations = self.location_repository.get_locations()
        finish = [
            loc for loc in all_locations
            if loc.tags.get("can_finish", False)
        ]
        return finish

    def _get_mountain_finishes(self) -> List[LocationEntity]:
        all_locations = self.location_repository.get_locations()
        return [
            loc for loc in all_locations
            if loc.tags.get("mountain_finish", False)
        ]

    def _get_tt_locations(self) -> List[LocationEntity]:
        all_locations = self.location_repository.get_locations()
        return [
            loc for loc in all_locations
            if loc.tags.get("tt_ok", False)
        ]

    def _get_locations_by_zone(self, zone: str) -> List[LocationEntity]:
        return self.location_repository.get_by_zone(zone)

    def _determine_stage_type(self, stage_num: int, total_stages: int, mountain_bias: float,
            itt_remaining: int, ttt_done: bool, recent_types = list[StageType]) -> StageType:

        #No more than 3 mountain stages in a row
        if recent_types[-2:].count(StageType.MOUNTAIN) >= 3:
            return random.choice([StageType.HILLY, StageType.FLAT])

        #Flat/Transition after mountain block
        if self._is_end_of_mountain_block(recent_types):
            return StageType.FLAT

        progress = stage_num / total_stages

        #The first stage could be a ttt(team time trial)
        if stage_num == 1 and not ttt_done:
            if random.random() < 0.3:
                return StageType.TTT

        #There usually is an individual time trial at the end
        if itt_remaining > 0 and stage_num == total_stages - 1:
            if random.random() < 0.8:
                return StageType.ITT

        is_mountain_block = (0.35 < progress < 0.55) or (0.7 < progress < 0.9)
        real_bias = mountain_bias * (2 if is_mountain_block else 0.5)

        #Determines the type based on the mountain_bias
        roll = random.random()
        if roll < real_bias * 0.4:
            return StageType.MOUNTAIN
        elif roll < real_bias * 0.4 + 0.3:
            return StageType.HILLY
        else:
            return StageType.FLAT

    def _is_end_of_mountain_block(self, recent_types: list[StageType]):
        streak = 0
        for stage in reversed(recent_types):
            if stage == StageType.MOUNTAIN:
                streak += 1
            else:
                break

        return streak >= 3

    def _select_finish_location(self, stage_type: StageType, stage_num: int, total_stages: int, in_foreign_block : bool, mountain_finishes: List[LocationEntity], tt_locations: List[LocationEntity], all_finish_locations: List[LocationEntity],
            previous_location: LocationEntity) -> LocationEntity:

        # Last stage has to be Paris
        if stage_num == total_stages:
            paris = [loc for loc in all_finish_locations if loc.name.lower() == "paris"]
            if paris:
                return paris[0]

        candidates = []

        if stage_type == StageType.MOUNTAIN:
            candidates = mountain_finishes
        elif stage_type in (StageType.ITT, StageType.TTT):
            candidates = tt_locations
        else:
            candidates = all_finish_locations

        #If we are in the foreign starting block, stages must finish abroad
        if in_foreign_block:
            foreign_candidates = [loc for loc in candidates if loc.zone == "FOREIGN"]
            #If the specific type has no foreign options, fall back to any foreign location.
            candidates = foreign_candidates if foreign_candidates else [
                loc for loc in all_finish_locations if loc.zone == "FOREIGN"
            ]
        else:
            national_candidates = [loc for loc in candidates if loc.zone != "FOREIGN"]
            #If the specific type has no national options, fall back to any foreign location.
            candidates = national_candidates if national_candidates else [
                loc for loc in all_finish_locations if loc.zone != "FOREIGN"
            ]

        #Do not repeat location
        candidates = [loc for loc in candidates if loc.id != previous_location.id]

        if not candidates:
            candidates = all_finish_locations

        return random.choice(candidates)

    def _haversine(self, start, finish) -> float:
        """The Harversine Formula is applied"""
        # Calculate line distance between places (orientative)
        from math import radians, sin, cos, sqrt, atan2

        lat1, lon1 = radians(start.lat), radians(start.lon)
        lat2, lon2 = radians(finish.lat), radians(finish.lon)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        r = 6371  # Earth Radius

        straight_line = r * c

        return straight_line

    def _calculate_stage_distance(self, start: LocationEntity, finish: LocationEntity, stage_type: StageType) -> float:
        straight_line = self._haversine(start, finish)
        min_d, max_d = DISTANCE_RULES[stage_type]

        road_reality = {
            StageType.MOUNTAIN: random.uniform(1.6, 2.2),
            StageType.HILLY: random.uniform(1.3, 1.7),
            StageType.FLAT: random.uniform(1.2, 1.4),
        }.get(stage_type)

        return round(straight_line * road_reality, 2)

    def _calculate_transfer_distance(self, previous_finish: LocationEntity, current_start: LocationEntity) -> float:
        """The Harversine Formula is applied"""
        #Calculates de transfer distance
        from math import radians, sin, cos, sqrt, atan2

        lat1, lon1 = radians(previous_finish.lat), radians(previous_finish.lon)
        lat2, lon2 = radians(current_start.lat), radians(current_start.lon)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        r = 6371

        return r * c

    def _should_have_rest_day(self, stage_num: int, total_stages: int) -> bool:
        """Determines whether the next day should be a rest day or not"""
        #Usually the 9 and 15 days
        if total_stages >= 21:
            return stage_num in [9, 15]
        elif total_stages >= 14:
            return stage_num in [7, 12]
        elif total_stages >= 7:
            return stage_num == 5
        return False

    def _is_rest_day(self, stage_num: int) -> bool:
        return stage_num in [9, 15]

    def _location_entity_to_schema(self, loc: LocationEntity) -> Location:
        return Location(
            id=loc.id,
            name=loc.name,
            country=loc.country,
            zone=loc.zone,
            lat=loc.lat,
            lon=loc.lon
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
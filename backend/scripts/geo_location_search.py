from __future__ import annotations

from pathlib import Path
import json
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

INPUT_NORMALIZED = Path("data/locations_normalized.json")
OUT_JSON_SUCCESS = Path("data/locations_geocoded.json")
OUT_FAIL = Path("data/locations_geocoded_fail.json")
CACHE = Path("data/geocode_cache.json")

MIN_DELAY = 1.1

COUNTRY_HINTS = [
    "France",
    "Belgium",
    "Netherlands",
    "Luxembourg",
    "Germany",
    "Switzerland",
    "Italy",
    "Spain",
    "United Kingdom",
    "Ireland",
    "Andorra",
    "Monaco",
]


def country_code(raw: dict | None):
    if not raw:
        return None
    addr = raw.get("address") or {}
    cc = addr.get("country_code")
    if isinstance(cc, str) and len(cc) == 2:
        return cc.upper()
    return None


def try_geocode(geocode, name: str):
    #First tries to find the country among COUNTRY_HINTS
    for c in COUNTRY_HINTS:
        q = f"{name}, {c}"
        place = geocode(q, exactly_one=True, addressdetails=True)
        if place:
            return place

    #If it does not fit into any of those countries tries to find it without it's country
    return geocode(name, exactly_one=True, addressdetails=True)


def main():
    locations = json.loads(INPUT_NORMALIZED.read_text(encoding="utf-8"))

    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    failed = []
    out = []

    geolocator = Nominatim(user_agent="tdf-route-generator/1.0 (local script)")
    geocode = RateLimiter(
        geolocator.geocode,
        min_delay_seconds=MIN_DELAY,
        swallow_exceptions=False,
    )

    for i, loc in enumerate(locations, start=1):
        loc_id = loc["id"]
        name = loc["name"]
        cache_key = name

        result = cache.get(cache_key)

        if result is None:
            time.sleep(0.01)
            place = try_geocode(geocode, name)

            if place is None:
                # NO cacheamos None para evitar cache envenenado por fallos temporales
                failed.append({"id": loc_id, "name": name})
                continue

            raw = place.raw
            result = {
                "lat": float(place.latitude),
                "lon": float(place.longitude),
                "display_name": raw.get("display_name"),
                "country_code": country_code(raw),
            }

            cache[cache_key] = result
            CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")

        out.append(
            {
                "id": loc_id,
                "name": name,
                "lat": result["lat"],
                "lon": result["lon"],
                "country": result.get("country_code"),
                "source": "nominatim",
                "display_name": result.get("display_name"),
            }
        )

        if i % 30 == 0:
            print(f"Processed {i}/{len(locations)}")

    OUT_JSON_SUCCESS.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_FAIL.write_text(json.dumps(failed, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Done")
    print(f"Geocoded: {len(out)}")
    if failed:
        print(f"Failed: {len(failed)} -> {OUT_FAIL}")


if __name__ == "__main__":
    main()
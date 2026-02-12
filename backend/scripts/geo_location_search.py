from __future__ import annotations

from pathlib import Path
import json
import time
from typing import Any

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

INPUT_NORMALIZED = Path("data/locations_normalized.json")
OUT_JSON_SUCCESS = Path("data/locations_geocoded.json")
OUT_FAIL = Path("data/locations_geocoded_fail.json")
CACHE = Path("data/geocode_cache.json")

MIN_DELAY = 1.1

def country_code(loc:dict | None):
    if not loc:
        return None
    addr = loc.get("adress") or {}
    cc = addr.get("country_code")
    if (isinstance(cc, str) and len(cc) == 2):
        return cc.upper()
    return None

def main():
    locations = json.loads(INPUT_NORMALIZED.read_text(encoding = "utf-8"))

    if CACHE.exists():
        cache = json.loads(CACHE.read_text(encoding="utf-8"))
    else:
        cache = {}

    failed = []

    geolocator = Nominatim(user_agent = "tdf-route-generator/1.0 (local script)")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds = MIN_DELAY, swallow_exceptions = False)

    out = []

    i = 1
    for loc in locations:
        loc_id = loc ["id"]
        name = loc["name"]
        cache_key = name

        if cache_key in cache:
            result = cache[cache_key]
        else:
            #Only searches for places in Europe
            query = f"{name}, Europe"
            time.sleep(0.01)
            place = geocode(query, exactly_one = True, addressdetails = True)

            if place is None:
                cache[cache_key] = None
                result = None
            else:
                raw = place.raw
                result = {
                    "lat": float(place.latitude),
                    "lon": float(place.longitude),
                    "raw": raw,
                    "display_name": raw.get("display_name"),
                    "country_code": country_code(raw)
                }

            CACHE.write_text(json.dumps(cache, ensure_ascii = False, indent = 2), encoding = "utf-8")

        if result is None:
            failed.append({"id": loc_id, "name": name})
            continue

        out.append({
            "id": loc_id,
            "name": name,
            "lat": result["lat"],
            "lon": result["lon"],
            "country": result["country_code"],
            "source": "nominatim",
            "display_name": result["display_name"]
        })

        if i%30 == 0:
            print(f"Processed{i}/{len(locations)}")
        i += 1

    OUT_JSON_SUCCESS.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    OUT_FAIL.write_text(json.dumps(failed, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Done")
    if failed:
        print(f"Failes n = {len(failed)}")

if __name__ == "__main__":
    main()
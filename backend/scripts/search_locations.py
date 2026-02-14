from __future__ import annotations

from pathlib import Path
import json
from typing import Any

IN_GEOCODED = Path("data/locations_geocoded.json")
IN_GEOCODED_OVERRIDES = Path("data/locations_geocoded_overrides.json")
OUT_ZONED = Path("data/locations_zoned.json")

def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))

def store_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def zone(lat, long, country, name):
    #Foreign country
    if not country or country.upper() != "FR":
        return "FOREIGN"

    #Paris zone
    if (lat - 48.8566) ** 2 + (long - 2.3522) ** 2 < (0.25 ** 2) :
        return "PARIS"

    #Rest of France
    mid_lat = 6.5
    mid_long = 2

    north = lat >= mid_lat
    west = long < mid_long

    if north and west:
        return "FR_NW"
    elif not north and west:
        return "FR_SW"
    elif north and not west:
        return "FR_NE"
    else:
        return "FR_SE"

def main():
    data1 = load_json(IN_GEOCODED)
    data2 = load_json(IN_GEOCODED_OVERRIDES)
    all_data = data1 + data2

    out = []
    error = []

    for location in all_data:
        long = location.get("lon")
        lat = location.get("lat")
        name = location.get("name")
        country = location.get("country")

        if lat is None or long is None:
            error.append(f"{name} has either the latitude or the longitude missing")
            continue

        location["zone"] = zone(lat, long, country, name)
        out.append(location)

    store_json(OUT_ZONED, out)

    if error:
        for e in error:
            print(e)

if __name__ == "__main__":
    main()
from __future__ import annotations

from pathlib import Path
import json
from typing import Any

IN_TAGGED = Path("data/locations_tagged.json")
OUT_FINAL = Path("data/locations.json")

ADD_COUNTRY_TO_ID = True

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def store(data, path):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def main():
    tagged = load(IN_TAGGED)

    out = []
    seen_ids = set()
    collisions = []

    for loc in tagged:
        loc_id = loc.get("id")
        name = loc.get("name")
        lat = loc.get("lat")
        lon = loc.get("lon")
        country = loc.get("country")
        zone = loc.get("zone")
        tags = loc.get("tags")

        if not loc_id or not name or lat is None or lon is None:
            continue

        location = {
            "id": loc_id,
            "name": name,
            "country": country,
            "lat": float(lat),
            "lon": float(lon),
            "zone": zone,
            "tags": {
                "can_start": bool(tags.get("can_start")),
                "can_finish": bool(tags.get("can_finish")),
                "mountain_finish": bool(tags.get("mountain_finish")),
                "tt_ok": bool(tags.get("tt_ok")),
            }}

        if loc_id in seen_ids:
            collisions.append(location)
            continue

        seen_ids.add(loc_id)
        out.append(location)

    store(out, OUT_FINAL)

    if collisions:
        print(f"{len(collisions)} collisions after export")
        print(collisions[:20])

if __name__ == "__main__":
    main()
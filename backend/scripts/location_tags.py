from __future__ import annotations

import json
from pathlib import Path
import _json
from typing import Any

IN_LOCATIONS = Path("data/locations_zoned.json")
OUT_LOCATIONS = Path("data/locations_tagged.json")
TAGS_OVERRIDES = Path("data/location_tags_overrides.json")

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def store(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def default_tags():
    return {
        "can_start": True,
        "can_finish": True,
        "mountain_finish": False,
        "tt_ok": True,
    }

def main():
    locations = load(IN_LOCATIONS)
    overrides = load(TAGS_OVERRIDES)

    out = []

    for loc in locations:
        loc_id = locations.get("id")

        tags = default_tags()

        if loc_id in overrides:
            tags.update(overrides.get(loc_id))

        loc2 = dict(loc)
        loc2["tags"] = tags
        out.append(loc2)

    store(OUT_LOCATIONS, out)

if __name__ == "__main__":
    main()
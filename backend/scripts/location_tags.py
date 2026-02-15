from __future__ import annotations

import json
from pathlib import Path
import _json
from typing import Any

IN_LOCATIONS = Path("data/locations_zoned.json")
OUT_LOCATIONS = Path("data/locations_tagged.json")

MOUNTAIN_KEYWORDS = [
    "col ",
    "mont ",
    "plateau",
    "alpe",
    "super",
    "val thorens",
    "tignes",
    "la plagne",
    "courchevel",
    "avoriaz",
    "les deux alpes",
    "les menuires",
    "isola 2000",
    "luz ardiden",
    "hautacam",
    "tourmalet",
    "izoard",
    "ventoux",
    "semnoz",
    "risoul",
    "pra-loup",
    "piau",
    "peyragudes",
    "pla d'adet",
    "pyrenees 2000",
    "orcières",
    "merlette",
    "serre chevalier",
    "le lioran",
    "station",
]

NON_TT_KEYWORDS = [
    "circuit",
    "eurotunnel",
]

DISABLE_START_FINISH_IDS = {
    "pal",
}

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

def is_mountain_finish(name):
    for word in MOUNTAIN_KEYWORDS:
        if word in name.lower():
            return True
    return False

def is_non_tt(name):
    for word in NON_TT_KEYWORDS:
        if word in name.lower():
            return True
    return False

def main():
    locations = load(IN_LOCATIONS)
    overrides = {}

    out = []

    for loc in locations:
        loc_id = loc.get("id")
        name = loc.get("name")

        tags = default_tags()

        if loc_id in DISABLE_START_FINISH_IDS:
            tags["can_start"] = False
            tags["can_finish"] = False
            tags["tt_ok"] = False

        if is_mountain_finish(name):
            tags["mountain_finish"] = True
            tags["tt_ok"] = False

        if is_non_tt(name):
            tags["tt_ok"] = False

        loc2 = dict(loc)
        loc2["tags"] = tags
        out.append(loc2)

    store(OUT_LOCATIONS, out)

if __name__ == "__main__":
    main()
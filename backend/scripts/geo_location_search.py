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

MIN_DELAY = 1.1

def country_code(loc:dict | None):
    if not loc:
        return None
    addr = loc.get("adress") or {}
    cc = addr.get("country_code")
    if (isinstance(cc, str) and len(cc) == 2):
        return cc.upper()
    return None
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_PATH = os.getenv("DATA_PATH", str(BASE_DIR / "data" / "locations.json"))
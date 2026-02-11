from __future__ import annotations
from pathlib import Path
import json
import re
import unicodedata

RAW_TXT = Path("data/raw_locations.txt")
ALIASES_JSON = Path("data/location_aliases.json")
OUT_JSON = Path("data/locations_normalized.json")
#OUT_REPORT = Path("data/locations_normalize_report.json")

#Removes accents
def strip_accents(text):
    descomposed_text = unicodedata.normalize("NFKD", text)

    #Filters characters and keeps only the "base" letters
    base_characters = [
        char for char in descomposed_text
        if not unicodedata.combining(char)
    ]

    devolver = "".join(base_characters)
    return devolver

def clean_name(text):
    text = text.strip()

    #Unify apostrophes
    text = text.replace("’", "'").replace("`", "'")

    #Normalize frequent hyphens
    text = text.replace("–", "-").replace("—", "-")

    #Remove double spaces
    text = re.sub(r"\s+", " ", text)

    #Remove final comas or misplaced characters
    text = re.sub(r"[,\s]+$", "", text).strip()

    return text

def slugify(text):
    text = strip_accents(text)
    text = text.lower()

    #Mantein letters and numbers, the rest becomes "_"
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    text = text.strip("_")

    return text

def main():
    if not RAW_TXT.exists():
        raise SystemExit(f"Missing input file: {RAW_TXT}")

    aliases = {}
    if ALIASES_JSON.exists():
        aliases = json.loads(ALIASES_JSON.read_text(encoding="utf-8"))

    raw_lines = RAW_TXT.read_text(encoding = "utf-8").splitlines()
    semicleaned_lines = []
    for ln in raw_lines:
        stripped_line = ln.strip()

        #If the line is not an empty string it is added to the cleaned_lines list
        if (stripped_line):
            semicleaned_lines.append(stripped_line)

    cleaned_locations = []
    for ln in semicleaned_lines:
        raw_clean = clean_name(ln)
        canonical = aliases.get(raw_clean, raw_clean)
        canonical = clean_name(canonical)
        id = slugify(canonical)

        cleaned_locations.append(
            {
                "raw": ln,
                "raw_clean": raw_clean,
                "name": canonical,
                "id": id
            }
        )

    # Remove duplicate locations
    by_id = {}
    collisions = []

    for location in cleaned_locations:
        loc_id = location["id"]
        if loc_id not in by_id:
            by_id[loc_id] = ({"id": loc_id, "name": location["name"]})
        else:
            collisions.append({"id": loc_id, "name": location["name"]})

    final = sorted(by_id.values(), key=lambda x: x["name"].lower())

    OUT_JSON.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")

    if (collisions):
        print("There are collisions review the location alianses")

if __name__ == "__main__":
    main()
from __future__ import annotations

from pathlib import Path
import json
import re
import unicodedata

RAW_TXT = Path("data/raw_locations.txt")
ALIASES_JSON = Path("data/location_aliases.json")
OUT_JSON = Path("data/locations_normalized.json")
OUT_REPORT = Path("data/locations_collisions_report.json")


def strip_accents(text: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(c)
    )


def clean_soft(text: str) -> str:
    text = text.strip()
    text = text.replace("’", "'").replace("`", "'")
    text = text.replace("–", "-").replace("—", "-")
    text = re.sub(r"\s+", " ", text)
    return text


def clean_hard(text: str) -> str:
    text = clean_soft(text)
    # si no quieres quitar paréntesis, comenta esta línea:
    text = re.sub(r"\s*\((.*?)\)\s*", "", text).strip()
    text = re.sub(r"[,\s]+$", "", text).strip()
    return text


def slugify(text: str) -> str:
    text = strip_accents(text).lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text


def score_name(name: str, alias_applied: bool) -> tuple:
    """
    Decide qué 'name' es mejor como canónico para un id.
    Preferencias:
    1) si vino de alias (decisión humana) gana
    2) nombre con acentos/caracteres no-ascii (más “bonito” para UI) gana
    3) nombre más largo (suele tener más info) gana
    """
    has_non_ascii = any(ord(c) > 127 for c in name)
    return (
        1 if alias_applied else 0,
        1 if has_non_ascii else 0,
        len(name),
    )


def main() -> None:
    if not RAW_TXT.exists():
        raise SystemExit(f"Missing input file: {RAW_TXT}")

    aliases = {}
    if ALIASES_JSON.exists():
        aliases = json.loads(ALIASES_JSON.read_text(encoding="utf-8"))

    raw_lines = RAW_TXT.read_text(encoding="utf-8").splitlines()
    raw_lines = [ln.strip() for ln in raw_lines if ln.strip()]

    # Agrupar por id
    grouped: dict[str, dict] = {}
    variants: dict[str, set[str]] = {}

    for raw in raw_lines:
        soft = clean_soft(raw)
        aliased = aliases.get(soft, soft)
        alias_applied = soft in aliases

        canonical = clean_hard(aliased)
        loc_id = slugify(canonical)
        if not loc_id:
            continue

        variants.setdefault(loc_id, set()).add(canonical)

        if loc_id not in grouped:
            grouped[loc_id] = {"id": loc_id, "name": canonical, "_score": score_name(canonical, alias_applied)}
        else:
            candidate_score = score_name(canonical, alias_applied)
            if candidate_score > grouped[loc_id]["_score"]:
                grouped[loc_id] = {"id": loc_id, "name": canonical, "_score": candidate_score}

    # construir salida final
    final = [{"id": v["id"], "name": v["name"]} for v in grouped.values()]
    final = sorted(final, key=lambda x: x["name"].lower())
    OUT_JSON.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")

    # construir reporte de ids con múltiples variantes
    collision_report = {
        loc_id: sorted(list(names))
        for loc_id, names in variants.items()
        if len(names) > 1
    }
    OUT_REPORT.write_text(json.dumps(collision_report, ensure_ascii=False, indent=2), encoding="utf-8")

if __name__ == "__main__":
    main()
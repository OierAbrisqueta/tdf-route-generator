import pytest
import json
import tempfile
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.app.infrastructure.repositories.LocationRepository import LocationRepository


@pytest.fixture
def sample_locations():
    return [
        {"id": "1", "zone": "norte", "tags": ["playa", "turismo"]},
        {"id": "2", "zone": "sur", "tags": ["montaña"]},
        {"id": "3", "zone": "norte", "tags": ["playa", "familiar"]}
    ]


@pytest.fixture
def temp_json_file(sample_locations):
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_locations, f)
        return f.name


@pytest.fixture
def repo(temp_json_file):
    # Resetear el Singleton antes de cada test
    LocationRepository._instance = None
    # Crear instancia y asignar el path manualmente
    instance = LocationRepository()
    instance.file_path = temp_json_file
    instance._locations = None  # Forzar recarga
    instance.load_locations()
    return instance


def test_get_locations(repo):
    assert len(repo.get_locations()) == 3


def test_get_by_zone(repo):
    result = repo.get_by_zone("norte")
    assert len(result) == 2


def test_get_by_id(repo):
    result = repo.get_by_id("1")
    assert result["zone"] == "norte"


def test_get_by_tags_all(repo):
    result = repo.get_by_tags_all(["playa", "turismo"])
    assert len(result) == 1

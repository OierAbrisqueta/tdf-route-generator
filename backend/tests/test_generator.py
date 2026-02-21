import pytest
from backend.app.infrastructure.repositories.LocationRepository import LocationRepository
from backend.app.api.services.generator import RouteGenerator
from backend.app.api.schemas.requests import GenerateRequest


@pytest.fixture
def location_repository():
    return LocationRepository()


@pytest.fixture
def generator(location_repository):
    return RouteGenerator(location_repository)


@pytest.fixture
def default_request():
    return GenerateRequest(
        stages=21,
        mountain_bias=0.5,
        itt_count=2,
        ttt_enabled=True,
        foreign_start=False,
        foreign_stages_min=2,
        foreign_stages_max=5
    )


def test_generate_returns_correct_number_of_stages(generator, default_request):
    """Verifica que se generan el número correcto de etapas"""
    response = generator.generate(default_request)
    assert len(response.stages) == default_request.stages


def test_generate_returns_seed(generator, default_request):
    """Verifica que se devuelve un seed"""
    response = generator.generate(default_request)
    assert response.seed is not None
    assert isinstance(response.seed, int)


def test_generate_with_same_seed_returns_same_route(generator):
    """Verifica que el mismo seed genera la misma ruta"""
    request = GenerateRequest(
        stages=21,
        mountain_bias=0.5,
        itt_count=2,
        ttt_enabled=True,
        foreign_start=False,
        foreign_stages_min=2,
        foreign_stages_max=5,
        seed=12345
    )

    response1 = generator.generate(request)
    response2 = generator.generate(request)

    assert response1.seed == response2.seed
    assert len(response1.stages) == len(response2.stages)
    for s1, s2 in zip(response1.stages, response2.stages):
        assert s1.start_location.name == s2.start_location.name
        assert s1.finish_location.name == s2.finish_location.name


def test_last_stage_finishes_in_paris(generator, default_request):
    """Verifica que la última etapa termina en París"""
    response = generator.generate(default_request)
    last_stage = response.stages[-1]
    assert last_stage.finish_location.name.lower() == "paris"


def test_stages_have_valid_locations(generator, default_request):
    """Verifica que todas las etapas tienen localizaciones válidas"""
    response = generator.generate(default_request)

    for stage in response.stages:
        assert stage.start_location.name != ""
        assert stage.finish_location.name != ""
        assert stage.start_location.id != ""
        assert stage.finish_location.id != ""


def test_summary_is_generated(generator, default_request):
    """Verifica que se genera el resumen del tour"""
    response = generator.generate(default_request)

    assert response.summary is not None
    assert response.summary.total_stages == default_request.stages
    assert response.summary.total_distance_km > 0
    assert len(response.summary.countries_visited) > 0

from fastapi import APIRouter, Depends
from ..schemas.requests import GenerateRequest
from ..schemas.response import GenerateResponse
from ..services.generator import RouteGenerator
from ...infrastructure.repositories.LocationRepository import LocationRepository

router = APIRouter()


def get_route_generator() -> RouteGenerator:
    repository = LocationRepository()
    return RouteGenerator(repository)


@router.post("/generate", response_model=GenerateResponse)
def generate(
    request: GenerateRequest,
    generator: RouteGenerator = Depends(get_route_generator),
):

    return generator.generate(request)

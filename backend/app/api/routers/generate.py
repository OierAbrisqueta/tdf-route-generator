from fastapi import APIRouter
from ..schemas.requests import GenerateRequest
from ..schemas.response import GenerateResponse
from ..services.generator import generate_tour

router = APIRouter()


@router.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    """
    Genera un Tour de Francia aleatorio basado en los settings.

    - Si no pasas `seed`, se genera uno nuevo.
    - Si pasas `seed`, obtienes el mismo Tour (reproducible).
    """
    return generate_tour(request)
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """Comprueba que la API está funcionando."""
    return {"status": "ok"}
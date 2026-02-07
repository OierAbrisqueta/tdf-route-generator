from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routers import health_router, generate_router

app = FastAPI(
    title="Tour de France Generator API",
    description="Genera Tours de Francia aleatorios pero realistas",
    version="0.1.0",
)

# CORS (para que el frontend pueda llamar desde otro puerto/dominio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, pon tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rutas
app.include_router(health_router, tags=["Health"])
app.include_router(generate_router, tags=["Generator"])


# Para correr directamente con `python api/main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
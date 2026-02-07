from pydantic import BaseModel, Field
from typing import Optional


class GenerateRequest(BaseModel):
    """Settings que manda el frontend para generar un Tour."""

    stages: int = Field(default=21, ge=7, le=21, description="Número de etapas")
    foreign_start: bool = Field(default=True, description="¿Empieza fuera de Francia?")
    foreign_stages_min: int = Field(default=3, ge=1, le=5)
    foreign_stages_max: int = Field(default=5, ge=1, le=5)
    itt_count: int = Field(default=1, ge=0, le=2, description="Número de contrarrelojes individuales")
    ttt_enabled: bool = Field(default=False, description="¿Incluir contrarreloj por equipos?")
    mountain_bias: float = Field(default=0.5, ge=0.0, le=1.0, description="0=más llano, 1=más montaña")
    seed: Optional[int] = Field(default=None, description="Seed para reproducibilidad")
from pydantic import BaseModel
from typing import Optional

class TipoEmpleadoBase(BaseModel):
    tipo: str
    horas_por_dia_max: int
    horas_semanales: int

class TipoEmpleadoResponse(TipoEmpleadoBase):
    id: int

    model_config = {"from_attributes": True}

class TipoEmpleadoUpdate(BaseModel):
    tipo: Optional[str] = None
    horas_por_dia_max: Optional[int] = None
    horas_semanales: Optional[int] = None

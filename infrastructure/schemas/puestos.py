from pydantic import BaseModel
from datetime import date
from typing import Optional

class PuestoBase(BaseModel):
    sucursal_id: int
    rol_colaborador_id: int
    dia_id: int
    fecha: date
    nombre: str
    # En la fase de asignación se asigna el colaborador; inicialmente puede ser None
    colaborador_id: Optional[int] = None

class PuestoUpdate(BaseModel):
    id: int
    sucursal_id: Optional[int] = None
    rol_colaborador_id: Optional[int] = None
    dia_id: Optional[int] = None
    fecha: Optional[date] = None
    nombre: Optional[str] = None
    colaborador_id: Optional[int] = None

class PuestoResponse(PuestoBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            date: lambda v: v.isoformat(),
        }
    }

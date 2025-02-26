from pydantic import BaseModel
from typing import Optional

class ColaboradorBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    dni: int
    empresa_id: int
    tipo_empleado_id: int
    horario_corrido: bool
    legajo: int

class ColaboradorResponse(ColaboradorBase):
    id: int

    model_config = {"from_attributes": True}

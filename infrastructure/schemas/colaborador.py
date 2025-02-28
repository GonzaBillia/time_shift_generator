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

class ColaboradorUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    telefono: Optional[str] = None
    dni: Optional[int] = None
    empresa_id: Optional[int] = None
    tipo_empleado_id: Optional[int] = None
    horario_corrido: Optional[bool] = None
    legajo: Optional[int] = None

class ColaboradorResponse(ColaboradorBase):
    id: int

    model_config = {"from_attributes": True}

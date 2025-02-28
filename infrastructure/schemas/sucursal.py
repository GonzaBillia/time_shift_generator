from pydantic import BaseModel
from typing import Optional

class SucursalBase(BaseModel):
    nombre: str
    direccion: str
    telefono: Optional[str] = None
    empresa_id: int
    formato_id: int

class SucursalUpdate(BaseModel):
    nombre: Optional[str]
    direccion: Optional[str]
    telefono: Optional[str] = None
    empresa_id: Optional[int]
    formato_id: Optional[int]

class SucursalResponse(SucursalBase):
    id: int

    model_config = {"from_attributes": True}

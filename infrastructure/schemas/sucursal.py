from pydantic import BaseModel
from typing import Optional

class SucursalBase(BaseModel):
    nombre: str
    direccion: str
    telefono: Optional[str] = None
    empresa_id: int
    formato_id: int

class SucursalResponse(SucursalBase):
    id: int

    class Config:
        orm_mode = True

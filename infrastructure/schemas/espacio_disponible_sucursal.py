from pydantic import BaseModel
from typing import Optional

class EspacioDisponibleSucursalBase(BaseModel):
    sucursal_id: int
    rol_colaborador_id: int
    cantidad: int
    limitado_por_pc: bool

class EspacioDisponibleSucursalUpdate(BaseModel):
    sucursal_id: Optional[int]
    rol_colaborador_id: Optional[int]
    cantidad: Optional[int]
    limitado_por_pc: Optional[bool]

class EspacioDisponibleSucursalResponse(EspacioDisponibleSucursalBase):
    id: int

    model_config = {"from_attributes": True}

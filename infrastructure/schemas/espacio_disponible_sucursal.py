from pydantic import BaseModel
from typing import Optional

class EspacioDisponibleSucursalBase(BaseModel):
    sucursal_id: int
    rol_colaborador_id: int
    cantidad: int
    limitado_por_pc: bool

class EspacioDisponibleSucursalUpdate(BaseModel):
    id: Optional[int] = None 
    sucursal_id: Optional[int] = None
    rol_colaborador_id: Optional[int] = None
    cantidad: Optional[int] = None
    limitado_por_pc: Optional[bool] = None

class EspacioDisponibleSucursalResponse(EspacioDisponibleSucursalBase):
    id: int

    model_config = {"from_attributes": True}

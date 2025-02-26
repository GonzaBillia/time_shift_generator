from pydantic import BaseModel

class EspacioDisponibleSucursalBase(BaseModel):
    sucursal_id: int
    rol_colaborador_id: int
    cantidad: int
    limitado_por_pc: bool

class EspacioDisponibleSucursalResponse(EspacioDisponibleSucursalBase):
    id: int

    class Config:
        orm_mode = True

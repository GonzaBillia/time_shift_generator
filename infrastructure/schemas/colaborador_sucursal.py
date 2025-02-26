from pydantic import BaseModel

class ColaboradorSucursalBase(BaseModel):
    colaborador_id: int
    sucursal_id: int
    rol_colaborador_id: int

class ColaboradorSucursalResponse(ColaboradorSucursalBase):
    id: int

    class Config:
        orm_mode = True

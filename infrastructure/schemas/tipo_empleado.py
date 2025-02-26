from pydantic import BaseModel

class TipoEmpleadoBase(BaseModel):
    tipo: str
    horas_por_dia_max: int
    horas_semanales: int

class TipoEmpleadoResponse(TipoEmpleadoBase):
    id: int

    class Config:
        orm_mode = True

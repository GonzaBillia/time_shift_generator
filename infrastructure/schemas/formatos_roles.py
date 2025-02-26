from pydantic import BaseModel

class FormatosRolesBase(BaseModel):
    rol_colaborador_id: int
    formato_id: int

class FormatosRolesResponse(FormatosRolesBase):
    # Al ser una clave compuesta, no se define un campo "id" adicional.
    class Config:
        orm_mode = True

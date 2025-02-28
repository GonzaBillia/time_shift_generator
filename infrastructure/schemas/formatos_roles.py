from pydantic import BaseModel

class FormatosRolesBase(BaseModel):
    rol_colaborador_id: int
    formato_id: int

class FormatosRolesResponse(FormatosRolesBase):
    model_config = {"from_attributes": True}

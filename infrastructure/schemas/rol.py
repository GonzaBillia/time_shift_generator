from pydantic import BaseModel

class RolBase(BaseModel):
    nombre: str
    principal: bool

class RolResponse(RolBase):
    id: int

    model_config = {"from_attributes": True}

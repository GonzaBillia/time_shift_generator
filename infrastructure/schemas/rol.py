from pydantic import BaseModel

class RolBase(BaseModel):
    nombre: str
    principal: bool

class RolResponse(RolBase):
    id: int

    class Config:
        orm_mode = True

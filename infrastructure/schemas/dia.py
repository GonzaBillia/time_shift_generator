from pydantic import BaseModel

class DiaBase(BaseModel):
    nombre: str

class DiaResponse(DiaBase):
    id: int

    class Config:
        orm_mode = True

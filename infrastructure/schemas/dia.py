from pydantic import BaseModel

class DiaBase(BaseModel):
    nombre: str

class DiaResponse(DiaBase):
    id: int

    model_config = {"from_attributes": True}

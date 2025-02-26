from pydantic import BaseModel

class EmpresaBase(BaseModel):
    razon_social: str
    cuit: str

class EmpresaResponse(EmpresaBase):
    id: int

    class Config:
        orm_mode = True

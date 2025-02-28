from pydantic import BaseModel
from typing import Optional

class EmpresaBase(BaseModel):
    razon_social: str
    cuit: str

class EmpresaResponse(EmpresaBase):
    id: int

    model_config = {"from_attributes": True}

class EmpresaUpdate(BaseModel):
    razon_social: Optional[str] = None
    cuit: Optional[str] = None

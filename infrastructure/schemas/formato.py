from pydantic import BaseModel, field_validator
from typing import List
from .rol import RolResponse

class FormatoBase(BaseModel):
    nombre: str

class FormatoResponse(FormatoBase):
    id: int
    roles: List[RolResponse]

    model_config = {"from_attributes": True}

    @field_validator("roles", mode="before")
    def extract_roles(cls, v):
        """
        Si 'v' es una lista de objetos FormatosRoles, se extrae su atributo 'rol'.
        """
        # Si ya es una lista de diccionarios o de RolResponse, se retorna tal cual.
        if not v:
            return []
        # Asumimos que 'v' es una lista de FormatosRoles y cada uno tiene el atributo 'rol'
        return [item.rol for item in v if item.rol is not None]
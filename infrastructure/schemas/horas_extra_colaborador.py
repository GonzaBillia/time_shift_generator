from pydantic import BaseModel

class HorasExtraColaboradorBase(BaseModel):
    colaborador_id: int
    tipo: str  # Se puede usar un Enum si se desea
    cantidad: int

class HorasExtraColaboradorResponse(HorasExtraColaboradorBase):
    id: int

    model_config = {"from_attributes": True}

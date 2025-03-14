# application/schemas/venta_hora.py
from pydantic import BaseModel, Field, validator
from datetime import date, time, timedelta
from typing import Optional, List

class VentaHora(BaseModel):
    Sucursal: int
    Doc: str
    Documento: str
    Fecha: date
    Hora: time
    Usuario: Optional[int]
    Efectivo: Optional[float]
    CtaCte: Optional[float]
    OSocial: Optional[float]
    obra_social_detalle: Optional[str] = Field(None, alias="Obra Social Detalle")
    Tarjeta: Optional[float]
    OtrosMP: Optional[float]
    tarjeta_detalle: Optional[str] = Field(None, alias="Tarjeta Detalle")
    Total: float
    apellido_y_nombre: Optional[str] = Field(None, alias="Apellido y nombre/Razón Social")
    DNI: Optional[str]
    CUIT: Optional[str]

    @validator("Hora", pre=True)
    def convert_value_to_time(cls, v):
        """
        Convierte un valor recibido (ya sea timedelta, float o int) en un objeto time.
        Se asume que:
          - Si es timedelta: se toman sus segundos totales.
          - Si es float o int: se interpreta como segundos desde medianoche.
        """
        if isinstance(v, timedelta):
            total_seconds = int(v.total_seconds())
        elif isinstance(v, (int, float)):
            total_seconds = int(v)
        else:
            return v  # Deja pasar si ya es un objeto time u otro tipo compatible

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return time(hour=hours, minute=minutes, second=seconds)


class VentaHoraResponse(BaseModel):
    data: List[VentaHora]

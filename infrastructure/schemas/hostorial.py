from pydantic import BaseModel
from datetime import date, time
from typing import List
# Importa tus esquemas de puestos y horarios (ajusta la ruta según tu proyecto)
from infrastructure.schemas.puestos import PuestoResponse  
from infrastructure.schemas.horario import HorarioBase  

class WeekRange(BaseModel):
    start: date
    end: date

class CopyHistoryRequest(BaseModel):
    sucursal_id: int
    origin_week: WeekRange
    destination_weeks: List[WeekRange]
    resources: List[PuestoResponse]   # Se asume que cada recurso incluye el campo 'id'
    events: List[HorarioBase]     # Se asume que cada evento incluye el campo 'puesto_id'

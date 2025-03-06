# services/horario_service.py
from domain.models.horario import Horario
from datetime import date, time

def crear_horario(
    sucursal_id: int,
    colaborador_id: int,
    dia_id: int,
    fecha: date,
    hora_inicio: time,
    hora_fin: time,
    horario_corrido: bool
) -> Horario:
    """
    Crea una instancia de Horario a partir de un único bloque de tiempo.
    Se puede extender para agrupar varios bloques si la lógica de negocio lo requiere.
    """
    bloques = [(hora_inicio, hora_fin)]
    return Horario(
        sucursal_id=sucursal_id,
        colaborador_id=colaborador_id,
        dia_id=dia_id,
        fecha=fecha,
        bloques=bloques,
        horario_corrido=horario_corrido
    )

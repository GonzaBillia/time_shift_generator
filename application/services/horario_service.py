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


def crear_horario_preferido(
    sucursal_id: int,
    colaborador_id: int,
    dia_id: int,
    hora_inicio: time,
    hora_fin: time,
    horario_corrido: bool
) -> Horario:
    """
    Crea una instancia de Horario para un horario preferido, que no depende de una fecha específica.
    Se puede extender para agrupar varios bloques si la lógica de negocio lo requiere.
    """
    bloques = [(hora_inicio, hora_fin)]
    return Horario(
        sucursal_id=sucursal_id,
        colaborador_id=colaborador_id,
        dia_id=dia_id,
        fecha=None,  # Se indica que no hay una fecha específica para el horario preferido.
        bloques=bloques,
        horario_corrido=horario_corrido
    )

def convertir_horario_a_dict(horario: object, id_val: int = 0) -> dict:
    if not horario.bloques:
        raise ValueError("El horario debe tener al menos un bloque de tiempo.")
    hora_inicio, hora_fin = horario.bloques[0]
    return {
        "id": id_val,
        "colaborador_id": horario.colaborador_id,
        "sucursal_id": horario.sucursal_id,
        "hora_inicio": hora_inicio.isoformat() if hasattr(hora_inicio, "isoformat") else hora_inicio,
        "hora_fin": hora_fin.isoformat() if hasattr(hora_fin, "isoformat") else hora_fin,
        "dia_id": horario.dia_id,
        "horario_corrido": horario.horario_corrido,
    }



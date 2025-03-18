# horario_mapper.py
from domain.models.horario import Horario

def horario_to_dict(horario: Horario) -> dict:
    """
    Convierte un objeto de dominio Horario en un diccionario
    que contenga únicamente los campos mapeados en el modelo ORM.
    """
    if not horario.bloques:
        raise ValueError("El horario debe tener al menos un bloque de tiempo.")
    hora_inicio, hora_fin = horario.bloques[0]
    return {
        "id": 0,  # O el valor correspondiente
        "colaborador_id": horario.colaborador_id,
        "rol_colaborador_id": horario.rol_colaborador_id,
        "sucursal_id": horario.sucursal_id,
        "hora_inicio": hora_inicio.isoformat() if hasattr(hora_inicio, "isoformat") else hora_inicio,
        "hora_fin": hora_fin.isoformat() if hasattr(hora_fin, "isoformat") else hora_fin,
        "dia_id": horario.dia_id,
        "horario_corrido": horario.horario_corrido,
    }

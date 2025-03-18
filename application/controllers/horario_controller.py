from typing import List
from fastapi import HTTPException
from application.config.logger_config import setup_logger
from infrastructure.databases.models.horario import Horario as HorarioORM
from infrastructure.repositories.horario_repo import HorarioRepository
from application.services.horario_service import crear_horarios, actualizar_horarios

logger = setup_logger(__name__, "logs/horario.log")

def controlador_py_logger_crear_horarios(horarios_front: List[dict], db=None) -> List[HorarioORM]:
    """
    Controlador para crear en bloque los bloques horarias (Horarios).
    Se espera una lista de diccionarios que contengan 'puesto_id', 'hora_inicio', 'hora_fin'
    y 'horario_corrido'.
    """
    try:
        resultados = crear_horarios(horarios_front, db)
        logger.info("Bloques horarias creados exitosamente.")
        return resultados
    except Exception as error:
        logger.error("Error al crear bloques horarias: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_actualizar_horarios(horarios_front: List[dict], db=None) -> List[HorarioORM]:
    """
    Controlador para actualizar en bloque los bloques horarias existentes.
    Se espera que cada objeto incluya 'id' y 'puesto_id' junto con la información de hora_inicio, hora_fin y horario_corrido.
    """
    try:
        resultados = actualizar_horarios(horarios_front, db)
        logger.info("Bloques horarias actualizados exitosamente.")
        return resultados
    except Exception as error:
        logger.error("Error al actualizar bloques horarias: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_get_by_puesto(puesto_id: int) -> List[HorarioORM]:
    """
    Devuelve todos los bloques horarias asociados a un puesto específico.
    """
    try:
        horarios = HorarioRepository.get_by_puesto(puesto_id)
    except Exception as error:
        logger.error("Error al obtener horarios para el puesto %s: %s", puesto_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not horarios:
        logger.warning("No se encontraron bloques horarias para el puesto %s", puesto_id)
        return []
    return horarios

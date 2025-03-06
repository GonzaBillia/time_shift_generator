from application.config.logger_config import setup_logger
from typing import List
from fastapi import HTTPException
from infrastructure.databases.models.horario_preferido_colaborador import HorarioPreferidoColaborador
from infrastructure.repositories.horario_preferido_colaborador_repo import HorarioPreferidoColaboradorRepository

logger = setup_logger(__name__, "logs/horario_preferido_colaborador.log")

def controlador_py_logger_get_by_id_horario_preferido_colaborador(horario_id: int) -> HorarioPreferidoColaborador:
    """
    Obtiene un HorarioPreferidoColaborador por su ID.
    """
    try:
        horario = HorarioPreferidoColaboradorRepository.get_by_id(horario_id)
    except Exception as error:
        logger.error("Error al obtener HorarioPreferidoColaborador con id %s: %s", horario_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not horario:
        logger.warning("HorarioPreferidoColaborador no encontrado con id %s", horario_id)
        raise HTTPException(status_code=404, detail="HorarioPreferidoColaborador no encontrado")

    return horario

def controlador_py_logger_get_by_colaborador(colaborador_id: int) -> List[HorarioPreferidoColaborador]:
    """
    Obtiene todos los HorarioPreferidoColaborador asociados a un colaborador.
    """
    try:
        horarios = HorarioPreferidoColaboradorRepository.get_by_colaborador(colaborador_id)
    except Exception as error:
        logger.error("Error al obtener HorarioPreferidoColaborador para colaborador %s: %s", colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horarios

def controlador_py_logger_get_by_dia(dia_id: int) -> List[HorarioPreferidoColaborador]:
    """
    Obtiene todos los HorarioPreferidoColaborador para un día específico.
    """
    try:
        horarios = HorarioPreferidoColaboradorRepository.get_by_dia(dia_id)
    except Exception as error:
        logger.error("Error al obtener HorarioPreferidoColaborador para día %s: %s", dia_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horarios

def controlador_py_logger_create_horario_preferido_colaborador(horario: HorarioPreferidoColaborador) -> HorarioPreferidoColaborador:
    """
    Crea un nuevo HorarioPreferidoColaborador en la base de datos.
    """
    try:
        nuevo = HorarioPreferidoColaboradorRepository.create(horario)
        logger.info("HorarioPreferidoColaborador creado exitosamente con id %s", nuevo.id)
        return nuevo
    except Exception as error:
        logger.error("Error al crear HorarioPreferidoColaborador: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_horario_preferido_colaborador(horario: HorarioPreferidoColaborador) -> HorarioPreferidoColaborador:
    """
    Actualiza un HorarioPreferidoColaborador existente.
    Retorna el objeto actualizado o levanta error si no existe.
    """
    try:
        existente = HorarioPreferidoColaboradorRepository.get_by_id(horario.id)
        if not existente:
            logger.warning("HorarioPreferidoColaborador no encontrado para actualizar con id %s", horario.id)
            raise HTTPException(status_code=404, detail="HorarioPreferidoColaborador no encontrado")
        
        actualizado = HorarioPreferidoColaboradorRepository.update(horario)
    except Exception as error:
        logger.error("Error al actualizar HorarioPreferidoColaborador con id %s: %s", horario.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not actualizado:
        logger.warning("HorarioPreferidoColaborador no encontrado tras actualización con id %s", horario.id)
        raise HTTPException(status_code=404, detail="HorarioPreferidoColaborador no encontrado")
    
    logger.info("HorarioPreferidoColaborador actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_py_logger_delete_horario_preferido_colaborador(horario_id: int) -> bool:
    """
    Elimina un HorarioPreferidoColaborador por su ID.
    """
    try:
        eliminado = HorarioPreferidoColaboradorRepository.delete(horario_id)
    except Exception as error:
        logger.error("Error al eliminar HorarioPreferidoColaborador con id %s: %s", horario_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("HorarioPreferidoColaborador no encontrado para eliminar con id %s", horario_id)
        raise HTTPException(status_code=404, detail="HorarioPreferidoColaborador no encontrado")
    
    logger.info("HorarioPreferidoColaborador eliminado exitosamente con id %s", horario_id)
    return eliminado

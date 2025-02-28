# CONTROLLER_PY_LOGGER_HORAS_EXTRA_COLABORADOR
from application.config.logger_config import setup_logger
from typing import List
from fastapi import HTTPException
from infrastructure.databases.models.horas_extra_colaborador import HorasExtraColaborador
from infrastructure.repositories.horas_extra_colaborador_repo import HorasExtraColaboradorRepository

logger = setup_logger(__name__, "logs/horas_extra_colaborador.log")

def controlador_py_logger_get_by_colaborador_horas_extra(colaborador_id: int) -> List[HorasExtraColaborador]:
    """
    Devuelve todas las horas extra para un colaborador específico.
    """
    try:
        horas_extra = HorasExtraColaboradorRepository.get_by_colaborador(colaborador_id)
    except Exception as error:
        logger.error("Error al obtener horas extra para colaborador %s: %s", colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horas_extra

def controlador_py_logger_get_by_tipo_horas_extra(colaborador_id: int, tipo: str) -> List[HorasExtraColaborador]:
    """
    Devuelve todas las horas extra para un colaborador filtradas por tipo.
    """
    try:
        horas_extra = HorasExtraColaboradorRepository.get_by_tipo(colaborador_id, tipo)
    except Exception as error:
        logger.error("Error al obtener horas extra para colaborador %s y tipo %s: %s", colaborador_id, tipo, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horas_extra

def controlador_py_logger_create_horas_extra(horas_extra: HorasExtraColaborador) -> HorasExtraColaborador:
    """
    Crea un nuevo registro de horas extra para un colaborador.
    """
    try:
        nuevo_registro = HorasExtraColaboradorRepository.create(horas_extra)
        logger.info("Horas extra creadas exitosamente con id %s", nuevo_registro.id)
        return nuevo_registro
    except Exception as error:
        logger.error("Error al crear horas extra: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_delete_horas_extra(horas_extra_id: int) -> bool:
    """
    Elimina un registro de horas extra por su ID.
    """
    try:
        eliminado = HorasExtraColaboradorRepository.delete(horas_extra_id)
    except Exception as error:
        logger.error("Error al eliminar horas extra con id %s: %s", horas_extra_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("Horas extra no encontradas para eliminar con id %s", horas_extra_id)
        raise HTTPException(status_code=404, detail="Horas extra no encontradas")
    
    logger.info("Horas extra eliminadas exitosamente con id %s", horas_extra_id)
    return eliminado

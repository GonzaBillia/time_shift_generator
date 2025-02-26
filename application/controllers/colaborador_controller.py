from application.config.logger_config import setup_logger
from typing import Optional, List
from fastapi import HTTPException
from infrastructure.databases.models import Colaborador
from infrastructure.repositories.colaborador_repo import ColaboradorRepository  # Ajusta el path según tu estructura

logger = setup_logger(__name__)

def controlador_py_logger_get_all() -> List[Colaborador]:
    """
    Obtiene todos los colaboradores.

    Returns:
        List[Colaborador]: Lista de colaboradores.

    Raises:
        HTTPException: Con código 500 si ocurre un error interno.
    """
    try:
        colaboradores = ColaboradorRepository.get_all()
    except Exception as error:
        logger.error("Error al obtener todos los colaboradores: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    return colaboradores

def controlador_py_logger_get_filtered(
    dni: Optional[int] = None,
    empresa_id: Optional[int] = None,
    tipo_empleado_id: Optional[int] = None,
    horario_corrido: Optional[bool] = None,
) -> List[Colaborador]:
    """
    Obtiene colaboradores aplicando filtros opcionales.

    Args:
        dni (Optional[int]): DNI del colaborador.
        empresa_id (Optional[int]): ID de la empresa.
        tipo_empleado_id (Optional[int]): ID del tipo de empleado.
        horario_corrido (Optional[bool]): Indicador de horario corrido.

    Returns:
        List[Colaborador]: Lista de colaboradores que cumplen los filtros.

    Raises:
        HTTPException: Con código 500 si ocurre un error interno.
    """
    try:
        colaboradores = ColaboradorRepository.get_filtered(
            dni=dni,
            empresa_id=empresa_id,
            tipo_empleado_id=tipo_empleado_id,
            horario_corrido=horario_corrido,
        )
    except Exception as error:
        logger.error("Error al obtener colaboradores filtrados: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    return colaboradores

def controlador_py_logger_get_by_id(colaborador_id: int) -> Colaborador:
    """
    Obtiene un colaborador por su ID.

    Args:
        colaborador_id (int): Identificador del colaborador.

    Returns:
        Colaborador: Objeto Colaborador obtenido.

    Raises:
        HTTPException: Con código 404 si no se encuentra el colaborador,
                       o con código 500 si ocurre un error interno.
    """
    try:
        colaborador = ColaboradorRepository.get_by_id(colaborador_id)
    except Exception as error:
        logger.error("Error al obtener colaborador con id %s: %s", colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not colaborador:
        logger.warning("Colaborador no encontrado con id %s", colaborador_id)
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")

    return colaborador

def controlador_py_logger_get_by_legajo(colaborador_legajo: int) -> Colaborador:
    """
    Obtiene un colaborador a partir de su legajo.

    Args:
        colaborador_legajo (int): Legajo del colaborador.

    Returns:
        Colaborador: Objeto Colaborador obtenido.

    Raises:
        HTTPException: Con código 404 si no se encuentra el colaborador,
                       o con código 500 si ocurre un error interno.
    """
    try:
        colaborador = ColaboradorRepository.get_by_legajo(colaborador_legajo)
    except Exception as error:
        logger.error("Error al obtener colaborador con legajo %s: %s", colaborador_legajo, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not colaborador:
        logger.warning("Colaborador no encontrado con legajo %s", colaborador_legajo)
        raise HTTPException(status_code=404, detail="Colaborador no encontrado")

    return colaborador
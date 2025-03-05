# CONTROLLER_PY_LOGGER_VTA_HORA
import logging
from typing import List
from fastapi import HTTPException
from datetime import date
from infrastructure.repositories.vta_hora_repo import get_vta_hora as repo_get_vta_hora

logger = logging.getLogger(__name__)

def controlador_py_logger_get_vta_hora(sucursal: int, fecha_desde: date, fecha_hasta: date) -> List[dict]:
    """
    Ejecuta la consulta de ventas/hora usando el archivo SQL get_vta_hora.sql y retorna los resultados.
    
    Args:
        sucursal (int): ID de la sucursal.
        fecha_desde (date): Fecha de inicio del rango.
        fecha_hasta (date): Fecha de fin del rango.
        
    Returns:
        List[dict]: Lista de registros resultantes de la consulta.
        
    Raises:
        HTTPException: En caso de error interno.
    """
    try:
        data = repo_get_vta_hora(sucursal, fecha_desde, fecha_hasta)
        return data
    except Exception as error:
        logger.error("Error al obtener vta_hora para sucursal %s, desde %s hasta %s: %s", 
                     sucursal, fecha_desde, fecha_hasta, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

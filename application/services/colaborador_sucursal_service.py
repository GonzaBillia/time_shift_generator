import logging
from typing import List
from sqlalchemy.orm import Session

from infrastructure.repositories.colaborador_sucursal_repo import ColaboradorSucursalRepository
from infrastructure.repositories.sucursal_repo import SucursalRepository
from infrastructure.repositories.colaborador_repo import ColaboradorRepository
from infrastructure.schemas.sucursal import SucursalResponse
from infrastructure.schemas.colaborador_sucursal import ColaboradorSucursalDetail
from infrastructure.repositories.rol_repo import RolRepository

logger = logging.getLogger(__name__)

def get_sucursales_by_colaborador(colaborador_id: int, db: Session) -> List[SucursalResponse]:
    """
    Obtiene las sucursales en las que está asignado un colaborador.
    
    1. Se obtienen las relaciones 'ColaboradorSucursal' para el colaborador.
    2. Se itera sobre cada relación para obtener el 'sucursal_id'.
    3. Por cada 'sucursal_id' se llama a SucursalRepository.get_by_id para obtener la sucursal completa.
    4. Se retorna una lista de sucursales.
    
    Args:
        colaborador_id (int): ID del colaborador.
        db (Session): Sesión activa para la consulta.
    
    Returns:
        List[SucursalResponse]: Lista de objetos Sucursal.
    """
    try:
        relaciones = ColaboradorSucursalRepository.get_by_colaborador(colaborador_id, db)
    except Exception as e:
        logger.error("Error obteniendo relaciones para colaborador %s: %s", colaborador_id, e)
        raise e

    sucursales = []
    for relacion in relaciones:
        sucursal_id = relacion.sucursal_id
        sucursal = SucursalRepository.get_by_id(sucursal_id, db)
        if sucursal:
            sucursales.append(sucursal)
        else:
            logger.warning("No se encontró sucursal con id %s", sucursal_id)
    return sucursales

def get_colaboradores_by_sucursal(sucursal_id: int, db: Session) -> List[ColaboradorSucursalDetail]:
    """
    Obtiene la lista de colaboradores asociados a una sucursal, añadiéndoles la información del rol.
    
    Args:
        sucursal_id (int): ID de la sucursal.
        db (Session): Sesión activa para la consulta.
        
    Returns:
        List[ColaboradorSucursalDetail]: Lista de diccionarios con información del colaborador y su rol.
    """
    try:
        relaciones = ColaboradorSucursalRepository.get_by_sucursal(sucursal_id, db)
        if not isinstance(relaciones, list):
            relaciones = [relaciones]
    except Exception as e:
        logger.error("Error obteniendo relaciones para sucursal %s: %s", sucursal_id, e)
        raise e

    resultados = []
    for relacion in relaciones:
        colaborador_id = relacion.colaborador_id
        rol_id = relacion.rol_colaborador_id  # Se asume que este campo existe en la relación
        try:
            # Se obtiene el colaborador y su rol pasando la sesión
            colaborador = ColaboradorRepository.get_by_id(colaborador_id, db)
            rol = RolRepository.get_by_id(rol_id, db) if rol_id is not None else None
        except Exception as e:
            logger.error("Error obteniendo colaborador o rol para id %s: %s", colaborador_id, e)
            continue  # Se continúa con la siguiente relación en caso de error
        if colaborador:
            # Convertir el colaborador a dict usando model_dump o vars()
            colaborador_dict = (
                colaborador.model_dump() if hasattr(colaborador, "model_dump") else vars(colaborador)
            )
            # Convertir el rol a dict (si existe)
            rol_dict = (
                rol.model_dump() if rol and hasattr(rol, "model_dump") else (vars(rol) if rol else None)
            )
            # Crear una estructura con la clave 'colaborador' y 'rol'
            resultados.append({
                "colaborador": colaborador_dict,
                "rol": rol_dict
            })
        else:
            logger.warning("Colaborador no encontrado con id %s", colaborador_id)
    return resultados

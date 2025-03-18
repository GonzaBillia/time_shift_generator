# services/rol_service.py

from infrastructure.repositories.rol_repo import RolRepository
import logging

logger = logging.getLogger(__name__)

def get_available_roles_service(sucursal_id: int):
    """
    Servicio que obtiene los roles disponibles para una sucursal específica.
    Se invoca al repositorio que realiza la consulta y retorna la lista de roles.
    """
    try:
        roles = RolRepository.get_available_rols_by_sucursal(sucursal_id)
        if not roles:
            logger.warning("No se encontraron roles disponibles para la sucursal con id %s", sucursal_id)
        return roles
    except Exception as error:
        logger.error("Error en el servicio al obtener roles para la sucursal %s: %s", sucursal_id, error)
        raise error


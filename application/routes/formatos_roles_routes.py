# ROUTER_PY_SCHEMA_FORMATOS_ROLES
from fastapi import APIRouter, HTTPException, Query
from typing import List
from infrastructure.schemas.formatos_roles import FormatosRolesResponse, FormatosRolesBase
from infrastructure.databases.models.formato_rol import FormatosRoles
from infrastructure.schemas.rol import RolResponse
from application.controllers.formatos_roles_controller import (
    controlador_py_logger_get_by_ids,
    controlador_py_logger_get_all_formatos_roles,
    controlador_py_logger_create_formatos_roles,
    controlador_py_logger_delete_formatos_roles,
    controlador_py_logger_get_by_formatos,
    controlador_py_logger_get_roles_by_formato
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

router = APIRouter(prefix="/formatos_roles", tags=["FormatosRoles"])
logger = setup_logger(__name__, "logs/formato_rol.log")

@router.get("/", response_model=List[FormatosRolesResponse])
def get_all_formatos_roles():
    """
    Endpoint para obtener todos los registros de FormatosRoles.
    """
    try:
        mappings = controlador_py_logger_get_all_formatos_roles()
        mappings_schema = [FormatosRolesResponse.model_validate(m) for m in mappings]
        data = [ms.model_dump() for ms in mappings_schema]
        return success_response("Registros de FormatosRoles encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_formatos_roles: %s", e)
        return error_response(str(e), status_code=500)
    
@router.get("/formato/{formato_id}", response_model=List[FormatosRolesResponse])
def get_all_formatos_roles(formato_id: int):
    """
    Endpoint para obtener todos los registros de FormatosRoles.
    """
    try:
        mappings = controlador_py_logger_get_by_formatos(formato_id)
        mappings_schema = [FormatosRolesResponse.model_validate(m) for m in mappings]
        data = [ms.model_dump() for ms in mappings_schema]
        return success_response("Registros de FormatosRoles encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_formatos_roles: %s", e)
        return error_response(str(e), status_code=500)
    
@router.get("/formato/{formato_id}/roles", response_model=List[RolResponse])
def get_all_roles_by_formato(formato_id: int):
    """
    Endpoint para obtener todos los registros de FormatosRoles.
    """
    try:
        mappings = controlador_py_logger_get_roles_by_formato(formato_id)
        mappings_schema = [RolResponse.model_validate(m) for m in mappings]
        data = [ms.model_dump() for ms in mappings_schema]
        return success_response("Registros de FormatosRoles encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_formatos_roles: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/ids", response_model=FormatosRolesResponse)
def get_formatos_roles_by_ids(
    rol_colaborador_id: int,
    formato_id: int
):
    """
    Endpoint para obtener un registro de FormatosRoles por su clave compuesta.
    Se reciben los parámetros como query parameters.
    """
    try:
        mapping = controlador_py_logger_get_by_ids(rol_colaborador_id, formato_id)
        mapping_schema = FormatosRolesResponse.model_validate(mapping)
        return success_response("Registro encontrado", data=mapping_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_formatos_roles_by_ids: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=FormatosRolesResponse)
def create_formatos_roles(mapping_data: FormatosRolesBase):
    """
    Endpoint para crear un nuevo registro en FormatosRoles.
    """
    try:
        nuevo_mapping = FormatosRoles(**mapping_data.model_dump())
        mapping_creado = controlador_py_logger_create_formatos_roles(nuevo_mapping)
        mapping_schema = FormatosRolesResponse.model_validate(mapping_creado)
        return success_response("Registro creado exitosamente", data=mapping_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_formatos_roles: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/")
def delete_formatos_roles(rol_colaborador_id: int, formato_id: int):
    """
    Endpoint para eliminar un registro de FormatosRoles por su clave compuesta.
    Se reciben los parámetros como query parameters.
    """
    try:
        resultado = controlador_py_logger_delete_formatos_roles(rol_colaborador_id, formato_id)
        return success_response("Registro eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_formatos_roles: %s", e)
        return error_response(str(e), status_code=500)

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from infrastructure.schemas.rol import RolResponse, RolBase
from infrastructure.databases.models.rol import Rol
from application.controllers.rol_controller import (
    controlador_py_logger_get_by_id_rol,
    controlador_py_logger_get_all_roles,
    controlador_py_logger_create_rol,
    controlador_py_logger_update_rol,
    controlador_py_logger_delete_rol,
    controlador_py_logger_get_by_nombre_rol,
    controlador_py_logger_get_principales,
    controlador_get_available_roles
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/roles", tags=["Roles"])
logger = setup_logger(__name__, "logs/rol.log")

@router.get("/id/{rol_id}", response_model=RolResponse)
def get_rol_by_id(
    rol_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener un Rol por su ID.
    """
    try:
        rol = controlador_py_logger_get_by_id_rol(rol_id, db)
        rol_schema = RolResponse.model_validate(rol)
        return success_response("Rol encontrado", data=rol_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_rol_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/", response_model=List[RolResponse])
def get_all_roles(
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todos los Roles.
    """
    try:
        roles = controlador_py_logger_get_all_roles(db)
        roles_schema = [RolResponse.model_validate(r) for r in roles]
        data = [rs.model_dump() for rs in roles_schema]
        return success_response("Roles encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_roles: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=RolResponse)
def create_rol(
    rol_data: RolBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para crear un nuevo Rol.
    """
    try:
        nuevo_rol = Rol(**rol_data.model_dump())
        rol_creado = controlador_py_logger_create_rol(nuevo_rol, db)
        rol_schema = RolResponse.model_validate(rol_creado)
        return success_response("Rol creado exitosamente", data=rol_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_rol: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{rol_id}", response_model=RolResponse)
def update_rol(
    rol_id: int,
    rol_data: RolBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para actualizar un Rol existente.
    """
    try:
        update_data = rol_data.model_dump()
        update_data["id"] = rol_id
        rol_to_update = Rol(**update_data)
        rol_actualizado = controlador_py_logger_update_rol(rol_to_update, db)
        rol_schema = RolResponse.model_validate(rol_actualizado)
        return success_response("Rol actualizado exitosamente", data=rol_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_rol: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{rol_id}")
def delete_rol(
    rol_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para eliminar un Rol por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_rol(rol_id, db)
        return success_response("Rol eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_rol: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/nombre/{nombre}", response_model=RolResponse)
def get_rol_by_nombre(
    nombre: str,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener un Rol por su nombre.
    """
    try:
        rol = controlador_py_logger_get_by_nombre_rol(nombre, db)
        rol_schema = RolResponse.model_validate(rol)
        return success_response("Rol encontrado", data=rol_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_rol_by_nombre: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/principales", response_model=List[RolResponse])
def get_principales(
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener los Roles marcados como 'principal=True'.
    """
    try:
        roles = controlador_py_logger_get_principales(db)
        roles_schema = [RolResponse.model_validate(r) for r in roles]
        data = [rs.model_dump() for rs in roles_schema]
        return success_response("Roles principales encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_principales: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/available/sucursal/{sucursal_id}", response_model=List[RolResponse])
def get_available_roles_by_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener los roles disponibles para una sucursal a partir de sus espacios disponibles.
    """
    try:
        roles = controlador_get_available_roles(sucursal_id, db)
        roles_schema = [RolResponse.model_validate(r) for r in roles]
        data = [rs.model_dump() for rs in roles_schema]
        return success_response("Roles disponibles encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_available_roles_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)

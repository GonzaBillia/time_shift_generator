from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from infrastructure.schemas.tipo_empleado import (
    TipoEmpleadoResponse, 
    TipoEmpleadoBase, 
    TipoEmpleadoUpdate
)

from infrastructure.databases.models.tipo_colaborador import TipoEmpleado
from application.controllers.tipo_colaborador_controller import (
    controlador_py_logger_get_by_id_tipo_empleado,
    controlador_py_logger_get_all_tipo_empleado,
    controlador_py_logger_create_tipo_empleado,
    controlador_py_logger_update_tipo_empleado,
    controlador_py_logger_delete_tipo_empleado,
    controlador_py_logger_get_by_tipo_tipo_empleado,
    
)
from application.controllers.rol_controller import (
    controlador_get_available_roles,
    controlador_py_logger_get_principales
)

from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/tipo_colaboradores", tags=["TipoEmpleado"])
logger = setup_logger(__name__, "logs/tipo_empleado.log")

@router.get("/id/{tipo_empleado_id}", response_model=TipoEmpleadoResponse)
def get_tipo_empleado_by_id(
    tipo_empleado_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener un TipoEmpleado por su ID.
    """
    try:
        tipo = controlador_py_logger_get_by_id_tipo_empleado(tipo_empleado_id, db)
        tipo_schema = TipoEmpleadoResponse.model_validate(tipo)
        return success_response("TipoEmpleado encontrado", data=tipo_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_tipo_empleado_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/", response_model=List[TipoEmpleadoResponse])
def get_all_tipo_empleados(
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todos los tipos de empleados.
    """
    try:
        tipos = controlador_py_logger_get_all_tipo_empleado(db)
        tipos_schema = [TipoEmpleadoResponse.model_validate(t) for t in tipos]
        data = [ts.model_dump() for ts in tipos_schema]
        return success_response("Tipos de empleados encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_tipo_empleados: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=TipoEmpleadoResponse)
def create_tipo_empleado(
    tipo_data: TipoEmpleadoBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para crear un nuevo TipoEmpleado.
    """
    try:
        nuevo_tipo = TipoEmpleado(**tipo_data.model_dump())
        tipo_creado = controlador_py_logger_create_tipo_empleado(nuevo_tipo, db)
        tipo_schema = TipoEmpleadoResponse.model_validate(tipo_creado)
        return success_response("TipoEmpleado creado exitosamente", data=tipo_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_tipo_empleado: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{tipo_empleado_id}", response_model=TipoEmpleadoResponse)
def update_tipo_empleado_partial(
    tipo_empleado_id: int,
    tipo_update: TipoEmpleadoUpdate,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para actualizar parcialmente un TipoEmpleado existente.
    Solo se actualizarán los campos que se envíen en el body.
    """
    try:
        update_data = tipo_update.dict(exclude_unset=True)
        update_data["id"] = tipo_empleado_id
        tipo_to_update = TipoEmpleado(**update_data)
        tipo_actualizado = controlador_py_logger_update_tipo_empleado(tipo_to_update, db)
        tipo_schema = TipoEmpleadoResponse.model_validate(tipo_actualizado)
        return success_response("TipoEmpleado actualizado exitosamente", data=tipo_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_tipo_empleado: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{tipo_empleado_id}")
def delete_tipo_empleado(
    tipo_empleado_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para eliminar un TipoEmpleado por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_tipo_empleado(tipo_empleado_id, db)
        return success_response("TipoEmpleado eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_tipo_empleado: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/tipo/{tipo}", response_model=TipoEmpleadoResponse)
def get_tipo_empleado_by_tipo(
    tipo: str,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener un TipoEmpleado por su campo 'tipo' (nombre).
    """
    try:
        tipo_empleado = controlador_py_logger_get_by_tipo_tipo_empleado(tipo, db)
        tipo_schema = TipoEmpleadoResponse.model_validate(tipo_empleado)
        return success_response("TipoEmpleado encontrado", data=tipo_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_tipo_empleado_by_tipo: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/principales", response_model=List[TipoEmpleadoResponse])
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
        roles_schema = [TipoEmpleadoResponse.model_validate(r) for r in roles]
        data = [rs.model_dump() for rs in roles_schema]
        return success_response("Roles principales encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_principales: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/available/sucursal/{sucursal_id}", response_model=List[TipoEmpleadoResponse])
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
        roles_schema = [TipoEmpleadoResponse.model_validate(r) for r in roles]
        data = [rs.model_dump() for rs in roles_schema]
        return success_response("Roles disponibles encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_available_roles_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)

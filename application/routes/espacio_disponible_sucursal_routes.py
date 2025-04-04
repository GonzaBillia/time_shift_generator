from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from infrastructure.schemas.espacio_disponible_sucursal import (
    EspacioDisponibleSucursalResponse, 
    EspacioDisponibleSucursalBase, 
    EspacioDisponibleSucursalUpdate
)
from infrastructure.databases.models.espacio_disponible_sucursal import EspacioDisponibleSucursal
from application.controllers.espacio_disponible_sucursal_controller import (
    controlador_py_logger_get_by_id_espacio,
    controlador_py_logger_get_all_espacios,
    controlador_py_logger_get_espacios_by_sucursal,
    controlador_py_logger_get_by_rol,
    controlador_py_logger_create_espacio,
    controlador_py_logger_update_espacio,
    controlador_py_logger_delete_espacio
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/espacios_disponibles", tags=["Espacios Disponibles"])
logger = setup_logger(__name__, "logs/espacio_disponible_sucursal.log")

@router.get("/id/{espacio_id}", response_model=EspacioDisponibleSucursalResponse)
def get_espacio_by_id(
    espacio_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        espacio = controlador_py_logger_get_by_id_espacio(espacio_id, db)
        espacio_schema = EspacioDisponibleSucursalResponse.model_validate(espacio)
        data = jsonable_encoder(espacio_schema.model_dump())
        return success_response("Espacio disponible encontrado", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_espacio_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/", response_model=List[EspacioDisponibleSucursalResponse])
def get_all_espacios(
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        espacios = controlador_py_logger_get_all_espacios(db)
        espacios_schema = [EspacioDisponibleSucursalResponse.model_validate(e) for e in espacios]
        data = [jsonable_encoder(es.model_dump()) for es in espacios_schema]
        return success_response("Espacios disponibles encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_espacios: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/sucursal/{sucursal_id}", response_model=List[EspacioDisponibleSucursalResponse])
def get_espacios_by_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        espacios = controlador_py_logger_get_espacios_by_sucursal(sucursal_id, db)
        espacios_schema = [EspacioDisponibleSucursalResponse.model_validate(e) for e in espacios]
        data = [jsonable_encoder(es.model_dump()) for es in espacios_schema]
        return success_response("Espacios disponibles para la sucursal encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_espacios_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/rol/{sucursal_id}", response_model=EspacioDisponibleSucursalResponse)
def get_espacio_by_rol(
    sucursal_id: int,
    rol_colaborador_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        espacio = controlador_py_logger_get_by_rol(sucursal_id, rol_colaborador_id, db)
        espacio_schema = EspacioDisponibleSucursalResponse.model_validate(espacio)
        data = jsonable_encoder(espacio_schema.model_dump())
        return success_response("Espacio disponible para el rol encontrado", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_espacio_by_rol: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=EspacioDisponibleSucursalResponse)
def create_espacio(
    espacio_data: EspacioDisponibleSucursalBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    try:
        nuevo_espacio = EspacioDisponibleSucursal(**espacio_data.model_dump())
        creado = controlador_py_logger_create_espacio(nuevo_espacio, db)
        espacio_schema = EspacioDisponibleSucursalResponse.model_validate(creado)
        data = jsonable_encoder(espacio_schema.model_dump())
        return success_response("Espacio disponible creado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_espacio: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{espacio_id}", response_model=EspacioDisponibleSucursalResponse)
def update_espacio_partial(
    espacio_id: int,
    espacio_update: EspacioDisponibleSucursalUpdate,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    try:
        # Recupera la instancia actual
        espacio_actual = controlador_py_logger_get_by_id_espacio(espacio_id, db)
        update_data = espacio_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(espacio_actual, key, value)
        actualizado = controlador_py_logger_update_espacio(espacio_actual, db)
        espacio_schema = EspacioDisponibleSucursalResponse.model_validate(actualizado)
        data = jsonable_encoder(espacio_schema.model_dump())
        return success_response("Espacio disponible actualizado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_espacio_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{espacio_id}")
def delete_espacio(
    espacio_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    try:
        resultado = controlador_py_logger_delete_espacio(espacio_id, db)
        return success_response("Espacio disponible eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_espacio: %s", e)
        return error_response(str(e), status_code=500)

import logging
from fastapi import APIRouter, HTTPException, Path, Body, Depends
from typing import List
from fastapi.encoders import jsonable_encoder

from application.controllers.colaborador_sucursal_controller import (
    controlador_get_by_id,
    controlador_get_by_colaborador,
    controlador_get_by_sucursal,
    controlador_create_colaborador_sucursal,
    controlador_update_colaborador_sucursal,
    controlador_delete_colaborador_sucursal,
    controlador_get_sucursales_by_colaborador,
    controlador_get_colaboradores_by_sucursal
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger
from infrastructure.schemas.colaborador_sucursal import (
    ColaboradorSucursalBase,
    ColaboradorSucursalUpdate,
    ColaboradorSucursalResponse,
    ColaboradorSucursalDetail
)
from infrastructure.schemas.sucursal import SucursalResponse
from infrastructure.databases.models.colaborador_sucursal import ColaboradorSucursal

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles
from sqlalchemy.orm import Session

router = APIRouter(prefix="/colaboradores_sucursales", tags=["Colaborador Sucursal"])
logger = setup_logger(__name__, "logs/colaborador_sucursal.log")

@router.get("/id/{relacion_id}", response_model=ColaboradorSucursalResponse)
def get_colaborador_sucursal_by_id(
    relacion_id: int = Path(..., description="ID de la relación"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        relacion = controlador_get_by_id(relacion_id, db)
        relacion_schema = ColaboradorSucursalResponse.model_validate(relacion)
        data = jsonable_encoder(relacion_schema.model_dump())
        return success_response("Registro obtenido", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_colaborador_sucursal_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/colaborador/{colaborador_id}", response_model=List[ColaboradorSucursalResponse])
def get_colaboradores_sucursal_by_colaborador(
    colaborador_id: int = Path(..., description="ID del colaborador"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        relaciones = controlador_get_by_colaborador(colaborador_id, db)
        relaciones_schema = [ColaboradorSucursalResponse.model_validate(r) for r in relaciones]
        data = [jsonable_encoder(r.model_dump()) for r in relaciones_schema]
        return success_response("Registros obtenidos", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_colaboradores_sucursal_by_colaborador: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/sucursal/{sucursal_id}", response_model=List[ColaboradorSucursalResponse])
def get_colaboradores_sucursal_by_sucursal(
    sucursal_id: int = Path(..., description="ID de la sucursal"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        relaciones = controlador_get_by_sucursal(sucursal_id, db)
        relaciones_schema = [ColaboradorSucursalResponse.model_validate(r) for r in relaciones]
        data = [jsonable_encoder(r.model_dump()) for r in relaciones_schema]
        return success_response("Registros obtenidos", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_colaboradores_sucursal_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=ColaboradorSucursalResponse)
def create_colaborador_sucursal(
    relacion_data: ColaboradorSucursalBase = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        nueva_relacion = ColaboradorSucursal(**relacion_data.model_dump())
        creado = controlador_create_colaborador_sucursal(nueva_relacion, db)
        relacion_schema = ColaboradorSucursalResponse.model_validate(creado)
        data = jsonable_encoder(relacion_schema.model_dump())
        return success_response("Registro creado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_colaborador_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{relacion_id}", response_model=ColaboradorSucursalResponse)
def update_colaborador_sucursal(
    relacion_id: int = Path(..., description="ID de la relación a actualizar"),
    relacion_update: ColaboradorSucursalUpdate = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        # Primero, se obtiene el registro actual
        registro_actual = controlador_get_by_id(relacion_id, db)
        update_data = relacion_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(registro_actual, key, value)
        actualizado = controlador_update_colaborador_sucursal(registro_actual, db)
        relacion_schema = ColaboradorSucursalResponse.model_validate(actualizado)
        data = jsonable_encoder(relacion_schema.model_dump())
        return success_response("Registro actualizado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_colaborador_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{relacion_id}")
def delete_colaborador_sucursal(
    relacion_id: int = Path(..., description="ID de la relación a eliminar"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        resultado = controlador_delete_colaborador_sucursal(relacion_id, db)
        return success_response("Registro eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_colaborador_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/colaborador/{colaborador_id}/sucursales", response_model=List[SucursalResponse])
def get_sucursales_by_colaborador_endpoint(
    colaborador_id: int = Path(..., description="ID del colaborador"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint que retorna la lista de sucursales completas en las que está asignado un colaborador.
    """
    try:
        sucursales = controlador_get_sucursales_by_colaborador(colaborador_id, db)
        sucursales_schema = [SucursalResponse.model_validate(s) for s in sucursales]
        data = [jsonable_encoder(s.model_dump()) for s in sucursales_schema]
        return success_response("Sucursales obtenidas exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_sucursales_by_colaborador_endpoint: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/sucursal/{sucursal_id}/colaboradores", response_model=List[ColaboradorSucursalDetail])
def get_colaboradores_by_sucursal_endpoint(
    sucursal_id: int = Path(..., description="ID de la sucursal"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint que retorna la lista de colaboradores completos asociados a una sucursal.
    """
    try:
        colaboradores = controlador_get_colaboradores_by_sucursal(sucursal_id, db)
        colaboradores_schema = [ColaboradorSucursalDetail.model_validate(c) for c in colaboradores]
        data = [jsonable_encoder(c.model_dump()) for c in colaboradores_schema]
        return success_response("Colaboradores obtenidos exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_colaboradores_by_sucursal_endpoint: %s", e)
        return error_response(str(e), status_code=500)

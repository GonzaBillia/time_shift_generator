from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from fastapi.encoders import jsonable_encoder

from infrastructure.schemas.dia import DiaResponse, DiaBase
from infrastructure.databases.models.dia import Dia
from application.controllers.dia_controller import (
    controlador_py_logger_get_by_id_dia,
    controlador_py_logger_get_by_nombre_dia,
    controlador_py_logger_get_all_dias,
    controlador_py_logger_create_dia,
    controlador_py_logger_update_dia,
    controlador_py_logger_delete_dia
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles
from sqlalchemy.orm import Session

router = APIRouter(prefix="/dias", tags=["Días"])
logger = setup_logger(__name__, "logs/dia.log")

@router.get("/id/{dia_id}", response_model=DiaResponse)
def get_dia_by_id(
    dia_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener un Día por su ID.
    """
    try:
        dia = controlador_py_logger_get_by_id_dia(dia_id, db)
        dia_schema = DiaResponse.model_validate(dia)
        return success_response("Día encontrado", data=dia_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_dia_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/nombre/{nombre}", response_model=DiaResponse)
def get_dia_by_nombre(
    nombre: str,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener un Día por su nombre.
    """
    try:
        dia = controlador_py_logger_get_by_nombre_dia(nombre, db)
        dia_schema = DiaResponse.model_validate(dia)
        return success_response("Día encontrado", data=dia_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_dia_by_nombre: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/", response_model=List[DiaResponse])
def get_all_dias(
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todos los Días.
    """
    try:
        dias = controlador_py_logger_get_all_dias(db)
        dias_schema = [DiaResponse.model_validate(d) for d in dias]
        data = [ds.model_dump() for ds in dias_schema]
        return success_response("Días encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_dias: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=DiaResponse)
def create_dia(
    dia_data: DiaBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin"))
):
    """
    Endpoint para crear un nuevo Día.
    """
    try:
        nueva_dia = Dia(**dia_data.model_dump())
        dia_creado = controlador_py_logger_create_dia(nueva_dia, db)
        dia_schema = DiaResponse.model_validate(dia_creado)
        return success_response("Día creado exitosamente", data=dia_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_dia: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{dia_id}", response_model=DiaResponse)
def update_dia(
    dia_id: int,
    dia_data: DiaBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin"))
):
    """
    Endpoint para actualizar un Día existente.
    """
    try:
        update_data = dia_data.model_dump(exclude_unset=True)
        update_data["id"] = dia_id
        dia_to_update = Dia(**update_data)
        dia_actualizado = controlador_py_logger_update_dia(dia_to_update, db)
        dia_schema = DiaResponse.model_validate(dia_actualizado)
        return success_response("Día actualizado exitosamente", data=dia_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_dia: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{dia_id}")
def delete_dia(
    dia_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin"))
):
    """
    Endpoint para eliminar un Día por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_dia(dia_id, db)
        return success_response("Día eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_dia: %s", e)
        return error_response(str(e), status_code=500)

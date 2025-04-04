from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from infrastructure.schemas.formato import FormatoResponse, FormatoBase
from infrastructure.schemas.rol import RolResponse
from infrastructure.databases.models.formato import Formato
from application.controllers.formato_controller import (
    controlador_py_logger_get_by_id_formato,
    controlador_py_logger_get_all_formatos,
    controlador_py_logger_create_formato,
    controlador_py_logger_update_formato,
    controlador_py_logger_delete_formato,
    controlador_py_logger_get_by_nombre_formato,
    controlador_py_logger_get_roles_by_formato
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/formatos", tags=["Formatos"])
logger = setup_logger(__name__, "logs/formato.log")

@router.get("/id/{formato_id}", response_model=FormatoResponse)
def get_formato_by_id(
    formato_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        formato = controlador_py_logger_get_by_id_formato(formato_id, db)
        formato_schema = FormatoResponse.model_validate(formato)
        return success_response("Formato encontrado", data=formato_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_formato_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/", response_model=List[FormatoResponse])
def get_all_formatos(
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        formatos = controlador_py_logger_get_all_formatos(db)
        formatos_schema = [FormatoResponse.model_validate(f) for f in formatos]
        data = [fs.model_dump() for fs in formatos_schema]
        return success_response("Formatos encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_formatos: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=FormatoResponse)
def create_formato(
    formato_data: FormatoBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    try:
        nuevo_formato = Formato(**formato_data.model_dump())
        formato_creado = controlador_py_logger_create_formato(nuevo_formato, db)
        formato_schema = FormatoResponse.model_validate(formato_creado)
        return success_response("Formato creado exitosamente", data=formato_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_formato: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{formato_id}", response_model=FormatoResponse)
def update_formato(
    formato_id: int,
    formato_data: FormatoBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    try:
        update_data = formato_data.model_dump()
        update_data["id"] = formato_id
        formato_to_update = Formato(**update_data)
        formato_actualizado = controlador_py_logger_update_formato(formato_to_update, db)
        formato_schema = FormatoResponse.model_validate(formato_actualizado)
        return success_response("Formato actualizado exitosamente", data=formato_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_formato: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{formato_id}")
def delete_formato(
    formato_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    try:
        resultado = controlador_py_logger_delete_formato(formato_id, db)
        return success_response("Formato eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_formato: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/nombre/{nombre}", response_model=FormatoResponse)
def get_formato_by_nombre(
    nombre: str,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        formato = controlador_py_logger_get_by_nombre_formato(nombre, db)
        formato_schema = FormatoResponse.model_validate(formato)
        return success_response("Formato encontrado", data=formato_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_formato_by_nombre: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/roles/{formato_id}", response_model=List[RolResponse])
def get_roles_by_formato(
    formato_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    try:
        roles = controlador_py_logger_get_roles_by_formato(formato_id, db)
        roles_schema = [RolResponse.model_validate(role) for role in roles]
        data = [rs.model_dump() for rs in roles_schema]
        return success_response("Roles obtenidos para el Formato", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_roles_by_formato: %s", e)
        return error_response(str(e), status_code=500)

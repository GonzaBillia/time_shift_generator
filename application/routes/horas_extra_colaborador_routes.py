from fastapi import APIRouter, HTTPException, Query, Body, Depends
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from infrastructure.schemas.horas_extra_colaborador import (
    HorasExtraColaboradorResponse, 
    HorasExtraColaboradorBase,
    HorasExtraColaboradorUpdate
)
from infrastructure.databases.models.horas_extra_colaborador import HorasExtraColaborador
from application.controllers.horas_extra_colaborador_controller import (
    controlador_py_logger_get_by_colaborador_horas_extra,
    controlador_py_logger_get_by_tipo_horas_extra,
    controlador_py_logger_create_horas_extra,
    controlador_py_logger_delete_horas_extra
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/horas_extra", tags=["Horas Extra Colaborador"])
logger = setup_logger(__name__, "logs/horas_extra_colaborador.log")

@router.get("/colaborador/{colaborador_id}", response_model=List[HorasExtraColaboradorResponse])
def get_horas_extra_by_colaborador(
    colaborador_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todas las horas extra de un colaborador.
    """
    try:
        registros = controlador_py_logger_get_by_colaborador_horas_extra(colaborador_id, db)
        registros_schema = [HorasExtraColaboradorResponse.model_validate(r) for r in registros]
        data = [jsonable_encoder(rs.model_dump()) for rs in registros_schema]
        return success_response("Horas extra obtenidas", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horas_extra_by_colaborador: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/colaborador/{colaborador_id}/tipo/{tipo}", response_model=List[HorasExtraColaboradorResponse])
def get_horas_extra_by_tipo(
    colaborador_id: int,
    tipo: str,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener las horas extra de un colaborador filtradas por tipo.
    """
    try:
        registros = controlador_py_logger_get_by_tipo_horas_extra(colaborador_id, tipo, db)
        registros_schema = [HorasExtraColaboradorResponse.model_validate(r) for r in registros]
        data = [jsonable_encoder(rs.model_dump()) for rs in registros_schema]
        return success_response("Horas extra filtradas por tipo obtenidas", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horas_extra_by_tipo: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=HorasExtraColaboradorResponse)
def create_horas_extra(
    horas_extra_data: HorasExtraColaboradorBase = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para crear un nuevo registro de horas extra.
    """
    try:
        nuevo_registro = HorasExtraColaborador(**horas_extra_data.model_dump())
        creado = controlador_py_logger_create_horas_extra(nuevo_registro, db)
        registro_schema = HorasExtraColaboradorResponse.model_validate(creado)
        data = jsonable_encoder(registro_schema.model_dump())
        return success_response("Horas extra creadas exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_horas_extra: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{horas_extra_id}")
def delete_horas_extra(
    horas_extra_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para eliminar un registro de horas extra por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_horas_extra(horas_extra_id, db)
        return success_response("Horas extra eliminadas exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_horas_extra: %s", e)
        return error_response(str(e), status_code=500)

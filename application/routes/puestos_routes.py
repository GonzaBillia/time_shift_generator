from fastapi import APIRouter, HTTPException, Body, Depends, Query
from typing import List, Generator
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import logging
from datetime import datetime

from infrastructure.schemas.puestos import PuestoBase, PuestoUpdate, PuestoResponse
from application.helpers.response_handler import success_response, error_response
from application.controllers.puestos_controller import (
    controlador_py_logger_crear_puesto,
    controlador_py_logger_actualizar_puesto,
    controlador_py_logger_obtener_puestos,
    controlador_py_logger_crear_varios_puestos,
    controlador_py_logger_eliminar_varios_puestos,
    controlador_py_logger_actualizar_varios_puestos,
    controlador_py_logger_copy_history
)
from infrastructure.databases.config.database import DBConfig

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_session, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/puestos", tags=["Puestos"])
logger = logging.getLogger(__name__)

def get_rrhh_session() -> Generator[Session, None, None]:
    yield from DBConfig.get_db_session("rrhh")

@router.post("/crear", response_model=PuestoResponse)
def crear_puesto_endpoint(
    puesto_data: PuestoBase = Body(...),
    db: Session = Depends(get_rrhh_session),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para crear un puesto. Se espera un objeto PuestoBase.
    """
    try:
        puesto_dict = puesto_data.model_dump() if hasattr(puesto_data, "model_dump") else puesto_data.dict()
        puesto = controlador_py_logger_crear_puesto(puesto_dict, db)
        return success_response("Puesto creado exitosamente", data=jsonable_encoder(puesto))
    except HTTPException as he:
        raise he
    except Exception as error:
        logger.error("Error en crear_puesto_endpoint: %s", error)
        return error_response(str(error), status_code=500)

@router.post("/crear_varios", response_model=List[PuestoResponse])
def crear_varios_puestos_endpoint(
    puestos_data: List[PuestoBase] = Body(...),
    db: Session = Depends(get_rrhh_session),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para crear varios puestos.
    Se espera una lista de objetos PuestoBase.
    """
    try:
        puestos_list = [
            puesto.model_dump() if hasattr(puesto, "model_dump") else puesto.dict()
            for puesto in puestos_data
        ]
        puestos = controlador_py_logger_crear_varios_puestos(puestos_list, db)
        return success_response("Puestos creados exitosamente", data=jsonable_encoder(puestos))
    except HTTPException as he:
        raise he
    except Exception as error:
        logger.error("Error en crear_varios_puestos_endpoint: %s", error)
        return error_response(str(error), status_code=500)

@router.put("/actualizar", response_model=PuestoResponse)
def actualizar_puesto_endpoint(
    puesto_data: PuestoUpdate = Body(...),
    db: Session = Depends(get_rrhh_session),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para actualizar un puesto. Se espera un objeto PuestoUpdate que contenga el 'id'.
    """
    try:
        puesto_dict = puesto_data.model_dump() if hasattr(puesto_data, "model_dump") else puesto_data.dict()
        puesto = controlador_py_logger_actualizar_puesto(puesto_dict, db)
        return success_response("Puesto actualizado exitosamente", data=jsonable_encoder(puesto))
    except HTTPException as he:
        raise he
    except Exception as error:
        logger.error("Error en actualizar_puesto_endpoint: %s", error)
        return error_response(str(error), status_code=500)

@router.put("/actualizar-varios", response_model=List[PuestoResponse])
def actualizar_varios_puestos_endpoint(
    puestos_data: List[PuestoUpdate] = Body(...),
    db: Session = Depends(get_rrhh_session),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para actualizar varios puestos. Se espera una lista de objetos PuestoUpdate,
    donde cada uno contenga el 'id' y los campos a modificar.
    """
    try:
        puestos_dict = [
            puesto.model_dump() if hasattr(puesto, "model_dump") else puesto.dict()
            for puesto in puestos_data
        ]
        puestos = controlador_py_logger_actualizar_varios_puestos(puestos_dict, db)
        return success_response("Puestos actualizados exitosamente", data=jsonable_encoder(puestos))
    except HTTPException as he:
        raise he
    except Exception as error:
        logger.error("Error en actualizar_varios_puestos_endpoint: %s", error)
        return error_response(str(error), status_code=500)

@router.get("/sucursal/{sucursal_id}", response_model=List[PuestoResponse])
def obtener_puestos_por_sucursal_endpoint(
    sucursal_id: int,
    db: Session = Depends(get_rrhh_session),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todos los puestos de una sucursal.
    """
    try:
        puestos = controlador_py_logger_obtener_puestos(sucursal_id, db)
        return success_response("Puestos obtenidos exitosamente", data=jsonable_encoder(puestos))
    except HTTPException as he:
        raise he
    except Exception as error:
        logger.error("Error en obtener_puestos_por_sucursal_endpoint: %s", error)
        return error_response(str(error), status_code=500)

@router.delete("/eliminar-varios", response_model=dict)
def eliminar_varios_puestos_endpoint(
    puesto_ids: List[int] = Body(..., embed=True),
    db: Session = Depends(get_rrhh_session),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para eliminar varios puestos.
    Se espera una lista de IDs de puestos en el body.
    """
    try:
        controlador_py_logger_eliminar_varios_puestos(puesto_ids, db)
        return success_response("Puestos eliminados exitosamente")
    except HTTPException as he:
        raise he
    except Exception as error:
        logger.error("Error en eliminar_varios_puestos_endpoint: %s", error)
        return error_response(str(error), status_code=500)

@router.post("/copy_history", response_model=dict)
def copy_history_endpoint(
    copy_history_data: dict = Body(...),
    db: Session = Depends(get_rrhh_session),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para copiar históricamente puestos y horarios.
    Se espera que el body contenga:
      - sucursal_id
      - origin_week: {start: date, end: date}
      - destination_weeks: List[{start: date, end: date}]
      - resources: List de puestos (con su id original)
      - events: List de horarios (con su puesto_id original)
    """
    try:
        result = controlador_py_logger_copy_history(copy_history_data, db)
        return success_response("Copia histórica completada", data=jsonable_encoder(result))
    except HTTPException as he:
        raise he
    except Exception as error:
        logger.error("Error en copy_history_endpoint: %s", error)
        return error_response(str(error), status_code=500)

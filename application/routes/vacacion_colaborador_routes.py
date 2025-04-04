from fastapi import APIRouter, HTTPException, Query, Body, Depends
from typing import List
from datetime import date
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import logging

from infrastructure.schemas.vacacion_colaborador import (
    VacacionColaboradorBase,
    VacacionColaboradorResponse,
    VacacionColaboradorUpdate
)
from infrastructure.databases.models.vacacion_colaborador import VacacionColaborador
from application.controllers.vacacion_colaborador_controller import (
    controlador_get_by_colaborador_vacacion,
    controlador_get_by_fecha_vacacion,
    controlador_create_vacacion,
    controlador_update_vacacion,
    controlador_delete_vacacion
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para la sesión y autenticación
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/vacaciones", tags=["Vacación Colaborador"])
logger = setup_logger(__name__, "logs/vacacion_colaborador.log")

@router.get("/colaborador/{colaborador_id}", response_model=List[VacacionColaboradorResponse])
def get_vacaciones_by_colaborador(
    colaborador_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todas las vacaciones de un colaborador.
    """
    try:
        vacaciones = controlador_get_by_colaborador_vacacion(colaborador_id, db)
        vacaciones_schema = [VacacionColaboradorResponse.model_validate(v) for v in vacaciones]
        data = [jsonable_encoder(v.model_dump()) for v in vacaciones_schema]
        return success_response("Vacaciones obtenidas exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_vacaciones_by_colaborador: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/fecha", response_model=List[VacacionColaboradorResponse])
def get_vacaciones_by_fecha(
    fecha: date = Query(..., description="Fecha en formato YYYY-MM-DD"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todas las vacaciones registradas para una fecha específica.
    """
    try:
        vacaciones = controlador_get_by_fecha_vacacion(fecha, db)
        vacaciones_schema = [VacacionColaboradorResponse.model_validate(v) for v in vacaciones]
        data = [jsonable_encoder(v.model_dump()) for v in vacaciones_schema]
        return success_response("Vacaciones obtenidas por fecha", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_vacaciones_by_fecha: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=VacacionColaboradorResponse)
def create_vacacion(
    vacacion_data: VacacionColaboradorBase = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para crear un nuevo registro de vacaciones.
    """
    try:
        # Se crea el objeto ORM a partir de los datos del esquema
        nueva_vacacion = VacacionColaborador(**vacacion_data.model_dump())
        creado = controlador_create_vacacion(nueva_vacacion, db)
        vacacion_schema = VacacionColaboradorResponse.model_validate(creado)
        data = jsonable_encoder(vacacion_schema.model_dump())
        return success_response("Vacación creada exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_vacacion: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{vacacion_id}", response_model=VacacionColaboradorResponse)
def update_vacacion(
    vacacion_id: int,
    vacacion_update: VacacionColaboradorUpdate = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para actualizar un registro de vacaciones.
    Se espera que el body contenga los campos a modificar y el 'id' del registro.
    """
    try:
        # Obtener el registro actual (idealmente, se debería obtener desde el repository)
        # En este ejemplo, se crea un objeto dummy con el id y se actualizan los campos.
        vacacion_actual = VacacionColaborador(id=vacacion_id, colaborador_id=0, fecha=date.today())
        update_data = vacacion_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(vacacion_actual, key, value)
        actualizado = controlador_update_vacacion(vacacion_actual, db)
        vacacion_schema = VacacionColaboradorResponse.model_validate(actualizado)
        data = jsonable_encoder(vacacion_schema.model_dump())
        return success_response("Vacación actualizada exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_vacacion: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{vacacion_id}")
def delete_vacacion(
    vacacion_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para eliminar un registro de vacaciones por su ID.
    """
    try:
        resultado = controlador_delete_vacacion(vacacion_id, db)
        return success_response("Vacación eliminada exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_vacacion: %s", e)
        return error_response(str(e), status_code=500)

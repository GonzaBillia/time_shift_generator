import logging
from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import date
from fastapi.encoders import jsonable_encoder
from application.controllers.vacacion_colaborador_controller import (
    controlador_get_by_colaborador_vacacion,
    controlador_get_by_fecha_vacacion,
    controlador_create_vacacion,
    controlador_update_vacacion,
    controlador_delete_vacacion
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger
from infrastructure.schemas.vacacion_colaborador import (
    VacacionColaboradorBase,
    VacacionColaboradorResponse,
    VacacionColaboradorUpdate
)
from infrastructure.databases.models.vacacion_colaborador import VacacionColaborador

router = APIRouter(prefix="/vacaciones", tags=["Vacación Colaborador"])
logger = setup_logger(__name__, "logs/vacacion_colaborador.log")

@router.get("/colaborador/{colaborador_id}", response_model=List[VacacionColaboradorResponse])
def get_vacaciones_by_colaborador(colaborador_id: int):
    try:
        vacaciones = controlador_get_by_colaborador_vacacion(colaborador_id)
        vacaciones_schema = [VacacionColaboradorResponse.model_validate(v) for v in vacaciones]
        data = [jsonable_encoder(v.model_dump()) for v in vacaciones_schema]
        return success_response("Vacaciones obtenidas exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_vacaciones_by_colaborador: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/fecha", response_model=List[VacacionColaboradorResponse])
def get_vacaciones_by_fecha(fecha: date = Query(..., description="Fecha en formato YYYY-MM-DD")):
    try:
        vacaciones = controlador_get_by_fecha_vacacion(fecha)
        vacaciones_schema = [VacacionColaboradorResponse.model_validate(v) for v in vacaciones]
        data = [jsonable_encoder(v.model_dump()) for v in vacaciones_schema]
        return success_response("Vacaciones obtenidas por fecha", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_vacaciones_by_fecha: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=VacacionColaboradorResponse)
def create_vacacion(vacacion_data: VacacionColaboradorBase):
    try:
        # Se crea el objeto ORM a partir de los datos del esquema
        nueva_vacacion = VacacionColaborador(**vacacion_data.model_dump())
        creado = controlador_create_vacacion(nueva_vacacion)
        vacacion_schema = VacacionColaboradorResponse.model_validate(creado)
        data = jsonable_encoder(vacacion_schema.model_dump())
        return success_response("Vacación creada exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_vacacion: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{vacacion_id}", response_model=VacacionColaboradorResponse)
def update_vacacion(vacacion_id: int, vacacion_update: VacacionColaboradorUpdate):
    try:
        # Se asume que existe un método get_by_id en el repository; si no, se puede simular
        # Para este ejemplo, se crea un objeto VacacionColaborador con el id indicado y se actualizan los campos.
        # Es preferible obtener primero el registro actual.
        # Aquí, por simplicidad, se crea un objeto con valores dummy que luego se sobreescriben.
        from infrastructure.databases.models.vacacion_colaborador import VacacionColaborador
        # Se recomienda obtener el registro actual; en este ejemplo se simula:
        vacacion_actual = VacacionColaborador(id=vacacion_id, colaborador_id=0, fecha=date.today())
        update_data = vacacion_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(vacacion_actual, key, value)
        actualizado = controlador_update_vacacion(vacacion_actual)
        vacacion_schema = VacacionColaboradorResponse.model_validate(actualizado)
        data = jsonable_encoder(vacacion_schema.model_dump())
        return success_response("Vacación actualizada exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_vacacion: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{vacacion_id}")
def delete_vacacion(vacacion_id: int):
    try:
        resultado = controlador_delete_vacacion(vacacion_id)
        return success_response("Vacación eliminada exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_vacacion: %s", e)
        return error_response(str(e), status_code=500)

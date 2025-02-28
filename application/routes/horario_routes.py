# ROUTER_PY_SCHEMA_HORARIO
from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import date, time
from fastapi.encoders import jsonable_encoder
from infrastructure.schemas.horario import HorarioResponse, HorarioBase, HorarioUpdate
from infrastructure.databases.models.horario import Horario
from application.controllers.horario_controller import (
    controlador_py_logger_get_by_id_horario,
    controlador_py_logger_get_all_horarios,
    controlador_py_logger_create_horario,
    controlador_py_logger_update_horario,
    controlador_py_logger_delete_horario,
    controlador_py_logger_get_by_sucursal,
    controlador_py_logger_get_by_colaborador,
    controlador_py_logger_get_by_fecha,
    controlador_py_logger_verificar_superposicion,
    controlador_py_logger_get_horarios_por_dia
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

router = APIRouter(prefix="/horarios", tags=["Horarios"])
logger = setup_logger(__name__, "logs/horario.log")

@router.get("/id/{horario_id}", response_model=HorarioResponse)
def get_horario_by_id(horario_id: int):
    try:
        horario = controlador_py_logger_get_by_id_horario(horario_id)
        horario_schema = HorarioResponse.model_validate(horario)
        return success_response("Horario encontrado", data=horario_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horario_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/", response_model=List[HorarioResponse])
def get_all_horarios():
    try:
        horarios = controlador_py_logger_get_all_horarios()
        horarios_schema = [HorarioResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Horarios encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_horarios: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=HorarioResponse)
def create_horario(horario_data: HorarioBase):
    try:
        nuevo_horario = Horario(**horario_data.model_dump())
        creado = controlador_py_logger_create_horario(nuevo_horario)
        horario_schema = HorarioResponse.model_validate(creado)
        data = jsonable_encoder(horario_schema.model_dump())
        return success_response("Horario creado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_horario: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{horario_id}", response_model=HorarioResponse)
def update_horario_partial(horario_id: int, horario_update: HorarioUpdate):
    """
    Actualiza parcialmente un Horario.
    Solo se actualizarán los campos enviados.
    """
    try:
        # Recupera la instancia actual
        horario_actual = controlador_py_logger_get_by_id_horario(horario_id)
        update_data = horario_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(horario_actual, key, value)
        actualizado = controlador_py_logger_update_horario(horario_actual)
        horario_schema = HorarioResponse.model_validate(actualizado)
        data = jsonable_encoder(horario_schema.model_dump())
        return success_response("Horario actualizado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_horario_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{horario_id}")
def delete_horario(horario_id: int):
    try:
        resultado = controlador_py_logger_delete_horario(horario_id)
        return success_response("Horario eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_horario: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/sucursal/{sucursal_id}", response_model=List[HorarioResponse])
def get_horarios_by_sucursal(sucursal_id: int):
    try:
        horarios = controlador_py_logger_get_by_sucursal(sucursal_id)
        horarios_schema = [HorarioResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Horarios para la sucursal encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/colaborador/{colaborador_id}", response_model=List[HorarioResponse])
def get_horarios_by_colaborador(colaborador_id: int):
    try:
        horarios = controlador_py_logger_get_by_colaborador(colaborador_id)
        horarios_schema = [HorarioResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Horarios para el colaborador encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_colaborador: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/fecha", response_model=List[HorarioResponse])
def get_horarios_by_fecha(fecha: date):
    try:
        horarios = controlador_py_logger_get_by_fecha(fecha)
        horarios_schema = [HorarioResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Horarios para la fecha encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_fecha: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/superposicion", response_model=bool)
def verificar_superposicion(
    sucursal_id: int, 
    fecha: date, 
    hora_inicio: time, 
    hora_fin: time
):
    try:
        superpone = controlador_py_logger_verificar_superposicion(sucursal_id, fecha, hora_inicio, hora_fin)
        return success_response("Verificación de superposición", data=superpone)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en verificar_superposicion: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/sucursal/{sucursal_id}/dia/{dia_id}", response_model=List[HorarioResponse])
def get_horarios_por_dia(sucursal_id: int, dia_id: int):
    try:
        horarios = controlador_py_logger_get_horarios_por_dia(sucursal_id, dia_id)
        horarios_schema = [HorarioResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Horarios para el día encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_por_dia: %s", e)
        return error_response(str(e), status_code=500)

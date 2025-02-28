# ROUTER_PY_SCHEMA_HORARIO_SUCURSAL
from fastapi import APIRouter, HTTPException, Query
from typing import List
from infrastructure.schemas.horario_sucursal import (
    HorarioSucursalResponse,
    HorarioSucursalBase,
    HorarioSucursalUpdate
)
from infrastructure.databases.models.horario_sucursal import HorarioSucursal
from application.controllers.horario_sucursal_controller import (
    controlador_py_logger_get_by_id_horario_sucursal,
    controlador_py_logger_get_by_sucursal,
    controlador_py_logger_get_by_dia,
    controlador_py_logger_create_horario_sucursal,
    controlador_py_logger_update_horario_sucursal,
    controlador_py_logger_delete_horario_sucursal
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

router = APIRouter(prefix="/horarios_sucursal", tags=["Horarios Sucursal"])
logger = setup_logger(__name__, "logs/horario_sucursal.log")

@router.get("/id/{horario_id}", response_model=HorarioSucursalResponse)
def get_horario_sucursal_by_id(horario_id: int):
    """
    Endpoint para obtener un HorarioSucursal por su ID.
    """
    try:
        horario = controlador_py_logger_get_by_id_horario_sucursal(horario_id)
        horario_schema = HorarioSucursalResponse.model_validate(horario)
        return success_response("HorarioSucursal encontrado", data=horario_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horario_sucursal_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/sucursal/{sucursal_id}", response_model=List[HorarioSucursalResponse])
def get_horarios_by_sucursal(sucursal_id: int):
    """
    Endpoint para obtener todos los HorarioSucursal asociados a una Sucursal.
    """
    try:
        horarios = controlador_py_logger_get_by_sucursal(sucursal_id)
        horarios_schema = [HorarioSucursalResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Horarios de sucursal encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/dia/{dia_id}", response_model=List[HorarioSucursalResponse])
def get_horarios_by_dia(dia_id: int):
    """
    Endpoint para obtener todos los HorarioSucursal para un día específico.
    """
    try:
        horarios = controlador_py_logger_get_by_dia(dia_id)
        horarios_schema = [HorarioSucursalResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Horarios para el día encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_dia: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=HorarioSucursalResponse)
def create_horario_sucursal(horario_data: HorarioSucursalBase):
    """
    Endpoint para crear un nuevo HorarioSucursal.
    """
    try:
        nuevo_horario = HorarioSucursal(**horario_data.model_dump())
        creado = controlador_py_logger_create_horario_sucursal(nuevo_horario)
        horario_schema = HorarioSucursalResponse.model_validate(creado)
        return success_response("HorarioSucursal creado exitosamente", data=horario_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_horario_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{horario_id}", response_model=HorarioSucursalResponse)
def update_horario_sucursal_partial(horario_id: int, horario_update: HorarioSucursalUpdate):
    """
    Endpoint para actualizar parcialmente un HorarioSucursal.
    Solo se actualizarán los campos enviados.
    """
    try:
        # Recuperar la instancia actual para actualizar
        horario_actual = controlador_py_logger_get_by_id_horario_sucursal(horario_id)
        update_data = horario_update.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(horario_actual, key, value)
        
        actualizado = controlador_py_logger_update_horario_sucursal(horario_actual)
        horario_schema = HorarioSucursalResponse.model_validate(actualizado)
        return success_response("HorarioSucursal actualizado exitosamente", data=horario_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_horario_sucursal_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{horario_id}")
def delete_horario_sucursal(horario_id: int):
    """
    Endpoint para eliminar un HorarioSucursal por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_horario_sucursal(horario_id)
        return success_response("HorarioSucursal eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_horario_sucursal: %s", e)
        return error_response(str(e), status_code=500)

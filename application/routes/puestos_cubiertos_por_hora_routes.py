# application/routes/puestos_cubiertos_routes.py

import logging
from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import time
from fastapi.encoders import jsonable_encoder
from application.helpers.response_handler import success_response, error_response
from application.controllers.puestos_cubiertos_por_hora_controller import (
    controlador_get_by_sucursal_puestos,
    controlador_get_by_rol_puestos,
    controlador_get_by_horario_puestos,
    controlador_create_puestos,
    controlador_update_puestos,
    controlador_delete_puestos
)
from application.config.logger_config import setup_logger
from infrastructure.schemas.puestos_cubiertos_por_hora import (
    PuestosCubiertosPorHoraBase,
    PuestosCubiertosPorHoraUpdate,
    PuestosCubiertosPorHoraResponse
)
from infrastructure.databases.models.puestos_cubiertos_por_hora import PuestosCubiertosPorHora

router = APIRouter(prefix="/puestos_cubiertos", tags=["Puestos Cubiertos Por Hora"])
logger = setup_logger(__name__, "logs/puestos_cubiertos.log")

@router.get("/sucursal/{sucursal_id}", response_model=List[PuestosCubiertosPorHoraResponse])
def get_puestos_by_sucursal(sucursal_id: int):
    try:
        registros = controlador_get_by_sucursal_puestos(sucursal_id)
        registros_schema = [PuestosCubiertosPorHoraResponse.model_validate(r) for r in registros]
        data = [jsonable_encoder(r.model_dump()) for r in registros_schema]
        return success_response("Registros obtenidos", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_puestos_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/rol", response_model=List[PuestosCubiertosPorHoraResponse])
def get_puestos_by_rol(sucursal_id: int, rol_colaborador_id: int):
    try:
        registros = controlador_get_by_rol_puestos(sucursal_id, rol_colaborador_id)
        registros_schema = [PuestosCubiertosPorHoraResponse.model_validate(r) for r in registros]
        data = [jsonable_encoder(r.model_dump()) for r in registros_schema]
        return success_response("Registros filtrados por rol obtenidos", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_puestos_by_rol: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/horario", response_model=PuestosCubiertosPorHoraResponse)
def get_puesto_by_horario(sucursal_id: int, dia_id: int, hora: time):
    try:
        registro = controlador_get_by_horario_puestos(sucursal_id, dia_id, hora)
        registro_schema = PuestosCubiertosPorHoraResponse.model_validate(registro)
        data = jsonable_encoder(registro_schema.model_dump())
        return success_response("Registro obtenido", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_puesto_by_horario: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=PuestosCubiertosPorHoraResponse)
def create_puesto(puesto_data: PuestosCubiertosPorHoraBase):
    try:
        nuevo_registro = PuestosCubiertosPorHora(**puesto_data.model_dump())
        creado = controlador_create_puestos(nuevo_registro)
        registro_schema = PuestosCubiertosPorHoraResponse.model_validate(creado)
        data = jsonable_encoder(registro_schema.model_dump())
        return success_response("Registro creado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_puesto: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{registro_id}", response_model=PuestosCubiertosPorHoraResponse)
def update_puesto(registro_id: int, puesto_update: PuestosCubiertosPorHoraUpdate):
    try:
        # Se asume que se obtiene el registro actual de alguna forma (por ejemplo, por un método get_by_id)
        # Para este ejemplo usaremos get_by_horario si se adapta, o bien se implementa un get_by_id.
        # Aquí usaremos get_by_horario como ejemplo:
        from infrastructure.repositories.puestos_cubiertos_por_hora_repo import PuestosCubiertosPorHoraRepository
        registro_actual = PuestosCubiertosPorHoraRepository.get_by_horario(
            sucursal_id=puesto_update.sucursal_id, 
            dia_id=puesto_update.dia_id, 
            hora=puesto_update.hora
        )
        if not registro_actual:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        update_data = puesto_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(registro_actual, key, value)
        
        actualizado = controlador_update_puestos(registro_actual)
        registro_schema = PuestosCubiertosPorHoraResponse.model_validate(actualizado)
        data = jsonable_encoder(registro_schema.model_dump())
        return success_response("Registro actualizado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_puesto: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{registro_id}")
def delete_puesto(registro_id: int):
    try:
        resultado = controlador_delete_puestos(registro_id)
        return success_response("Registro eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_puesto: %s", e)
        return error_response(str(e), status_code=500)

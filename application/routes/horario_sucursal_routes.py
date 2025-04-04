from fastapi import APIRouter, HTTPException, Depends
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

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

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/horarios_sucursal", tags=["Horarios Sucursal"])
logger = setup_logger(__name__, "logs/horario_sucursal.log")

@router.get("/id/{horario_id}", response_model=HorarioSucursalResponse)
def get_horario_sucursal_by_id(
    horario_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener un HorarioSucursal por su ID.
    """
    try:
        horario = controlador_py_logger_get_by_id_horario_sucursal(horario_id, db)
        horario_schema = HorarioSucursalResponse.model_validate(horario)
        data = jsonable_encoder(horario_schema.model_dump())
        return success_response("HorarioSucursal encontrado", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horario_sucursal_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/sucursal/{sucursal_id}", response_model=List[HorarioSucursalResponse])
def get_horarios_by_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todos los HorarioSucursal asociados a una Sucursal.
    """
    try:
        horarios = controlador_py_logger_get_by_sucursal(sucursal_id, db)
        horarios_schema = [HorarioSucursalResponse.model_validate(h) for h in horarios]
        data = jsonable_encoder([hs.model_dump() for hs in horarios_schema])
        return success_response("Horarios de sucursal encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/dia/{dia_id}", response_model=List[HorarioSucursalResponse])
def get_horarios_by_dia(
    dia_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todos los HorarioSucursal para un día específico.
    """
    try:
        horarios = controlador_py_logger_get_by_dia(dia_id, db)
        horarios_schema = [HorarioSucursalResponse.model_validate(h) for h in horarios]
        data = jsonable_encoder([hs.model_dump() for hs in horarios_schema])
        return success_response("Horarios para el día encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_dia: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=HorarioSucursalResponse)
def create_horario_sucursal(
    horario_data: HorarioSucursalBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    try:
        nuevo_horario = HorarioSucursal(**horario_data.model_dump())
        creado = controlador_py_logger_create_horario_sucursal(nuevo_horario, db)
        horario_schema = HorarioSucursalResponse.model_validate(creado)
        data = jsonable_encoder(horario_schema.model_dump())
        return success_response("HorarioSucursal creado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_horario_sucursal: %s", e)
        return error_response(str(e), status_code=500)
    
@router.put("/{horario_id}", response_model=HorarioSucursalResponse)
def update_horario_sucursal_partial(
    horario_id: int,
    horario_update: HorarioSucursalUpdate,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    """
    Endpoint para actualizar parcialmente un HorarioSucursal.
    Solo se actualizarán los campos enviados.
    """
    try:
        # Recuperar la instancia actual para actualizar
        horario_actual = controlador_py_logger_get_by_id_horario_sucursal(horario_id, db)
        update_data = horario_update.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(horario_actual, key, value)
        
        actualizado = controlador_py_logger_update_horario_sucursal(horario_actual, db)
        horario_schema = HorarioSucursalResponse.model_validate(actualizado)
        data = jsonable_encoder(horario_schema.model_dump())
        return success_response("HorarioSucursal actualizado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_horario_sucursal_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{horario_id}")
def delete_horario_sucursal(
    horario_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    """
    Endpoint para eliminar un HorarioSucursal por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_horario_sucursal(horario_id, db)
        data = jsonable_encoder({"deleted": resultado})
        return success_response("HorarioSucursal eliminado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_horario_sucursal: %s", e)
        return error_response(str(e), status_code=500)

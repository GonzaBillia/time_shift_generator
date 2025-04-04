from fastapi import APIRouter, HTTPException, Query, Body, Depends
from typing import List
from datetime import time
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from infrastructure.schemas.minimo_puestos_requeridos import (
    MinimoPuestosRequeridosResponse,
    MinimoPuestosRequeridosBase,
    MinimoPuestosRequeridosUpdate
)
from infrastructure.databases.models.minimo_puestos_requeridos import MinimoPuestosRequeridos
from application.controllers.minimo_puestos_controller import (
    controlador_py_logger_get_by_sucursal_minimo,
    controlador_py_logger_get_by_rol_minimo,
    controlador_py_logger_get_by_horario_minimo,
    controlador_py_logger_create_minimo,
    controlador_py_logger_update_minimo,
    controlador_py_logger_delete_minimo
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/minimos", tags=["Mínimo Puestos Requeridos"])
logger = setup_logger(__name__, "logs/minimo_puestos.log")

@router.get("/sucursal/{sucursal_id}", response_model=List[MinimoPuestosRequeridosResponse])
def get_minimos_by_sucursal(
    sucursal_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todos los registros de mínimos de puestos requeridos para una sucursal.
    """
    try:
        minimos = controlador_py_logger_get_by_sucursal_minimo(sucursal_id, db)
        minimos_schema = [MinimoPuestosRequeridosResponse.model_validate(m) for m in minimos]
        data = [jsonable_encoder(ms.model_dump()) for ms in minimos_schema]
        return success_response("Registros obtenidos", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_minimos_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/rol", response_model=List[MinimoPuestosRequeridosResponse])
def get_minimos_by_rol(
    sucursal_id: int = Query(...),
    rol_colaborador_id: int = Query(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener los registros de mínimos de puestos para una sucursal y rol específico.
    """
    try:
        minimos = controlador_py_logger_get_by_rol_minimo(sucursal_id, rol_colaborador_id, db)
        minimos_schema = [MinimoPuestosRequeridosResponse.model_validate(m) for m in minimos]
        data = [jsonable_encoder(ms.model_dump()) for ms in minimos_schema]
        return success_response("Registros filtrados por rol obtenidos", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_minimos_by_rol: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/horario", response_model=MinimoPuestosRequeridosResponse)
def get_minimo_by_horario(
    sucursal_id: int = Query(...),
    dia_id: int = Query(...),
    hora: time = Query(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener el mínimo de puestos requeridos para una sucursal en un día y hora específicos.
    """
    try:
        minimo = controlador_py_logger_get_by_horario_minimo(sucursal_id, dia_id, hora, db)
        minimo_schema = MinimoPuestosRequeridosResponse.model_validate(minimo)
        data = jsonable_encoder(minimo_schema.model_dump())
        return success_response("Registro obtenido", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_minimo_by_horario: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=MinimoPuestosRequeridosResponse)
def create_minimo(
    minimo_data: MinimoPuestosRequeridosBase = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    """
    Endpoint para crear un nuevo registro de mínimos de puestos requeridos.
    """
    try:
        nuevo_minimo = MinimoPuestosRequeridos(**minimo_data.model_dump())
        creado = controlador_py_logger_create_minimo(nuevo_minimo, db)
        minimo_schema = MinimoPuestosRequeridosResponse.model_validate(creado)
        data = jsonable_encoder(minimo_schema.model_dump())
        return success_response("Registro creado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_minimo: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{minimo_id}", response_model=MinimoPuestosRequeridosResponse)
def update_minimo_partial(
    minimo_id: int,
    minimo_update: MinimoPuestosRequeridosUpdate = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    """
    Endpoint para actualizar parcialmente un registro de mínimos de puestos requeridos.
    Solo se actualizarán los campos enviados.
    """
    try:
        # Para actualizar, se obtiene el registro actual usando un método del repositorio.
        # Se asume que existe un método get_by_horario en el repositorio que permita obtener el registro según sucursal, día y hora.
        # Aquí usamos los datos de "minimo_update" para identificar el registro.
        from infrastructure.repositories.minimo_puestos_requeridos_repo import MinimoPuestosRequeridosRepository
        registro_actual = MinimoPuestosRequeridosRepository.get_by_horario(
            sucursal_id=minimo_update.sucursal_id,
            dia_id=minimo_update.dia_id,
            hora=minimo_update.hora,
            db=db
        )
        if not registro_actual:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        
        update_data = minimo_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(registro_actual, key, value)
        
        actualizado = controlador_py_logger_update_minimo(registro_actual, db)
        minimo_schema = MinimoPuestosRequeridosResponse.model_validate(actualizado)
        data = jsonable_encoder(minimo_schema.model_dump())
        return success_response("Registro actualizado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_minimo_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{minimo_id}")
def delete_minimo(
    minimo_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    """
    Endpoint para eliminar un registro de mínimos de puestos requeridos por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_minimo(minimo_id, db)
        return success_response("Registro eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_minimo: %s", e)
        return error_response(str(e), status_code=500)

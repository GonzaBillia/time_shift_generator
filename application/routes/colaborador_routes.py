from fastapi import APIRouter, HTTPException, Query, Depends, status
from sqlalchemy.orm import Session
from datetime import date, time
from typing import List, Optional, Generator
from fastapi.encoders import jsonable_encoder
from application.config.logger_config import setup_logger
from application.controllers.colaborador_controller import (
    controlador_py_logger_get_filtered, 
    controlador_py_logger_get_by_id, 
    controlador_py_logger_get_by_legajo,
    controlador_py_logger_get_details,
    controlador_py_logger_create_colaborador,
    controlador_py_logger_update_colaborador,
    controlador_py_logger_delete_colaborador,
    controlador_py_logger_get_paginated,
    controlador_py_logger_get_horarios_asignados
)
from application.services.colaborador_service import update_full_colaborador_service
from application.helpers.response_handler import error_response, success_response
from infrastructure.schemas.colaborador import ColaboradorResponse, ColaboradorBase, ColaboradorUpdate
from infrastructure.schemas.colaborador_details import ColaboradorDetailSchema
from infrastructure.databases.models.colaborador import Colaborador
from infrastructure.schemas.colaborador_details import ColaboradorFullUpdate
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

logger = setup_logger(__name__)
router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

# Para obtener la sesión de la base de datos "rrhh" usando la factory.
# Dependencia: get_db_factory("rrhh") retorna una función callable.
# En este archivo usamos directamente Depends(get_db_factory("rrhh"))
  
@router.get("/all", response_model=List[ColaboradorResponse])
def get_all_colaboradores(
    page: int = Query(1, ge=1), 
    limit: int = Query(20, ge=1), 
    search: str = Query("", alias="search"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener los colaboradores de forma paginada.
    Parámetros:
      - page: número de página (empezando en 1)
      - limit: cantidad de colaboradores por página
    """
    try:
        colaboradores = controlador_py_logger_get_paginated(page, limit, search, db)
        colaboradores_schema = [ColaboradorResponse.model_validate(c) for c in colaboradores]
        data = [cs.model_dump() for cs in colaboradores_schema]
        return success_response("Colaboradores encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=500)

@router.get("/filters", response_model=List[ColaboradorResponse])
def search_colaboradores(
    dni: Optional[int] = Query(None, description="DNI del colaborador"),
    empresa_id: Optional[int] = Query(None, description="ID de la empresa"),
    tipo_empleado_id: Optional[int] = Query(None, description="ID del tipo de empleado"),
    horario_corrido: Optional[bool] = Query(None, description="Indica si el colaborador tiene horario corrido"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener colaboradores filtrados por DNI, empresa, tipo de empleado y horario corrido.
    """
    logger.info("Endpoint /filters accedido con parámetros: dni=%s, empresa_id=%s, tipo_empleado_id=%s, horario_corrido=%s", 
        dni, empresa_id, tipo_empleado_id, horario_corrido)
    try:
        colaboradores = controlador_py_logger_get_filtered(
            dni=dni,
            empresa_id=empresa_id,
            tipo_empleado_id=tipo_empleado_id,
            horario_corrido=horario_corrido,
            db=db
        )
        colaboradores_schema = [ColaboradorResponse.model_validate(c) for c in colaboradores]
        data = [cs.model_dump() for cs in colaboradores_schema]
        return success_response("Colaboradores filtrados encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=500)

@router.get("/id/{colaborador_id}", response_model=ColaboradorResponse)
def get_colaborador(
        colaborador_id: int, 
        db: Session = Depends(get_db_factory("rrhh")),
        current_user = Depends(get_current_user_from_cookie),
        role = Depends(require_roles("superadmin", "admin", "supervisor"))
    ):
    """
    Endpoint para obtener la información de un colaborador por ID.
    """
    try:
        colaborador = controlador_py_logger_get_by_id(colaborador_id, db)
        colaborador_schema = ColaboradorResponse.model_validate(colaborador)
        return success_response("Colaborador encontrado", data=colaborador_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=500)

@router.get("/legajo/{colaborador_legajo}", response_model=ColaboradorResponse)
def get_colaborador_by_legajo(
        colaborador_legajo: int, 
        db: Session = Depends(get_db_factory("rrhh")),
        current_user = Depends(get_current_user_from_cookie),
        role = Depends(require_roles("superadmin", "admin", "supervisor"))):
    """
    Endpoint para obtener un colaborador por legajo.
    """
    try:
        colaborador = controlador_py_logger_get_by_legajo(colaborador_legajo, db)
        colaborador_schema = ColaboradorResponse.model_validate(colaborador)
        return success_response("Colaborador encontrado", data=colaborador_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=500)

@router.get("/details/{colaborador_id}", response_model=ColaboradorDetailSchema)
def get_colaborador_details_endpoint(
        colaborador_id: int, 
        db: Session = Depends(get_db_factory("rrhh")),
        current_user = Depends(get_current_user_from_cookie),
        role = Depends(require_roles("superadmin", "admin", "supervisor"))
    ):
    try:
        colaborador = controlador_py_logger_get_details(colaborador_id, db)
        colaborador_schema = ColaboradorDetailSchema.model_validate(colaborador)
        data = jsonable_encoder(colaborador_schema)
        return success_response("Colaborador encontrado", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_colaborador_details_endpoint: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=ColaboradorResponse)
def create_colaborador(
        colaborador_data: ColaboradorBase, 
        db: Session = Depends(get_db_factory("rrhh")),
        current_user = Depends(get_current_user_from_cookie),
        role = Depends(require_roles("superadmin", "admin"))
    ):
    """
    Endpoint para crear un nuevo Colaborador.
    """
    try:
        nueva_colaborador = Colaborador(**colaborador_data.model_dump())
        creado = controlador_py_logger_create_colaborador(nueva_colaborador, db)
        colaborador_schema = ColaboradorResponse.model_validate(creado)
        return success_response("Colaborador creado exitosamente", data=colaborador_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_colaborador: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{colaborador_id}", response_model=ColaboradorResponse)
def update_colaborador_partial(
    colaborador_id: int,
    colaborador_update: ColaboradorUpdate,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para actualizar parcialmente un Colaborador.
    Solo se actualizarán los campos que se envíen en el body.
    """
    try:
        colaborador_actual = controlador_py_logger_get_by_id(colaborador_id, db)
        update_data = colaborador_update.model_dump(exclude_unset=True)
        current_data = {
            "id": colaborador_actual.id,
            "nombre": colaborador_actual.nombre,
            "email": colaborador_actual.email,
            "telefono": colaborador_actual.telefono,
            "dni": colaborador_actual.dni,
            "empresa_id": colaborador_actual.empresa_id,
            "tipo_empleado_id": colaborador_actual.tipo_empleado_id,
            "horario_corrido": colaborador_actual.horario_corrido,
            "legajo": colaborador_actual.legajo
        }
        current_data.update(update_data)
        colaborador_to_update = Colaborador(**current_data)
        actualizado = controlador_py_logger_update_colaborador(colaborador_to_update, db)
        colaborador_schema = ColaboradorResponse.model_validate(actualizado)
        return success_response("Colaborador actualizado exitosamente", data=colaborador_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_colaborador_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{colaborador_id}")
def delete_colaborador(
    colaborador_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin"))
):
    """
    Endpoint para eliminar un Colaborador por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_colaborador(colaborador_id, db)
        return success_response("Colaborador eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_colaborador: %s", e)
        return error_response(str(e), status_code=500)
    
@router.put("/full/{colaborador_id}", response_model=ColaboradorResponse)
def update_colaborador_full(
    colaborador_id: int,
    colaborador_full_update: ColaboradorFullUpdate,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
) -> ColaboradorResponse:
    """
    Endpoint para actualizar completamente un colaborador, delegando la lógica al servicio.
    """
    try:
        data = update_full_colaborador_service(colaborador_id, colaborador_full_update, db)
        return success_response("Colaborador actualizado exitosamente", data=data, status_code=status.HTTP_200_OK)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_colaborador_full: %s", e)
        return error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get("/{colaborador_id}/horarios", response_model=List[dict])
def get_horarios_asignados(
    colaborador_id: int,
    fecha_desde: date = Query(...),
    fecha_hasta: date = Query(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener los horarios asignados a un colaborador en un rango de fechas.
    """
    try:
        horarios = controlador_py_logger_get_horarios_asignados(colaborador_id, fecha_desde, fecha_hasta, db)
        return success_response("Horarios asignados encontrados", data=horarios)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_asignados: %s", e)
        return error_response(str(e), status_code=500)
# ROUTER_PY_SCHEMA_SUCURSAL
from fastapi import APIRouter, HTTPException, Depends
from typing import List, Generator
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from infrastructure.schemas.sucursal import SucursalResponse, SucursalBase, SucursalUpdate, SucursalEditResponse
from infrastructure.databases.models.sucursal import Sucursal
from application.services.sucursal_service import get_sucursal_details
from application.controllers.sucursal_controller import (
    controlador_py_logger_get_by_id_sucursal,
    controlador_py_logger_get_all_sucursales,
    controlador_py_logger_create_sucursal,
    controlador_py_logger_update_sucursal_partial,
    controlador_py_logger_delete_sucursal,
    controlador_py_logger_get_by_nombre_sucursal,
    controlador_py_logger_get_by_empresa,
    controlador_py_logger_get_horarios,
    controlador_update_full_sucursal
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger
from infrastructure.schemas.sucursal import SucursalFullUpdate, SucursalResponse
from infrastructure.schemas.horario_sucursal import HorarioSucursalUpdate
from infrastructure.databases.config.database import DBConfig

router = APIRouter(prefix="/sucursales", tags=["Sucursales"])
logger = setup_logger(__name__, "logs/sucursal.log")

def get_rrhh_session() -> Generator[Session, None, None]:
    yield from DBConfig.get_db_session("rrhh")

@router.get("/id/{sucursal_id}", response_model=SucursalResponse)
def get_sucursal_by_id(sucursal_id: int):
    """
    Endpoint para obtener una Sucursal por su ID.
    """
    try:
        sucursal = controlador_py_logger_get_by_id_sucursal(sucursal_id)
        sucursal_schema = SucursalResponse.model_validate(sucursal)
        return success_response("Sucursal encontrada", data=sucursal_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_sucursal_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/", response_model=List[SucursalResponse])
def get_all_sucursales():
    """
    Endpoint para obtener todas las Sucursales.
    """
    try:
        sucursales = controlador_py_logger_get_all_sucursales()
        sucursales_schema = [SucursalResponse.model_validate(s) for s in sucursales]
        data = [ss.model_dump() for ss in sucursales_schema]
        return success_response("Sucursales encontradas", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_sucursales: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=SucursalResponse)
def create_sucursal(sucursal_data: SucursalBase):
    """
    Endpoint para crear una nueva Sucursal.
    """
    try:
        # Convertir el body (SucursalBase) en una instancia del modelo SQLAlchemy
        nueva_sucursal = Sucursal(**sucursal_data.model_dump())
        creada = controlador_py_logger_create_sucursal(nueva_sucursal)
        sucursal_schema = SucursalResponse.model_validate(creada)
        return success_response("Sucursal creada exitosamente", data=sucursal_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{sucursal_id}", response_model=SucursalResponse)
def update_sucursal_partial(sucursal_id: int, sucursal_update: SucursalUpdate):
    """
    Endpoint para actualizar parcialmente una Sucursal.
    Solo se actualizarán los campos enviados en el body.
    """
    try:
        update_data = sucursal_update.dict(exclude_unset=True)
        actualizado = controlador_py_logger_update_sucursal_partial(sucursal_id, update_data)
        sucursal_schema = SucursalResponse.model_validate(actualizado)
        return success_response("Sucursal actualizada exitosamente", data=sucursal_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_sucursal_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{sucursal_id}")
def delete_sucursal(sucursal_id: int):
    """
    Endpoint para eliminar una Sucursal por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_sucursal(sucursal_id)
        return success_response("Sucursal eliminada exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_sucursal: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/nombre/{nombre}", response_model=SucursalResponse)
def get_sucursal_by_nombre(nombre: str):
    """
    Endpoint para obtener una Sucursal por su nombre.
    """
    try:
        sucursal = controlador_py_logger_get_by_nombre_sucursal(nombre)
        sucursal_schema = SucursalResponse.model_validate(sucursal)
        return success_response("Sucursal encontrada", data=sucursal_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_sucursal_by_nombre: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/empresa/{empresa_id}", response_model=List[SucursalResponse])
def get_sucursales_by_empresa(empresa_id: int):
    """
    Endpoint para obtener todas las Sucursales asociadas a una Empresa.
    """
    try:
        sucursales = controlador_py_logger_get_by_empresa(empresa_id)
        sucursales_schema = [SucursalResponse.model_validate(s) for s in sucursales]
        data = [ss.model_dump() for ss in sucursales_schema]
        return success_response("Sucursales de la Empresa encontradas", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_sucursales_by_empresa: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/{sucursal_id}/horarios", response_model=List)
def get_horarios_by_sucursal(sucursal_id: int):
    """
    Endpoint para obtener la lista de horarios asignados a una Sucursal.
    """
    try:
        horarios = controlador_py_logger_get_horarios(sucursal_id)
        # Si dispones de un esquema para Horario, sería recomendable usarlo.
        # Por ahora, se retorna una lista de representaciones.
        data = [str(horario) for horario in horarios]
        return success_response("Horarios obtenidos", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_sucursal: %s", e)
        return error_response(str(e), status_code=500)
    
@router.get("/{sucursal_id}/details", response_model=SucursalEditResponse)
def controlador_get_sucursal_details(
    sucursal_id: int
) -> SucursalEditResponse:
    """
    Controlador para obtener los detalles completos de una sucursal.
    Se utiliza la función get_sucursal_details para centralizar y procesar la información.
    """
    try:
        # Se llama al servicio que reúne todos los datos de la sucursal.
        details = get_sucursal_details(sucursal_id)
        if not details:
            raise HTTPException(status_code=404, detail="Sucursal no encontrada")
        return success_response("Sucursal actualizada exitosamente", data=details)
    except Exception as error:
        # Captura y retorna el error en caso de falla.
        raise HTTPException(status_code=500, detail=str(error))

@router.put("/full/{sucursal_id}", response_model=SucursalResponse)
def update_sucursal_full(
    sucursal_id: int,
    sucursal_full_update: SucursalFullUpdate = Depends(),  # También se puede usar Body(...)
    db: Session = Depends(get_rrhh_session)
):
    """
    Endpoint para actualizar completamente una sucursal y sus objetos asociados:
      - Actualiza los datos básicos de la sucursal.
      - Actualiza, crea o elimina filas de HorarioSucursal.
      - Actualiza, crea o elimina filas de EspacioDisponibleSucursal.
      - Deriva y actualiza el campo 'dias_atencion' a partir de los horarios actualizados.
    Toda la operación se ejecuta en una transacción.
    """
    try:
        updated = controlador_update_full_sucursal(sucursal_id, sucursal_full_update, db)
        sucursal_schema = SucursalResponse.model_validate(updated)
        data = jsonable_encoder(sucursal_schema.model_dump())
        return success_response("Sucursal actualizada exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_sucursal_full: %s", e)
        return error_response(str(e), status_code=500)
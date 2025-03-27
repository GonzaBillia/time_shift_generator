from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from datetime import time
from typing import List, Optional, Generator
from application.config.logger_config import setup_logger
from fastapi.encoders import jsonable_encoder
from application.controllers.colaborador_controller import(
    controlador_py_logger_get_all, 
    controlador_py_logger_get_filtered, 
    controlador_py_logger_get_by_id, 
    controlador_py_logger_get_by_legajo,
    controlador_py_logger_get_details,
    controlador_py_logger_create_colaborador,
    controlador_py_logger_update_colaborador,
    controlador_py_logger_delete_colaborador,
    controlador_py_logger_get_paginated
)
from application.controllers.horario_preferido_colaborador_controller import (
    controlador_py_logger_get_by_id_horario_preferido_colaborador,
    controlador_py_logger_get_by_colaborador,
    controlador_py_logger_update_horario_preferido_colaborador,
    controlador_py_logger_create_horario_preferido_colaborador,
    controlador_py_logger_delete_horario_preferido_colaborador
)
from application.controllers.colaborador_sucursal_controller import (
    controlador_get_by_colaborador,
    controlador_create_colaborador_sucursal,
    controlador_delete_colaborador_sucursal
)
from application.services.colaborador_service import convertir_recursivamente
from application.helpers.response_handler import error_response, success_response
from infrastructure.schemas.colaborador import ColaboradorResponse, ColaboradorBase, ColaboradorUpdate
from infrastructure.schemas.colaborador_sucursal import ColaboradorSucursalBase
from infrastructure.schemas.horario_preferido_colaborador import HorarioPreferidoColaboradorBase
from infrastructure.schemas.colaborador_details import ColaboradorDetailSchema, ColaboradorFullUpdate
from infrastructure.databases.models.colaborador import Colaborador
from infrastructure.databases.models.colaborador_sucursal import ColaboradorSucursal
from infrastructure.databases.config.database import DBConfig 

logger = setup_logger(__name__)
router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

def get_rrhh_session() -> Generator[Session, None, None]:
    yield from DBConfig.get_db_session("rrhh")

@router.get("/all", response_model=List[ColaboradorResponse])
def get_all_colaboradores(page: int = Query(1, ge=1), limit: int = Query(20, ge=1), search: str = Query("", alias="search")):
    """
    Endpoint para obtener los colaboradores de forma paginada.
    Parámetros:
      - page: número de página (empezando en 1)
      - limit: cantidad de colaboradores por página
    """
    try:
        colaboradores = controlador_py_logger_get_paginated(page, limit, search)
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
    horario_corrido: Optional[bool] = Query(None, description="Indica si el colaborador tiene horario corrido")
):
    """
    Endpoint para obtener colaboradores filtrados por DNI, empresa, tipo de empleado y horario corrido.
    Todos los parámetros son opcionales y se combinan para filtrar los resultados.
    """
    logger.info("Endpoint /filters accedido con parámetros: dni=%s, empresa_id=%s, tipo_empleado_id=%s, horario_corrido=%s", 
        dni, empresa_id, tipo_empleado_id, horario_corrido)
    try:
        colaboradores = controlador_py_logger_get_filtered(
            dni=dni,
            empresa_id=empresa_id,
            tipo_empleado_id=tipo_empleado_id,
            horario_corrido=horario_corrido,
        )
        colaboradores_schema = [ColaboradorResponse.model_validate(c) for c in colaboradores]
        data = [cs.model_dump() for cs in colaboradores_schema]
        return success_response("Colaboradores filtrados encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=500)

@router.get("/id/{colaborador_id}", response_model=ColaboradorResponse)
def get_colaborador(colaborador_id: int):
    """
    Endpoint para obtener la información de un colaborador por ID.
    
    Se utiliza el controlador 'controlador_py_logger_get_by_id' para recuperar
    el colaborador, se valida y se transforma en un esquema Pydantic y se retorna
    en un formato de respuesta estandarizado.
    """
    try:
        # Recupera el colaborador usando el controlador con logging
        colaborador = controlador_py_logger_get_by_id(colaborador_id)
        # Valida y transforma la instancia en un esquema Pydantic usando model_validate (Pydantic v2)
        colaborador_schema = ColaboradorResponse.model_validate(colaborador)
        # Convierte el esquema a dict y retorna la respuesta exitosa
        return success_response("Colaborador encontrado", data=colaborador_schema.model_dump())
    except HTTPException as he:
        # Propaga las excepciones HTTP (404, 500, etc.) generadas en el controlador
        raise he
    except Exception as e:
        # Para otras excepciones inesperadas, retorna una respuesta de error con status 500
        return error_response(str(e), status_code=500)


@router.get("/legajo/{colaborador_legajo}", response_model=ColaboradorResponse)
def get_colaborador_by_legajo(colaborador_legajo: int):
    """
    Endpoint para obtener un colaborador por legajo.
    """
    try:
        colaborador = controlador_py_logger_get_by_legajo(colaborador_legajo)
        colaborador_schema = ColaboradorResponse.model_validate(colaborador)
        return success_response("Colaborador encontrado", data=colaborador_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=500)

@router.get("/details/{colaborador_id}", response_model=ColaboradorDetailSchema)
def get_colaborador_details_endpoint(colaborador_id: int):
    try:
        colaborador = controlador_py_logger_get_details(colaborador_id)
        colaborador_schema = ColaboradorDetailSchema.model_validate(colaborador)
        data = jsonable_encoder(colaborador_schema)
        return success_response("Colaborador encontrado", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_colaborador_details_endpoint: %s", e)
        return error_response(str(e), status_code=500)


@router.post("/", response_model=ColaboradorResponse)
def create_colaborador(colaborador_data: ColaboradorBase):
    """
    Endpoint para crear un nuevo Colaborador.
    """
    try:
        nueva_colaborador = Colaborador(**colaborador_data.model_dump())
        creado = controlador_py_logger_create_colaborador(nueva_colaborador)
        colaborador_schema = ColaboradorResponse.model_validate(creado)
        return success_response("Colaborador creado exitosamente", data=colaborador_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_colaborador: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{colaborador_id}", response_model=ColaboradorResponse)
def update_colaborador_partial(colaborador_id: int, colaborador_update: ColaboradorUpdate):
    """
    Endpoint para actualizar parcialmente un Colaborador.
    Solo se actualizarán los campos que se envíen en el body.
    """
    try:
        # Recuperar el registro actual
        colaborador_actual = controlador_py_logger_get_by_id(colaborador_id)
        
        # Extraer datos enviados, excluyendo los que no se establecieron
        update_data = colaborador_update.model_dump(exclude_unset=True)
        
        # Convertir el registro actual en un diccionario
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
        
        # Actualizar los datos actuales con los nuevos valores
        current_data.update(update_data)
        
        # Crear la instancia del modelo con los datos combinados
        colaborador_to_update = Colaborador(**current_data)
        
        # Actualizar usando el controlador
        actualizado = controlador_py_logger_update_colaborador(colaborador_to_update)
        colaborador_schema = ColaboradorResponse.model_validate(actualizado)
        return success_response("Colaborador actualizado exitosamente", data=colaborador_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_colaborador_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{colaborador_id}")
def delete_colaborador(colaborador_id: int):
    """
    Endpoint para eliminar un Colaborador por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_colaborador(colaborador_id)
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
    db: Session = Depends(get_rrhh_session)
):
    """
    Endpoint para actualizar completamente un colaborador, incluyendo:
    - Los datos básicos (solo se actualizan los campos enviados)
    - La lista de horarios preferidos: se actualizan los existentes (si vienen con id), se crean nuevos o se eliminan
    - Relaciones colaborador_sucursal: a partir de dos listas (roles y sucursales) se extrae el id de cada objeto
      para crear o eliminar las relaciones correspondientes.
    Toda la operación se ejecuta en una transacción.
    """
    try:
        with db.begin():
            # Recuperar el colaborador actual
            colaborador_actual = controlador_py_logger_get_by_id(colaborador_id, db)
            if not colaborador_actual:
                raise HTTPException(status_code=404, detail="Colaborador no encontrado")
            
            # Actualizar los campos del colaborador (solo los enviados)
            update_data = colaborador_full_update.colaborador.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(colaborador_actual, key, value)
            
            # 1. Actualizar los horarios preferidos
            current_horarios = controlador_py_logger_get_by_colaborador(colaborador_actual.id, db)
            current_horario_ids = {h.id for h in current_horarios if h.id is not None}
            payload_horario_ids = {h.id for h in colaborador_full_update.horario_preferido if h.id}
            
            # Eliminar horarios que ya no vienen en el payload
            to_delete_horarios = current_horario_ids - payload_horario_ids
            for del_id in to_delete_horarios:
                controlador_py_logger_delete_horario_preferido_colaborador(del_id, db)
            
            updated_horarios = []
            for horario_data in colaborador_full_update.horario_preferido:
                if horario_data.id:  # Si se envía un id, se intenta actualizar
                    horario_actual = controlador_py_logger_get_by_id_horario_preferido_colaborador(horario_data.id, db)
                    if horario_actual:
                        update_horario = horario_data.model_dump(exclude_unset=True)
                        for key, value in update_horario.items():
                            setattr(horario_actual, key, value)
                        actualizado_horario = controlador_py_logger_update_horario_preferido_colaborador(horario_actual, db)
                        updated_horarios.append(actualizado_horario)
                    else:
                        nuevo_horario = HorarioPreferidoColaboradorBase(**horario_data.model_dump())
                        creado = controlador_py_logger_create_horario_preferido_colaborador(nuevo_horario, db)
                        updated_horarios.append(creado)
                else:
                    nuevo_horario = HorarioPreferidoColaboradorBase(**horario_data.model_dump())
                    creado = controlador_py_logger_create_horario_preferido_colaborador(nuevo_horario, db)
                    updated_horarios.append(creado)
            
            # 2. Actualizar las relaciones colaborador_sucursal a partir de roles y sucursales
            if colaborador_full_update.roles is not None and colaborador_full_update.sucursales is not None:
                payload_relaciones = set()
                # Caso: un solo rol para varias sucursales
                if len(colaborador_full_update.roles) == 1 and len(colaborador_full_update.sucursales) >= 1:
                    role_id = colaborador_full_update.roles[0].id
                    for sucursal in colaborador_full_update.sucursales:
                        payload_relaciones.add((role_id, sucursal.id))
                # Caso: una sola sucursal para varios roles
                elif len(colaborador_full_update.sucursales) == 1 and len(colaborador_full_update.roles) >= 1:
                    sucursal_id = colaborador_full_update.sucursales[0].id
                    for role in colaborador_full_update.roles:
                        payload_relaciones.add((role.id, sucursal_id))
                # Caso: ambas listas tienen la misma longitud y se emparejan por índice
                elif len(colaborador_full_update.roles) == len(colaborador_full_update.sucursales):
                    roles_ids = [role.id for role in colaborador_full_update.roles]
                    sucursales_ids = [sucursal.id for sucursal in colaborador_full_update.sucursales]
                    payload_relaciones = set(zip(roles_ids, sucursales_ids))
                else:
                    raise HTTPException(
                        status_code=400,
                        detail="La cantidad de roles y sucursales no coincide y no se puede inferir una relación única"
                    )
                
                # Obtener las relaciones actuales para el colaborador
                relaciones_actuales = controlador_get_by_colaborador(colaborador_actual.id, db)
                current_set = {(rel.rol_colaborador_id, rel.sucursal_id) for rel in relaciones_actuales}
                
                # Eliminar relaciones que existen en la BD pero no vienen en el payload
                relaciones_to_delete = current_set - payload_relaciones
                for rel in relaciones_actuales:
                    if (rel.rol_colaborador_id, rel.sucursal_id) in relaciones_to_delete:
                        controlador_delete_colaborador_sucursal(rel.id, db)
                
                # Agregar nuevas relaciones que vienen en el payload pero no existen en la BD
                relaciones_to_add = payload_relaciones - current_set
                for role_id, sucursal_id in relaciones_to_add:
                    # Crear el objeto utilizando el patrón model_dump() como en horarios preferidos
                    nueva_relacion_data = ColaboradorSucursalBase(
                        colaborador_id=colaborador_actual.id,
                        rol_colaborador_id=role_id,
                        sucursal_id=sucursal_id
                    )
                    nueva_relacion = ColaboradorSucursal(**nueva_relacion_data.model_dump())
                    controlador_create_colaborador_sucursal(nueva_relacion, db)
            
            # 3. Actualizar el colaborador en la base de datos
            actualizado = controlador_py_logger_update_colaborador(colaborador_actual, db)
            colaborador_schema = ColaboradorResponse.model_validate(actualizado)
            return success_response("Colaborador actualizado exitosamente", data=colaborador_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_colaborador_full: %s", e)
        return error_response(str(e), status_code=500)

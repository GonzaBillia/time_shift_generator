from fastapi import HTTPException
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from application.config.logger_config import setup_logger
from infrastructure.schemas.sucursal import SucursalFullUpdate, SucursalEditResponse
from infrastructure.databases.models.sucursal import Sucursal
from infrastructure.databases.models.horario_sucursal import HorarioSucursal
from infrastructure.databases.models.espacio_disponible_sucursal import EspacioDisponibleSucursal
from infrastructure.repositories.sucursal_repo import SucursalRepository
from infrastructure.repositories.horario_sucursal_repo import HorarioSucursalRepository
from infrastructure.repositories.espacio_disponible_sucursal_repo import EspacioDisponibleSucursalRepository
from application.controllers.empresa_controller import controlador_py_logger_get_by_id_empresa
from application.controllers.formato_controller import controlador_py_logger_get_by_id_formato
from application.controllers.formatos_roles_controller import controlador_py_logger_get_roles_by_formato
from application.controllers.colaborador_sucursal_controller import controlador_get_colaboradores_by_sucursal
from application.controllers.horario_sucursal_controller import controlador_py_logger_get_by_sucursal
from application.controllers.espacio_disponible_sucursal_controller import controlador_py_logger_get_espacios_by_sucursal

logger = setup_logger(__name__, "logs/sucursal_full_service.log")

def get_sucursal_details(sucursal_id: int, db: Session) -> SucursalEditResponse:
    # 1. Obtener la sucursal por su ID.
    sucursal = SucursalRepository.get_by_id(sucursal_id, db)
    if not sucursal:
        raise ValueError("Sucursal no encontrada")
    
    # 2. Obtener la empresa asociada.
    empresa = controlador_py_logger_get_by_id_empresa(sucursal.empresa_id, db)
    
    # 3. Obtener el mapeo de formatos para el formato de la sucursal.
    formato_obj = controlador_py_logger_get_by_id_formato(sucursal.formato_id, db)
    
    # 4. Obtener los roles asociados al formato.
    roles = controlador_py_logger_get_roles_by_formato(sucursal.formato_id, db)
    
    # 5. Obtener los colaboradores asignados a la sucursal.
    colaboradores = controlador_get_colaboradores_by_sucursal(sucursal.id, db)
    countColabs = len(colaboradores) if colaboradores else 0
    
    # 6. Obtener los horarios asignados a la sucursal.
    horarios = controlador_py_logger_get_by_sucursal(sucursal.id, db)
    
    # 7. Obtener los espacios disponibles para la sucursal.
    espacios = controlador_py_logger_get_espacios_by_sucursal(sucursal.id, db)
    
    # 8. Construir y retornar el objeto con la información completa.
    sucursal_details: Dict[str, Any] = {
        "id": sucursal.id,
        "nombre": sucursal.nombre,
        "direccion": sucursal.direccion,
        "telefono": sucursal.telefono,
        "empresa_id": sucursal.empresa_id,
        "formato_id": sucursal.formato_id,
        "formato": formato_obj.nombre if formato_obj else None,
        "empresa": empresa.razon_social if empresa else None,
        "roles": roles,
        "colaboradores": colaboradores,
        "countColabs": countColabs,
        "horarios": horarios,
        "espacio": espacios
    }
    
    return sucursal_details


def update_full_sucursal(sucursal_id: int, data: SucursalFullUpdate, db: Session) -> Sucursal:
    """
    Actualiza completamente una sucursal y sus objetos asociados:
      - Actualiza los campos básicos de la sucursal.
      - Actualiza, crea o elimina filas de HorarioSucursal.
      - Actualiza, crea o elimina filas de EspacioDisponibleSucursal.
      - Deriva y actualiza el campo 'dias_atencion' a partir de los horarios actualizados.
    Toda la operación se realiza en una transacción.
    
    Nota: Es importante que los métodos de los repositorios (create, update, delete) utilicen db.flush()
    para enviar los cambios sin finalizar la transacción, permitiendo que la transacción se confirme al final.
    """
    try:
        with db.begin():
            # 1. Recuperar la sucursal actual.
            sucursal_actual = SucursalRepository.get_by_id(sucursal_id, db)
            if not sucursal_actual:
                raise HTTPException(status_code=404, detail="Sucursal no encontrada")
            
            # 2. Actualizar campos básicos de la sucursal (excluyendo relaciones).
            basic_update_data = data.model_dump(
                exclude_unset=True,
                exclude={"horario", "horarios", "espacio", "roles", "colaboradores"}
            )
            for key, value in basic_update_data.items():
                if value is not None:
                    setattr(sucursal_actual, key, value)
            
            # 3. Procesar HorarioSucursal.
            current_horarios = HorarioSucursalRepository.get_by_sucursal(sucursal_id, db)
            current_ids = {h.id for h in current_horarios if h.id is not None}
            payload_ids = {h_data.id for h_data in data.horarios if h_data.id}
            to_delete_ids = current_ids - payload_ids
            for del_id in to_delete_ids:
                HorarioSucursalRepository.delete(del_id, db)
            
            updated_horarios = []
            for horario_data in data.horarios:
                horario_dict = horario_data.model_dump()
                # Asegurar que se asigna el sucursal_id si no viene en el payload.
                if not horario_dict.get("sucursal_id"):
                    horario_dict["sucursal_id"] = sucursal_id
                if horario_data.id:
                    horario_actual = HorarioSucursalRepository.get_by_id(horario_data.id, db)
                    if horario_actual:
                        update_horario = horario_data.model_dump(exclude_unset=True)
                        for key, value in update_horario.items():
                            setattr(horario_actual, key, value)
                        updated = HorarioSucursalRepository.update(horario_actual, db)
                        updated_horarios.append(updated)
                    else:
                        nuevo = HorarioSucursal(**horario_dict)
                        creado = HorarioSucursalRepository.create(nuevo, db)
                        updated_horarios.append(creado)
                else:
                    nuevo = HorarioSucursal(**horario_dict)
                    creado = HorarioSucursalRepository.create(nuevo, db)
                    updated_horarios.append(creado)
            
            # 4. Procesar EspacioDisponibleSucursal.
            current_espacios = EspacioDisponibleSucursalRepository.get_by_sucursal(sucursal_id, db)
            current_esp_ids = {e.id for e in current_espacios if e.id is not None}
            payload_esp_ids = {esp_data.id for esp_data in data.espacio if esp_data.id}
            to_delete_esp_ids = current_esp_ids - payload_esp_ids
            for del_id in to_delete_esp_ids:
                EspacioDisponibleSucursalRepository.delete(del_id, db)
            
            updated_espacios = []
            for esp_data in data.espacio:
                esp_dict = esp_data.model_dump()
                if not esp_dict.get("sucursal_id"):
                    esp_dict["sucursal_id"] = sucursal_id
                if esp_data.id:
                    espacio_actual = EspacioDisponibleSucursalRepository.get_by_id(esp_data.id, db)
                    if espacio_actual:
                        update_esp = esp_data.model_dump(exclude_unset=True)
                        for key, value in update_esp.items():
                            setattr(espacio_actual, key, value)
                        updated = EspacioDisponibleSucursalRepository.update(espacio_actual, db)
                        updated_espacios.append(updated)
                    else:
                        nuevo_esp = EspacioDisponibleSucursal(**esp_dict)
                        creado = EspacioDisponibleSucursalRepository.create(nuevo_esp, db)
                        updated_espacios.append(creado)
                else:
                    nuevo_esp = EspacioDisponibleSucursal(**esp_dict)
                    creado = EspacioDisponibleSucursalRepository.create(nuevo_esp, db)
                    updated_espacios.append(creado)
            
            # 5. Actualizar la sucursal en la base de datos.
            updated_sucursal = SucursalRepository.update(sucursal_actual, db)
            return updated_sucursal
    except Exception as e:
        logger.error("Error en update_full_sucursal: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e

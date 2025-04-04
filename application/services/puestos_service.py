from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.models.puestos import Puesto
from infrastructure.repositories.puesto_repo import PuestoRepository

def crear_puesto(
    sucursal_id: int,
    rol_colaborador_id: int,
    dia_id: int,
    fecha: date,
    nombre: str,
    db: Session,
    colaborador_id: Optional[int] = None
) -> Puesto:
    """
    Crea un nuevo puesto para una sucursal, rol, día y fecha específicos.
    El campo 'colaborador_id' se asigna en la fase de asignación.
    """
    nuevo_puesto = Puesto(
        sucursal_id=sucursal_id,
        rol_colaborador_id=rol_colaborador_id,
        dia_id=dia_id,
        fecha=fecha,
        nombre=nombre,
        colaborador_id=colaborador_id
    )
    return PuestoRepository.create(nuevo_puesto, db)

def create_multiple_puestos(puestos: List[Puesto], db: Session) -> List[Puesto]:
    """
    Crea múltiples puestos en la base de datos utilizando el repositorio.
    
    :param puestos: Lista de objetos Puesto a crear.
    :param db: Sesión de base de datos.
    :return: Lista de objetos Puesto creados, con sus atributos actualizados (por ejemplo, id).
    """
    try:
        return PuestoRepository.create_many(puestos, db)
    except Exception as e:
        raise e

def actualizar_puesto(puesto_data: dict, db: Session) -> Puesto:
    """
    Actualiza un puesto existente. Se espera que puesto_data contenga el 'id' y los campos a modificar.
    """
    puesto = Puesto(**puesto_data)
    return PuestoRepository.update(puesto, db)

def actualizar_varios_puestos(puesto_data: List[dict], db: Session) -> List[Puesto]:
    """
    Actualiza varios puestos existentes. Se espera que cada diccionario en puesto_data contenga el 'id' y los campos a modificar.
    """
    puestos = [Puesto(**data) for data in puesto_data]
    return PuestoRepository.update_many(puestos, db)

def obtener_puestos_por_sucursal(sucursal_id: int, db: Session) -> List[Puesto]:
    """
    Retorna todos los puestos de una sucursal.
    """
    return PuestoRepository.get_by_sucursal(sucursal_id, db)

def delete_multiple_puestos(puesto_ids: List[int], db: Session) -> None:
    """
    Servicio para eliminar múltiples puestos.
    
    :param puesto_ids: Lista de IDs de los puestos a eliminar.
    :param db: Sesión de base de datos.
    """
    try:
        PuestoRepository.delete_many(puesto_ids, db)
    except Exception as error:
        raise error

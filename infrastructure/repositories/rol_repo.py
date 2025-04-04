from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from infrastructure.databases.models.rol import Rol
from infrastructure.databases.models.espacio_disponible_sucursal import EspacioDisponibleSucursal

class RolRepository:
    @staticmethod
    def get_by_id(rol_id: int, db: Session) -> Optional[Rol]:
        """
        Obtiene un Rol por su ID. Retorna None si no existe.
        Se carga de forma anticipada la relación 'formatos' para evitar lazy loading.
        """
        return db.query(Rol) \
            .options(joinedload(Rol.formatos)) \
            .filter_by(id=rol_id).first()

    @staticmethod
    def get_all(db: Session) -> List[Rol]:
        """
        Devuelve todos los Roles registrados en la base de datos.
        Se carga de forma anticipada la relación 'formatos' para evitar lazy loading.
        """
        return db.query(Rol) \
            .options(joinedload(Rol.formatos)) \
            .all()

    @staticmethod
    def create(rol: Rol, db: Session) -> Rol:
        """
        Crea un nuevo Rol en la base de datos.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(rol)
        db.flush()  # Sincroniza los cambios para asignar un ID si es necesario
        db.refresh(rol)
        return rol

    @staticmethod
    def update(rol: Rol, db: Session) -> Optional[Rol]:
        """
        Actualiza un Rol existente. Retorna el rol actualizado o None si no existe.
        Se asume que el commit se realizará externamente.
        """
        existente = db.query(Rol).filter_by(id=rol.id).first()
        if not existente:
            return None
        db_rol = db.merge(rol)
        db.flush()
        db.refresh(db_rol)
        return db_rol

    @staticmethod
    def delete(rol_id: int, db: Session) -> bool:
        """
        Elimina un Rol por su ID. Retorna True si se elimina, False si no existe.
        Se asume que el commit se realizará externamente.
        """
        rol = db.query(Rol).filter_by(id=rol_id).first()
        if rol:
            db.delete(rol)
            db.flush()
            return True
        return False

    @staticmethod
    def get_by_nombre(nombre: str, db: Session) -> Optional[Rol]:
        """
        Obtiene un Rol por su nombre. Retorna None si no existe.
        Se carga de forma anticipada la relación 'formatos' para evitar lazy loading.
        """
        return db.query(Rol) \
            .options(joinedload(Rol.formatos)) \
            .filter_by(nombre=nombre).first()

    @staticmethod
    def get_principales(db: Session) -> List[Rol]:
        """
        Devuelve todos los Roles marcados como 'principal=True'.
        Se carga de forma anticipada la relación 'formatos' para evitar lazy loading.
        """
        return db.query(Rol) \
            .options(joinedload(Rol.formatos)) \
            .filter_by(principal=True).all()
    
    @staticmethod
    def get_available_rols_by_sucursal(sucursal_id: int, db: Session) -> List[Rol]:
        """
        Obtiene los roles disponibles para una sucursal específica a partir de sus espacios disponibles.
        
        Se realiza un join entre Rol y EspacioDisponibleSucursal y se filtra por:
          - sucursal_id (de EspacioDisponibleSucursal)
          - cantidad > 0 (para considerar solo espacios con disponibilidad)
        
        Se utiliza distinct() para evitar roles duplicados en caso de que existan múltiples espacios para el mismo rol.
        """
        roles = (
            db.query(Rol)
            .join(EspacioDisponibleSucursal, Rol.id == EspacioDisponibleSucursal.rol_colaborador_id)
            .filter(
                EspacioDisponibleSucursal.sucursal_id == sucursal_id,
                EspacioDisponibleSucursal.cantidad > 0
            )
            .distinct()
            .all()
        )
        return roles

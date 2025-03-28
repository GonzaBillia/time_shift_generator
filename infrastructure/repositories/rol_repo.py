from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.rol import Rol
from infrastructure.databases.models.espacio_disponible_sucursal import EspacioDisponibleSucursal

class RolRepository:
    @staticmethod
    def get_by_id(rol_id: int) -> Optional[Rol]:
        """
        Obtiene un Rol por su ID. Retorna None si no existe.
        Se carga de forma anticipada la relación 'formatos' para evitar lazy loading.
        """
        session: Session = Database.get_session("rrhh")
        rol = session.query(Rol) \
            .options(joinedload(Rol.formatos)) \
            .filter_by(id=rol_id).first()
        session.close()
        return rol

    @staticmethod
    def get_all() -> List[Rol]:
        """
        Devuelve todos los Roles registrados en la base de datos.
        Se carga de forma anticipada la relación 'formatos' para evitar lazy loading.
        """
        session: Session = Database.get_session("rrhh")
        roles = session.query(Rol) \
            .options(joinedload(Rol.formatos)) \
            .all()
        session.close()
        return roles

    @staticmethod
    def create(rol: Rol) -> Rol:
        """
        Crea un nuevo Rol en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(rol)
        session.commit()
        session.refresh(rol)
        session.close()
        return rol

    @staticmethod
    def update(rol: Rol) -> Optional[Rol]:
        """
        Actualiza un Rol existente. Retorna el rol actualizado o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        existente = session.query(Rol).filter_by(id=rol.id).first()
        if not existente:
            session.close()
            return None

        db_rol = session.merge(rol)
        session.commit()
        session.refresh(db_rol)
        session.close()
        return db_rol

    @staticmethod
    def delete(rol_id: int) -> bool:
        """
        Elimina un Rol por su ID. Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        rol = session.query(Rol).filter_by(id=rol_id).first()
        if rol:
            session.delete(rol)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def get_by_nombre(nombre: str) -> Optional[Rol]:
        """
        Obtiene un Rol por su nombre. Retorna None si no existe.
        Se carga de forma anticipada la relación 'formatos' para evitar lazy loading.
        """
        session: Session = Database.get_session("rrhh")
        rol = session.query(Rol) \
            .options(joinedload(Rol.formatos)) \
            .filter_by(nombre=nombre).first()
        session.close()
        return rol

    @staticmethod
    def get_principales() -> List[Rol]:
        """
        Devuelve todos los Roles marcados como 'principal=True'.
        Se carga de forma anticipada la relación 'formatos' para evitar lazy loading.
        """
        session: Session = Database.get_session("rrhh")
        roles = session.query(Rol) \
            .options(joinedload(Rol.formatos)) \
            .filter_by(principal=True).all()
        session.close()
        return roles
    
    @staticmethod
    def get_available_rols_by_sucursal(sucursal_id: int):
        """
        Obtiene los roles disponibles para una sucursal específica a partir de sus espacios disponibles.
        
        Se realiza un join entre Rol y EspacioDisponibleSucursal y se filtra por:
        - sucursal_id (de EspacioDisponibleSucursal)
        - cantidad > 0 (opcional, para considerar solo espacios con disponibilidad)
        
        Se utiliza distinct() para evitar roles duplicados en caso de que existan múltiples espacios para el mismo rol.
        """
        session: Session = Database.get_session("rrhh")
        roles = (
            session.query(Rol)
            .join(EspacioDisponibleSucursal, Rol.id == EspacioDisponibleSucursal.rol_colaborador_id)
            .filter(
                EspacioDisponibleSucursal.sucursal_id == sucursal_id,
                EspacioDisponibleSucursal.cantidad > 0  # Filtra solo si la cantidad es mayor a 0
            )
            .distinct()
            .all()
        )
        return roles

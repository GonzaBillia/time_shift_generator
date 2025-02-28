from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.rol import Rol

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

from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.rol import Rol
from typing import List, Optional

class RolRepository:
    @staticmethod
    def get_by_id(rol_id: int) -> Optional[Rol]:
        """Obtiene un rol por su ID."""
        session: Session = Database.get_session("rrhh")
        rol = session.query(Rol).filter_by(id=rol_id).first()
        session.close()
        return rol

    @staticmethod
    def get_all() -> List[Rol]:
        """Obtiene todos los roles registrados en la base de datos."""
        session: Session = Database.get_session("rrhh")
        roles = session.query(Rol).all()
        session.close()
        return roles

    @staticmethod
    def create(rol: Rol) -> Rol:
        """Crea un nuevo rol en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.add(rol)
        session.commit()
        session.refresh(rol)
        session.close()
        return rol

    @staticmethod
    def update(rol: Rol) -> Rol:
        """Actualiza un rol existente en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.merge(rol)
        session.commit()
        session.refresh(rol)
        session.close()
        return rol

    @staticmethod
    def delete(rol_id: int) -> bool:
        """Elimina un rol de la base de datos."""
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
        """Obtiene un rol por su nombre."""
        session: Session = Database.get_session("rrhh")
        rol = session.query(Rol).filter_by(nombre=nombre).first()
        session.close()
        return rol

    @staticmethod
    def get_principales() -> List[Rol]:
        """Obtiene todos los roles principales."""
        session: Session = Database.get_session("rrhh")
        roles = session.query(Rol).filter_by(principal=True).all()
        session.close()
        return roles

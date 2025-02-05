from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.formato import Formato
from infrastructure.databases.models.rol import Rol
from typing import List, Optional

class FormatoRepository:
    @staticmethod
    def get_by_id(formato_id: int) -> Optional[Formato]:
        """Obtiene un formato por su ID, incluyendo los roles asociados."""
        session: Session = Database.get_session("rrhh")
        formato = session.query(Formato).filter_by(id=formato_id).first()
        session.close()
        return formato

    @staticmethod
    def get_all() -> List[Formato]:
        """Obtiene todos los formatos registrados en la base de datos."""
        session: Session = Database.get_session("rrhh")
        formatos = session.query(Formato).all()
        session.close()
        return formatos

    @staticmethod
    def create(formato: Formato) -> Formato:
        """Crea un nuevo formato en la base de datos y asocia sus roles."""
        session: Session = Database.get_session("rrhh")
        session.add(formato)
        session.commit()
        session.refresh(formato)
        session.close()
        return formato

    @staticmethod
    def update(formato: Formato) -> Formato:
        """Actualiza un formato existente en la base de datos y sus roles."""
        session: Session = Database.get_session("rrhh")
        
        # Obtener el formato actual y actualizarlo
        formato_existente = session.query(Formato).filter_by(id=formato.id).first()
        if formato_existente:
            formato_existente.nombre = formato.nombre

            # Actualizar la relación Many-to-Many con `roles`
            formato_existente.roles.clear()
            for rol in formato.roles:
                formato_existente.roles.append(session.query(Rol).filter_by(id=rol.id).first())

            session.commit()
            session.refresh(formato_existente)
        session.close()
        return formato_existente

    @staticmethod
    def delete(formato_id: int) -> bool:
        """Elimina un formato de la base de datos y su relación con los roles."""
        session: Session = Database.get_session("rrhh")
        formato = session.query(Formato).filter_by(id=formato_id).first()
        if formato:
            session.delete(formato)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def get_by_nombre(nombre: str) -> Optional[Formato]:
        """Obtiene un formato por su nombre."""
        session: Session = Database.get_session("rrhh")
        formato = session.query(Formato).filter_by(nombre=nombre).first()
        session.close()
        return formato

    @staticmethod
    def get_roles_by_formato(formato_id: int) -> List[Rol]:
        """Obtiene los roles asociados a un formato específico."""
        session: Session = Database.get_session("rrhh")
        formato = session.query(Formato).filter_by(id=formato_id).first()
        session.close()
        return formato.roles if formato else []

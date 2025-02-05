from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.sucursal import Sucursal
from typing import List, Optional

class SucursalRepository:
    @staticmethod
    def get_by_id(sucursal_id: int) -> Optional[Sucursal]:
        """Obtiene una sucursal por su ID."""
        session: Session = Database.get_session("rrhh")
        sucursal = session.query(Sucursal).filter_by(id=sucursal_id).first()
        session.close()
        return sucursal

    @staticmethod
    def get_all() -> List[Sucursal]:
        """Obtiene todas las sucursales."""
        session: Session = Database.get_session("rrhh")
        sucursales = session.query(Sucursal).all()
        session.close()
        return sucursales

    @staticmethod
    def create(sucursal: Sucursal) -> Sucursal:
        """Crea una nueva sucursal en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.add(sucursal)
        session.commit()
        session.refresh(sucursal)
        session.close()
        return sucursal

    @staticmethod
    def update(sucursal: Sucursal) -> Sucursal:
        """Actualiza una sucursal en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.merge(sucursal)
        session.commit()
        session.refresh(sucursal)
        session.close()
        return sucursal

    @staticmethod
    def delete(sucursal_id: int) -> bool:
        """Elimina una sucursal de la base de datos."""
        session: Session = Database.get_session("rrhh")
        sucursal = session.query(Sucursal).filter_by(id=sucursal_id).first()
        if sucursal:
            session.delete(sucursal)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def get_by_nombre(nombre: str) -> Optional[Sucursal]:
        """Obtiene una sucursal por su nombre."""
        session: Session = Database.get_session("rrhh")
        sucursal = session.query(Sucursal).filter_by(nombre=nombre).first()
        session.close()
        return sucursal

    @staticmethod
    def get_by_empresa(empresa_id: int) -> List[Sucursal]:
        """Obtiene todas las sucursales de una empresa."""
        session: Session = Database.get_session("rrhh")
        sucursales = session.query(Sucursal).filter_by(empresa_id=empresa_id).all()
        session.close()
        return sucursales

    @staticmethod
    def get_horarios(sucursal_id: int) -> List:
        """Obtiene los horarios de una sucursal."""
        session: Session = Database.get_session("rrhh")
        sucursal = session.query(Sucursal).filter_by(id=sucursal_id).first()
        session.close()
        return sucursal.horarios if sucursal else []

    @staticmethod
    def esta_abierta(sucursal_id: int, dia_id: int) -> bool:
        """Verifica si la sucursal está abierta en un día específico."""
        session: Session = Database.get_session("rrhh")
        sucursal = session.query(Sucursal).filter_by(id=sucursal_id).first()
        session.close()
        return dia_id in sucursal.dias_atencion if sucursal else False

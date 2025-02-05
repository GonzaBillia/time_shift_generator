# archivo: infrastructure/repositories/sucursal_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.sucursal import Sucursal

class SucursalRepository:
    @staticmethod
    def get_by_id(sucursal_id: int) -> Optional[Sucursal]:
        """
        Obtiene una Sucursal por su ID. Retorna None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        sucursal = session.query(Sucursal).filter_by(id=sucursal_id).first()
        session.close()
        return sucursal

    @staticmethod
    def get_all() -> List[Sucursal]:
        """
        Devuelve la lista de todas las Sucursales.
        """
        session: Session = Database.get_session("rrhh")
        sucursales = session.query(Sucursal).all()
        session.close()
        return sucursales

    @staticmethod
    def create(sucursal: Sucursal) -> Sucursal:
        """
        Crea una nueva Sucursal en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(sucursal)
        session.commit()
        session.refresh(sucursal)
        session.close()
        return sucursal

    @staticmethod
    def update(sucursal: Sucursal) -> Optional[Sucursal]:
        """
        Actualiza una Sucursal existente. Retorna la sucursal actualizada o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        existente = session.query(Sucursal).filter_by(id=sucursal.id).first()
        if not existente:
            session.close()
            return None

        db_sucursal = session.merge(sucursal)
        session.commit()
        session.refresh(db_sucursal)
        session.close()
        return db_sucursal

    @staticmethod
    def delete(sucursal_id: int) -> bool:
        """
        Elimina una Sucursal por su ID. Retorna True si se elimina, False si no existe.
        """
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
        """
        Obtiene una Sucursal por su nombre. Retorna None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        sucursal = session.query(Sucursal).filter_by(nombre=nombre).first()
        session.close()
        return sucursal

    @staticmethod
    def get_by_empresa(empresa_id: int) -> List[Sucursal]:
        """
        Devuelve todas las Sucursales asociadas a una Empresa específica.
        """
        session: Session = Database.get_session("rrhh")
        sucursales = session.query(Sucursal).filter_by(empresa_id=empresa_id).all()
        session.close()
        return sucursales

    @staticmethod
    def get_horarios(sucursal_id: int) -> List:
        """
        Devuelve la lista de objetos 'Horario' asignados a la Sucursal.
        """
        session: Session = Database.get_session("rrhh")
        sucursal = session.query(Sucursal).filter_by(id=sucursal_id).first()
        horarios = sucursal.horarios if sucursal else []
        session.close()
        return horarios

    # COMENTADO: no existe 'dias_atencion' en el modelo Sucursal
    # @staticmethod
    # def esta_abierta(sucursal_id: int, dia_id: int) -> bool:
    #     ...

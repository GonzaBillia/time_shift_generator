from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.dia import Dia

class DiaRepository:
    @staticmethod
    def get_by_id(dia_id: int) -> Optional[Dia]:
        """
        Obtiene un día por su ID.
        """
        session: Session = Database.get_session("rrhh")
        dia = session.query(Dia).filter_by(id=dia_id).first()
        session.close()
        return dia

    @staticmethod
    def get_by_nombre(nombre: str) -> Optional[Dia]:
        """
        Obtiene un día por su nombre.
        Por ejemplo, 'Lunes', 'Martes', etc.
        """
        session: Session = Database.get_session("rrhh")
        dia = session.query(Dia).filter_by(nombre=nombre).first()
        session.close()
        return dia

    @staticmethod
    def get_all() -> List[Dia]:
        """
        Obtiene todos los días registrados en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        dias = session.query(Dia).all()
        session.close()
        return dias

    @staticmethod
    def create(dia: Dia) -> Dia:
        """
        Crea un nuevo registro de día en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(dia)
        session.commit()
        session.refresh(dia)
        session.close()
        return dia

    @staticmethod
    def update(dia: Dia) -> Dia:
        """
        Actualiza un día existente en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        db_dia = session.merge(dia)  # Devuelve la instancia unificada/persistida
        session.commit()
        session.refresh(db_dia)
        session.close()
        return db_dia

    @staticmethod
    def delete(dia_id: int) -> bool:
        """
        Elimina un día de la base de datos, por su ID.
        Retorna True si se eliminó correctamente.
        """
        session: Session = Database.get_session("rrhh")
        dia = session.query(Dia).filter_by(id=dia_id).first()
        if dia:
            session.delete(dia)
            session.commit()
            session.close()
            return True
        session.close()
        return False

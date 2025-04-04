from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.models.dia import Dia

class DiaRepository:
    @staticmethod
    def get_by_id(dia_id: int, db: Session) -> Optional[Dia]:
        """
        Obtiene un día por su ID.
        """
        return db.query(Dia).filter_by(id=dia_id).first()

    @staticmethod
    def get_by_nombre(nombre: str, db: Session) -> Optional[Dia]:
        """
        Obtiene un día por su nombre.
        Por ejemplo, 'Lunes', 'Martes', etc.
        """
        return db.query(Dia).filter_by(nombre=nombre).first()

    @staticmethod
    def get_all(db: Session) -> List[Dia]:
        """
        Obtiene todos los días registrados en la base de datos.
        """
        return db.query(Dia).all()

    @staticmethod
    def create(dia: Dia, db: Session) -> Dia:
        """
        Crea un nuevo registro de día en la base de datos.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(dia)
        db.flush()  # Sincroniza los cambios para asignar un ID si es necesario
        db.refresh(dia)
        return dia

    @staticmethod
    def update(dia: Dia, db: Session) -> Dia:
        """
        Actualiza un día existente en la base de datos.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db_dia = db.merge(dia)
        db.flush()
        db.refresh(db_dia)
        return db_dia

    @staticmethod
    def delete(dia_id: int, db: Session) -> bool:
        """
        Elimina un día de la base de datos, por su ID.
        Retorna True si se eliminó correctamente.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        dia = db.query(Dia).filter_by(id=dia_id).first()
        if dia:
            db.delete(dia)
            db.flush()
            return True
        return False

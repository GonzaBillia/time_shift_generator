from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.models.horario_sucursal import HorarioSucursal

class HorarioSucursalRepository:
    @staticmethod
    def get_by_id(horario_id: int, db: Session) -> Optional[HorarioSucursal]:
        """
        Obtiene un HorarioSucursal por su ID.
        Retorna None si no existe.
        """
        return db.query(HorarioSucursal).filter_by(id=horario_id).first()

    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Session) -> List[HorarioSucursal]:
        """
        Obtiene todos los HorarioSucursal asociados a una sucursal.
        """
        return db.query(HorarioSucursal).filter_by(sucursal_id=sucursal_id).all()

    @staticmethod
    def get_by_dia(dia_id: int, db: Session) -> List[HorarioSucursal]:
        """
        Obtiene todos los HorarioSucursal para un día específico.
        """
        return db.query(HorarioSucursal).filter_by(dia_id=dia_id).all()

    @staticmethod
    def create(horario: HorarioSucursal, db: Session) -> HorarioSucursal:
        """
        Crea un nuevo HorarioSucursal en la base de datos.
        Se asume que el manejo del commit se realizará externamente.
        """
        db.add(horario)
        db.flush()  # Sincroniza los cambios para asignar ID si es necesario
        db.refresh(horario)
        return horario

    @staticmethod
    def update(horario: HorarioSucursal, db: Session) -> Optional[HorarioSucursal]:
        """
        Actualiza un HorarioSucursal existente en la base de datos.
        Se asume que el manejo del commit se realizará externamente.
        """
        db_horario = db.merge(horario)
        db.flush()
        db.refresh(db_horario)
        return db_horario

    @staticmethod
    def delete(horario_id: int, db: Session) -> bool:
        """
        Elimina un HorarioSucursal de la base de datos por su ID.
        Retorna True si se elimina, False si no existe.
        Se asume que el manejo del commit se realizará externamente.
        """
        horario = db.query(HorarioSucursal).filter_by(id=horario_id).first()
        if horario:
            db.delete(horario)
            db.flush()
            return True
        return False

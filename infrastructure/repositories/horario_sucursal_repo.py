# archivo: infrastructure/repositories/horario_sucursal_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario_sucursal import HorarioSucursal

class HorarioSucursalRepository:
    @staticmethod
    def get_by_id(horario_id: int) -> Optional[HorarioSucursal]:
        """
        Obtiene un HorarioSucursal por su ID.
        Retorna None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        horario = session.query(HorarioSucursal).filter_by(id=horario_id).first()
        session.close()
        return horario

    @staticmethod
    def get_by_sucursal(sucursal_id: int) -> List[HorarioSucursal]:
        """
        Retorna todos los horarios de sucursal para la Sucursal con 'sucursal_id'.
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(HorarioSucursal).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return horarios

    @staticmethod
    def get_by_dia(dia_id: int) -> List[HorarioSucursal]:
        """
        Retorna todos los horarios de sucursal en un día específico (dia_id).
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(HorarioSucursal).filter_by(dia_id=dia_id).all()
        session.close()
        return horarios

    @staticmethod
    def create(horario: HorarioSucursal) -> HorarioSucursal:
        """
        Crea un nuevo horario de sucursal en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(horario)
        session.commit()
        session.refresh(horario)
        session.close()
        return horario

    @staticmethod
    def update(horario: HorarioSucursal) -> Optional[HorarioSucursal]:
        """
        Actualiza un HorarioSucursal existente.
        Retorna el objeto actualizado o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        existente = session.query(HorarioSucursal).filter_by(id=horario.id).first()
        if not existente:
            session.close()
            return None

        db_horario = session.merge(horario)
        session.commit()
        session.refresh(db_horario)
        session.close()
        return db_horario

    @staticmethod
    def delete(horario_id: int) -> bool:
        """
        Elimina un HorarioSucursal por su ID. Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        horario = session.query(HorarioSucursal).filter_by(id=horario_id).first()
        if horario:
            session.delete(horario)
            session.commit()
            session.close()
            return True
        session.close()
        return False

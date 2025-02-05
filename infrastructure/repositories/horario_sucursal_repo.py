from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario_sucursal import HorarioSucursal
from typing import List, Optional

class HorarioSucursalRepository:
    @staticmethod
    def get_by_id(horario_id: int) -> Optional[HorarioSucursal]:
        """Obtiene un horario de sucursal por su ID."""
        session: Session = Database.get_session("rrhh")
        horario = session.query(HorarioSucursal).filter_by(id=horario_id).first()
        session.close()
        return horario

    @staticmethod
    def get_by_sucursal(sucursal_id: int) -> List[HorarioSucursal]:
        """Obtiene todos los horarios de una sucursal específica."""
        session: Session = Database.get_session("rrhh")
        horarios = session.query(HorarioSucursal).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return horarios

    @staticmethod
    def get_by_dia(dia_id: int) -> List[HorarioSucursal]:
        """Obtiene todos los horarios de sucursales en un día específico."""
        session: Session = Database.get_session("rrhh")
        horarios = session.query(HorarioSucursal).filter_by(dia_id=dia_id).all()
        session.close()
        return horarios

    @staticmethod
    def create(horario: HorarioSucursal) -> HorarioSucursal:
        """Crea un nuevo horario para una sucursal."""
        session: Session = Database.get_session("rrhh")
        session.add(horario)
        session.commit()
        session.refresh(horario)
        session.close()
        return horario

    @staticmethod
    def update(horario: HorarioSucursal) -> HorarioSucursal:
        """Actualiza un horario existente en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.merge(horario)
        session.commit()
        session.refresh(horario)
        session.close()
        return horario

    @staticmethod
    def delete(horario_id: int) -> bool:
        """Elimina un horario de la base de datos."""
        session: Session = Database.get_session("rrhh")
        horario = session.query(HorarioSucursal).filter_by(id=horario_id).first()
        if horario:
            session.delete(horario)
            session.commit()
            session.close()
            return True
        session.close()
        return False

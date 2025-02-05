# archivo: infrastructure/repositories/horas_extra_colaborador_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horas_extra_colaborador import HorasExtraColaborador

class HorasExtraColaboradorRepository:
    @staticmethod
    def get_by_colaborador(colaborador_id: int) -> List[HorasExtraColaborador]:
        """
        Devuelve todas las horas extra pertenecientes a un colaborador específico.
        """
        session: Session = Database.get_session("rrhh")
        horas_extra = session.query(HorasExtraColaborador).filter_by(colaborador_id=colaborador_id).all()
        session.close()
        return horas_extra

    @staticmethod
    def get_by_tipo(colaborador_id: int, tipo: str) -> List[HorasExtraColaborador]:
        """
        Devuelve todas las horas extra de un colaborador, filtradas por tipo ('devolver' o 'cobrar').
        """
        session: Session = Database.get_session("rrhh")
        horas_extra = session.query(HorasExtraColaborador).filter_by(
            colaborador_id=colaborador_id, tipo=tipo
        ).all()
        session.close()
        return horas_extra

    @staticmethod
    def create(horas_extra: HorasExtraColaborador) -> HorasExtraColaborador:
        """
        Crea un nuevo registro de horas extra para un colaborador.
        """
        session: Session = Database.get_session("rrhh")
        session.add(horas_extra)
        session.commit()
        session.refresh(horas_extra)
        session.close()
        return horas_extra

    @staticmethod
    def delete(horas_extra_id: int) -> bool:
        """
        Elimina un registro de horas extra por su ID.
        Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        horas_extra = session.query(HorasExtraColaborador).filter_by(id=horas_extra_id).first()
        if horas_extra:
            session.delete(horas_extra)
            session.commit()
            session.close()
            return True
        session.close()
        return False

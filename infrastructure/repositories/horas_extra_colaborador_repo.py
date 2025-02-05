from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horas_extra_colaborador import HorasExtraColaborador
from typing import List, Optional

class HorasExtraColaboradorRepository:
    @staticmethod
    def get_by_colaborador(colaborador_id: int) -> List[HorasExtraColaborador]:
        """Obtiene todas las horas extra de un colaborador."""
        session: Session = Database.get_session("rrhh")
        horas_extra = session.query(HorasExtraColaborador).filter_by(colaborador_id=colaborador_id).all()
        session.close()
        return horas_extra

    @staticmethod
    def get_by_tipo(colaborador_id: int, tipo: str) -> List[HorasExtraColaborador]:
        """Obtiene todas las horas extra de un colaborador por tipo ('devolver' o 'cobrar')."""
        session: Session = Database.get_session("rrhh")
        horas_extra = session.query(HorasExtraColaborador).filter_by(
            colaborador_id=colaborador_id, tipo=tipo
        ).all()
        session.close()
        return horas_extra

    @staticmethod
    def create(horas_extra: HorasExtraColaborador) -> HorasExtraColaborador:
        """Registra una nueva entrada de horas extra para un colaborador."""
        session: Session = Database.get_session("rrhh")
        session.add(horas_extra)
        session.commit()
        session.refresh(horas_extra)
        session.close()
        return horas_extra

    @staticmethod
    def delete(horas_extra_id: int) -> bool:
        """Elimina una entrada de horas extra de la base de datos."""
        session: Session = Database.get_session("rrhh")
        horas_extra = session.query(HorasExtraColaborador).filter_by(id=horas_extra_id).first()
        if horas_extra:
            session.delete(horas_extra)
            session.commit()
            session.close()
            return True
        session.close()
        return False

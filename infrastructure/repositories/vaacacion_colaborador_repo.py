from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.vacacion_colaborador import VacacionColaborador
from typing import List, Optional
from datetime import date

class VacacionColaboradorRepository:
    @staticmethod
    def get_by_colaborador(colaborador_id: int) -> List[VacacionColaborador]:
        """Obtiene todas las vacaciones de un colaborador."""
        session: Session = Database.get_session("rrhh")
        vacaciones = session.query(VacacionColaborador).filter_by(colaborador_id=colaborador_id).all()
        session.close()
        return vacaciones

    @staticmethod
    def get_by_fecha(fecha: date) -> List[VacacionColaborador]:
        """Obtiene todas las vacaciones registradas en una fecha específica."""
        session: Session = Database.get_session("rrhh")
        vacaciones = session.query(VacacionColaborador).filter_by(fecha=fecha).all()
        session.close()
        return vacaciones

    @staticmethod
    def create(vacacion: VacacionColaborador) -> VacacionColaborador:
        """Registra una nueva vacación para un colaborador."""
        session: Session = Database.get_session("rrhh")
        session.add(vacacion)
        session.commit()
        session.refresh(vacacion)
        session.close()
        return vacacion

    @staticmethod
    def delete(vacacion_id: int) -> bool:
        """Elimina una vacación de la base de datos."""
        session: Session = Database.get_session("rrhh")
        vacacion = session.query(VacacionColaborador).filter_by(id=vacacion_id).first()
        if vacacion:
            session.delete(vacacion)
            session.commit()
            session.close()
            return True
        session.close()
        return False

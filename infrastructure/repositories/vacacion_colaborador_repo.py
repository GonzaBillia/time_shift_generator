# archivo: infrastructure/repositories/vacacion_colaborador_repo.py
from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.vacacion_colaborador import VacacionColaborador

class VacacionColaboradorRepository:
    @staticmethod
    def get_by_colaborador(colaborador_id: int) -> List[VacacionColaborador]:
        """
        Devuelve todas las vacaciones asociadas a un colaborador específico.
        """
        session: Session = Database.get_session("rrhh")
        vacaciones = session.query(VacacionColaborador).filter_by(colaborador_id=colaborador_id).all()
        session.close()
        return vacaciones

    @staticmethod
    def get_by_fecha(fecha: date) -> List[VacacionColaborador]:
        """
        Devuelve todas las vacaciones registradas para una fecha específica.
        """
        session: Session = Database.get_session("rrhh")
        vacaciones = session.query(VacacionColaborador).filter_by(fecha=fecha).all()
        session.close()
        return vacaciones

    @staticmethod
    def create(vacacion: VacacionColaborador) -> VacacionColaborador:
        """
        Crea un nuevo registro de vacación para un colaborador.
        """
        session: Session = Database.get_session("rrhh")
        session.add(vacacion)
        session.commit()
        session.refresh(vacacion)
        session.close()
        return vacacion

    @staticmethod
    def delete(vacacion_id: int) -> bool:
        """
        Elimina un registro de vacación por su ID. Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        vacacion = session.query(VacacionColaborador).filter_by(id=vacacion_id).first()
        if vacacion:
            session.delete(vacacion)
            session.commit()
            session.close()
            return True
        session.close()
        return False

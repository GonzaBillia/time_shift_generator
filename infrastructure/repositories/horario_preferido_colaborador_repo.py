from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario_preferido_colaborador import HorarioPreferidoColaborador

class HorarioPreferidoColaboradorRepository:
    @staticmethod
    def get_by_id(horario_id: int) -> Optional[HorarioPreferidoColaborador]:
        """
        Obtiene un HorarioPreferidoColaborador por su ID.
        Retorna None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        horario = session.query(HorarioPreferidoColaborador).filter_by(id=horario_id).first()
        session.close()
        return horario

    @staticmethod
    def get_by_colaborador(colaborador_id: int) -> List[HorarioPreferidoColaborador]:
        """
        Retorna todos los horarios preferidos asociados a un colaborador.
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(HorarioPreferidoColaborador).filter_by(colaborador_id=colaborador_id).all()
        session.close()
        return horarios

    @staticmethod
    def get_by_dia(dia_id: int) -> List[HorarioPreferidoColaborador]:
        """
        Retorna todos los horarios preferidos para un día específico.
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(HorarioPreferidoColaborador).filter_by(dia_id=dia_id).all()
        session.close()
        return horarios

    @staticmethod
    def create(horario: HorarioPreferidoColaborador) -> HorarioPreferidoColaborador:
        """
        Crea un nuevo HorarioPreferidoColaborador en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(horario)
        session.commit()
        session.refresh(horario)
        session.close()
        return horario

    @staticmethod
    def update(horario: HorarioPreferidoColaborador) -> Optional[HorarioPreferidoColaborador]:
        """
        Actualiza un HorarioPreferidoColaborador existente.
        Retorna el objeto actualizado o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        existente = session.query(HorarioPreferidoColaborador).filter_by(id=horario.id).first()
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
        Elimina un HorarioPreferidoColaborador por su ID.
        Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        horario = session.query(HorarioPreferidoColaborador).filter_by(id=horario_id).first()
        if horario:
            session.delete(horario)
            session.commit()
            session.close()
            return True
        session.close()
        return False

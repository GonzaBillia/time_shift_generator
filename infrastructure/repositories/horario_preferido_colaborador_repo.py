from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario_preferido_colaborador import HorarioPreferidoColaborador

class HorarioPreferidoColaboradorRepository:
    @staticmethod
    def get_by_id(horario_id: int, db: Optional[Session] = None) -> Optional[HorarioPreferidoColaborador]:
        """
        Obtiene un HorarioPreferidoColaborador por su ID.
        Retorna None si no existe.
        Si no se pasa una sesión, se crea y se cierra internamente.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horario = db.query(HorarioPreferidoColaborador).filter_by(id=horario_id).first()
            return horario
        finally:
            if close_session:
                db.close()

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
    def create(horario: HorarioPreferidoColaborador, db: Optional[Session] = None) -> HorarioPreferidoColaborador:
        """
        Crea un nuevo HorarioPreferidoColaborador en la base de datos.
        Si no se proporciona una sesión, se crea y se cierra internamente.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db.add(horario)
            if close_session:
                db.commit()
            else:
                db.flush()
            db.refresh(horario)
            return horario
        finally:
            if close_session:
                db.close()

    @staticmethod
    def update(horario: HorarioPreferidoColaborador, db: Optional[Session] = None) -> Optional[HorarioPreferidoColaborador]:
        """
        Actualiza un HorarioPreferidoColaborador existente.
        Retorna el objeto actualizado o None si no existe.
        Si se pasa una sesión externa, se asume que el commit se realizará fuera.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            existente = db.query(HorarioPreferidoColaborador).filter_by(id=horario.id).first()
            if not existente:
                return None
            db_horario = db.merge(horario)
            if close_session:
                db.commit()
            else:
                db.flush()
            db.refresh(db_horario)
            return db_horario
        finally:
            if close_session:
                db.close()

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

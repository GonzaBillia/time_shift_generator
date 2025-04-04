from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario_preferido_colaborador import HorarioPreferidoColaborador

class HorarioPreferidoColaboradorRepository:
    @staticmethod
    def get_by_id(horario_id: int, db: Session) -> Optional[HorarioPreferidoColaborador]:
        """
        Obtiene un HorarioPreferidoColaborador por su ID.
        Retorna None si no existe.
        """
        return db.query(HorarioPreferidoColaborador).filter_by(id=horario_id).first()

    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Session) -> List[HorarioPreferidoColaborador]:
        """
        Retorna todos los horarios preferidos asociados a un colaborador.
        """
        return db.query(HorarioPreferidoColaborador).filter_by(colaborador_id=colaborador_id).all()

    @staticmethod
    def get_by_dia(dia_id: int, db: Session) -> List[HorarioPreferidoColaborador]:
        """
        Retorna todos los horarios preferidos para un día específico.
        """
        return db.query(HorarioPreferidoColaborador).filter_by(dia_id=dia_id).all()

    @staticmethod
    def create(horario: HorarioPreferidoColaborador, db: Session) -> HorarioPreferidoColaborador:
        """
        Crea un nuevo HorarioPreferidoColaborador en la base de datos.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(horario)
        db.flush()  # Realiza un flush para asignar un ID, en caso de que sea necesario
        db.refresh(horario)
        return horario

    @staticmethod
    def update(horario: HorarioPreferidoColaborador, db: Session) -> Optional[HorarioPreferidoColaborador]:
        """
        Actualiza un HorarioPreferidoColaborador existente.
        Retorna el objeto actualizado o None si no existe.
        Se asume que el commit se realizará externamente.
        """
        existente = db.query(HorarioPreferidoColaborador).filter_by(id=horario.id).first()
        if not existente:
            return None
        db_horario = db.merge(horario)
        db.flush()
        db.refresh(db_horario)
        return db_horario

    @staticmethod
    def delete(horario_id: int, db: Session) -> bool:
        """
        Elimina un HorarioPreferidoColaborador por su ID.
        Retorna True si se elimina, o False si no existe.
        Se asume que el commit se realizará externamente.
        """
        existente = db.query(HorarioPreferidoColaborador).filter_by(id=horario_id).first()
        if not existente:
            return False
        db.delete(existente)
        db.flush()
        return True

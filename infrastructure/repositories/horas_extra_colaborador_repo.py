from typing import List
from sqlalchemy.orm import Session
from infrastructure.databases.models.horas_extra_colaborador import HorasExtraColaborador

class HorasExtraColaboradorRepository:
    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Session) -> List[HorasExtraColaborador]:
        """
        Devuelve todas las horas extra pertenecientes a un colaborador específico.
        """
        return db.query(HorasExtraColaborador).filter_by(colaborador_id=colaborador_id).all()

    @staticmethod
    def get_by_tipo(colaborador_id: int, tipo: str, db: Session) -> List[HorasExtraColaborador]:
        """
        Devuelve todas las horas extra de un colaborador, filtradas por tipo ('devolver' o 'cobrar').
        """
        return db.query(HorasExtraColaborador).filter_by(
            colaborador_id=colaborador_id, tipo=tipo
        ).all()

    @staticmethod
    def create(horas_extra: HorasExtraColaborador, db: Session) -> HorasExtraColaborador:
        """
        Crea un nuevo registro de horas extra para un colaborador.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(horas_extra)
        db.flush()  # Sincroniza los cambios para asignar un ID si es necesario
        db.refresh(horas_extra)
        return horas_extra

    @staticmethod
    def delete(horas_extra_id: int, db: Session) -> bool:
        """
        Elimina un registro de horas extra por su ID.
        Retorna True si se elimina, o False si no existe.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        horas_extra = db.query(HorasExtraColaborador).filter_by(id=horas_extra_id).first()
        if horas_extra:
            db.delete(horas_extra)
            db.flush()
            return True
        return False

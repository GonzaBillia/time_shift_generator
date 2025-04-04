from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session

from infrastructure.databases.models.vacacion_colaborador import VacacionColaborador

class VacacionColaboradorRepository:
    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Session) -> List[VacacionColaborador]:
        """
        Devuelve todas las vacaciones asociadas a un colaborador específico.
        """
        return db.query(VacacionColaborador).filter_by(colaborador_id=colaborador_id).all()

    @staticmethod
    def get_by_fecha(fecha: date, db: Session) -> List[VacacionColaborador]:
        """
        Devuelve todas las vacaciones registradas para una fecha específica.
        """
        return db.query(VacacionColaborador).filter_by(fecha=fecha).all()

    @staticmethod
    def create(vacacion: VacacionColaborador, db: Session) -> VacacionColaborador:
        """
        Crea un nuevo registro de vacación para un colaborador.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(vacacion)
        db.flush()  # Sincroniza los cambios para asignar un ID si es necesario
        db.refresh(vacacion)
        return vacacion

    @staticmethod
    def delete(vacacion_id: int, db: Session) -> bool:
        """
        Elimina un registro de vacación por su ID. Retorna True si se elimina, o False si no existe.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        vacacion = db.query(VacacionColaborador).filter_by(id=vacacion_id).first()
        if vacacion:
            db.delete(vacacion)
            db.flush()
            return True
        return False

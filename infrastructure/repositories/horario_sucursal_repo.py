from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario_sucursal import HorarioSucursal

class HorarioSucursalRepository:
    @staticmethod
    def get_by_id(horario_id: int, db: Optional[Session] = None) -> Optional[HorarioSucursal]:
        """
        Obtiene un HorarioSucursal por su ID. Retorna None si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horario = db.query(HorarioSucursal).filter_by(id=horario_id).first()
            return horario
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Optional[Session] = None) -> List[HorarioSucursal]:
        """
        Retorna todos los horarios de sucursal para la Sucursal con 'sucursal_id'.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horarios = db.query(HorarioSucursal).filter_by(sucursal_id=sucursal_id).all()
            return horarios
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_dia(dia_id: int, db: Optional[Session] = None) -> List[HorarioSucursal]:
        """
        Retorna todos los horarios de sucursal en un día específico (dia_id).
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horarios = db.query(HorarioSucursal).filter_by(dia_id=dia_id).all()
            return horarios
        finally:
            if close_session:
                db.close()

    @staticmethod
    def create(horario: HorarioSucursal, db: Optional[Session] = None) -> HorarioSucursal:
        """
        Crea un nuevo horario de sucursal en la base de datos.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db.add(horario)
            db.commit()
            db.refresh(horario)
            return horario
        finally:
            if close_session:
                db.close()

    @staticmethod
    def update(horario: HorarioSucursal, db: Optional[Session] = None) -> Optional[HorarioSucursal]:
        """
        Actualiza un HorarioSucursal existente. Retorna el objeto actualizado o None si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            existente = db.query(HorarioSucursal).filter_by(id=horario.id).first()
            if not existente:
                return None
            db_horario = db.merge(horario)
            db.commit()
            db.refresh(db_horario)
            return db_horario
        finally:
            if close_session:
                db.close()

    @staticmethod
    def delete(horario_id: int, db: Optional[Session] = None) -> bool:
        """
        Elimina un HorarioSucursal por su ID. Retorna True si se elimina, False si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horario = db.query(HorarioSucursal).filter_by(id=horario_id).first()
            if horario:
                db.delete(horario)
                db.commit()
                return True
            return False
        finally:
            if close_session:
                db.close()

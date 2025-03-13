from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario_sucursal import HorarioSucursal

class HorarioSucursalRepository:
    @staticmethod
    def get_by_id(horario_id: int, db: Optional[Session] = None) -> Optional[HorarioSucursal]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(HorarioSucursal).filter_by(id=horario_id).first()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Optional[Session] = None) -> List[HorarioSucursal]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(HorarioSucursal).filter_by(sucursal_id=sucursal_id).all()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_dia(dia_id: int, db: Optional[Session] = None) -> List[HorarioSucursal]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(HorarioSucursal).filter_by(dia_id=dia_id).all()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def create(horario: HorarioSucursal, db: Optional[Session] = None) -> HorarioSucursal:
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
    def update(horario: HorarioSucursal, db: Optional[Session] = None) -> Optional[HorarioSucursal]:
        """
        Actualiza un HorarioSucursal en la base de datos.
        Si se pasa una sesión externa, se asume que el manejo de la transacción (commit) se hace afuera.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
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
    def delete(horario_id: int, db: Optional[Session] = None) -> bool:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horario = db.query(HorarioSucursal).filter_by(id=horario_id).first()
            if horario:
                db.delete(horario)
                if close_session:
                    db.commit()
                else:
                    db.flush()
                return True
            return False
        finally:
            if close_session:
                db.close()

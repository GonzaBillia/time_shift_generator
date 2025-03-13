from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.sucursal import Sucursal

class SucursalRepository:
    @staticmethod
    def get_by_id(sucursal_id: int, db: Optional[Session] = None) -> Optional[Sucursal]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(Sucursal).filter_by(id=sucursal_id).first()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_all(db: Optional[Session] = None) -> List[Sucursal]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(Sucursal).all()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def create(sucursal: Sucursal, db: Optional[Session] = None) -> Sucursal:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db.add(sucursal)
            if close_session:
                db.commit()
            else:
                db.flush()
            db.refresh(sucursal)
            return sucursal
        finally:
            if close_session:
                db.close()

    @staticmethod
    def update(sucursal: Sucursal, db: Optional[Session] = None) -> Optional[Sucursal]:
        """
        Actualiza una sucursal en la base de datos.
        Si se pasa una sesión externa, se asume que el manejo de la transacción (commit) se hace afuera.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db_sucursal = db.merge(sucursal)
            if close_session:
                db.commit()
            else:
                db.flush()
            db.refresh(db_sucursal)
            return db_sucursal
        finally:
            if close_session:
                db.close()

    @staticmethod
    def delete(sucursal_id: int, db: Optional[Session] = None) -> bool:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            sucursal = db.query(Sucursal).filter_by(id=sucursal_id).first()
            if sucursal:
                db.delete(sucursal)
                if close_session:
                    db.commit()
                else:
                    db.flush()
                return True
            return False
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_nombre(nombre: str, db: Optional[Session] = None) -> Optional[Sucursal]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(Sucursal).filter_by(nombre=nombre).first()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_empresa(empresa_id: int, db: Optional[Session] = None) -> List[Sucursal]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(Sucursal).filter_by(empresa_id=empresa_id).all()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_horarios(sucursal_id: int, db: Optional[Session] = None) -> List:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            sucursal = db.query(Sucursal).filter_by(id=sucursal_id).first()
            return sucursal.horarios if sucursal else []
        finally:
            if close_session:
                db.close()

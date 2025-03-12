from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.sucursal import Sucursal

class SucursalRepository:
    @staticmethod
    def get_by_id(sucursal_id: int, db: Optional[Session] = None) -> Optional[Sucursal]:
        """
        Obtiene una Sucursal por su ID. Retorna None si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            sucursal = db.query(Sucursal).filter_by(id=sucursal_id).first()
            return sucursal
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_all(db: Optional[Session] = None) -> List[Sucursal]:
        """
        Devuelve la lista de todas las Sucursales.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            sucursales = db.query(Sucursal).all()
            return sucursales
        finally:
            if close_session:
                db.close()

    @staticmethod
    def create(sucursal: Sucursal, db: Optional[Session] = None) -> Sucursal:
        """
        Crea una nueva Sucursal en la base de datos.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db.add(sucursal)
            db.commit()
            db.refresh(sucursal)
            return sucursal
        finally:
            if close_session:
                db.close()

    @staticmethod
    def update(sucursal: Sucursal, db: Optional[Session] = None) -> Optional[Sucursal]:
        """
        Actualiza una Sucursal existente. Retorna la sucursal actualizada o None si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            existente = db.query(Sucursal).filter_by(id=sucursal.id).first()
            if not existente:
                return None
            db_sucursal = db.merge(sucursal)
            db.commit()
            db.refresh(db_sucursal)
            return db_sucursal
        finally:
            if close_session:
                db.close()

    @staticmethod
    def delete(sucursal_id: int, db: Optional[Session] = None) -> bool:
        """
        Elimina una Sucursal por su ID. Retorna True si se elimina, False si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            sucursal = db.query(Sucursal).filter_by(id=sucursal_id).first()
            if sucursal:
                db.delete(sucursal)
                db.commit()
                return True
            return False
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_nombre(nombre: str, db: Optional[Session] = None) -> Optional[Sucursal]:
        """
        Obtiene una Sucursal por su nombre. Retorna None si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            sucursal = db.query(Sucursal).filter_by(nombre=nombre).first()
            return sucursal
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_empresa(empresa_id: int, db: Optional[Session] = None) -> List[Sucursal]:
        """
        Devuelve todas las Sucursales asociadas a una Empresa específica.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            sucursales = db.query(Sucursal).filter_by(empresa_id=empresa_id).all()
            return sucursales
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_horarios(sucursal_id: int, db: Optional[Session] = None) -> List:
        """
        Devuelve la lista de objetos 'Horario' asignados a la Sucursal.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            sucursal = db.query(Sucursal).filter_by(id=sucursal_id).first()
            horarios = sucursal.horarios if sucursal else []
            return horarios
        finally:
            if close_session:
                db.close()

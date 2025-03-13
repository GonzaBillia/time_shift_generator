from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.espacio_disponible_sucursal import EspacioDisponibleSucursal

class EspacioDisponibleSucursalRepository:
    @staticmethod
    def get_by_id(espacio_id: int, db: Optional[Session] = None) -> Optional[EspacioDisponibleSucursal]:
        """
        Obtiene un registro de EspacioDisponibleSucursal por su ID.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(EspacioDisponibleSucursal).filter_by(id=espacio_id).first()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_all(db: Optional[Session] = None) -> List[EspacioDisponibleSucursal]:
        """
        Obtiene todos los registros de espacios disponibles en sucursales.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(EspacioDisponibleSucursal).all()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Optional[Session] = None) -> List[EspacioDisponibleSucursal]:
        """
        Obtiene la lista de espacios disponibles asociados a una sucursal específica.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(EspacioDisponibleSucursal).filter_by(sucursal_id=sucursal_id).all()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_rol(sucursal_id: int, rol_colaborador_id: int, db: Optional[Session] = None) -> Optional[EspacioDisponibleSucursal]:
        """
        Obtiene el espacio disponible en una sucursal para un rol específico.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            return db.query(EspacioDisponibleSucursal).filter_by(
                sucursal_id=sucursal_id,
                rol_colaborador_id=rol_colaborador_id
            ).first()
        finally:
            if close_session:
                db.close()

    @staticmethod
    def create(espacio: EspacioDisponibleSucursal, db: Optional[Session] = None) -> EspacioDisponibleSucursal:
        """
        Crea un nuevo registro de espacio disponible en una sucursal.
        Si se pasa una sesión externa, se asume que el manejo de la transacción (commit) se hace afuera.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db.add(espacio)
            if close_session:
                db.commit()
            else:
                db.flush()
            db.refresh(espacio)
            return espacio
        finally:
            if close_session:
                db.close()

    @staticmethod
    def update(espacio: EspacioDisponibleSucursal, db: Optional[Session] = None) -> EspacioDisponibleSucursal:
        """
        Actualiza un registro de espacio disponible en una sucursal.
        Si se pasa una sesión externa, se asume que el manejo de la transacción (commit) se hace afuera.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db_espacio = db.merge(espacio)
            if close_session:
                db.commit()
            else:
                db.flush()
            db.refresh(db_espacio)
            return db_espacio
        finally:
            if close_session:
                db.close()

    @staticmethod
    def delete(espacio_id: int, db: Optional[Session] = None) -> bool:
        """
        Elimina un registro de espacio disponible de la base de datos, por su ID.
        Devuelve True si se ha eliminado correctamente.
        Si se pasa una sesión externa, se asume que el manejo de la transacción (commit) se hace afuera.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            espacio = db.query(EspacioDisponibleSucursal).filter_by(id=espacio_id).first()
            if espacio:
                db.delete(espacio)
                if close_session:
                    db.commit()
                else:
                    db.flush()
                return True
            return False
        finally:
            if close_session:
                db.close()

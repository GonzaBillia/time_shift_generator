from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.tipo_colaborador import TipoEmpleado

class TipoEmpleadoRepository:
    @staticmethod
    def get_by_id(tipo_empleado_id: int, db: Optional[Session] = None) -> Optional[TipoEmpleado]:
        """
        Obtiene un TipoEmpleado por su ID. Retorna None si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            tipo_empleado = db.query(TipoEmpleado).filter_by(id=tipo_empleado_id).first()
            return tipo_empleado
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_all(db: Optional[Session] = None) -> List[TipoEmpleado]:
        """
        Devuelve la lista de todos los tipos de empleados en la base de datos.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            tipos_empleados = db.query(TipoEmpleado).all()
            return tipos_empleados
        finally:
            if close_session:
                db.close()

    @staticmethod
    def create(tipo_empleado: TipoEmpleado, db: Optional[Session] = None) -> TipoEmpleado:
        """
        Crea un nuevo TipoEmpleado en la base de datos.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db.add(tipo_empleado)
            db.commit()
            db.refresh(tipo_empleado)
            return tipo_empleado
        finally:
            if close_session:
                db.close()

    @staticmethod
    def update(tipo_empleado: TipoEmpleado, db: Optional[Session] = None) -> Optional[TipoEmpleado]:
        """
        Actualiza un TipoEmpleado existente. Retorna el objeto actualizado o None si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            existente = db.query(TipoEmpleado).filter_by(id=tipo_empleado.id).first()
            if not existente:
                return None
            db_tipo = db.merge(tipo_empleado)
            db.commit()
            db.refresh(db_tipo)
            return db_tipo
        finally:
            if close_session:
                db.close()

    @staticmethod
    def delete(tipo_empleado_id: int, db: Optional[Session] = None) -> bool:
        """
        Elimina un TipoEmpleado por su ID. Retorna True si se elimina, False si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            tipo_empleado = db.query(TipoEmpleado).filter_by(id=tipo_empleado_id).first()
            if tipo_empleado:
                db.delete(tipo_empleado)
                db.commit()
                return True
            return False
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_tipo(tipo: str, db: Optional[Session] = None) -> Optional[TipoEmpleado]:
        """
        Obtiene un TipoEmpleado por su campo 'tipo' (nombre), o None si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            tipo_empleado = db.query(TipoEmpleado).filter_by(tipo=tipo).first()
            return tipo_empleado
        finally:
            if close_session:
                db.close()

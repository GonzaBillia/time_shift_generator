# archivo: infrastructure/repositories/tipo_empleado_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.tipo_colaborador import TipoEmpleado

class TipoEmpleadoRepository:
    @staticmethod
    def get_by_id(tipo_empleado_id: int) -> Optional[TipoEmpleado]:
        """
        Obtiene un TipoEmpleado por su ID. Retorna None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        tipo_empleado = session.query(TipoEmpleado).filter_by(id=tipo_empleado_id).first()
        session.close()
        return tipo_empleado

    @staticmethod
    def get_all() -> List[TipoEmpleado]:
        """
        Devuelve la lista de todos los tipos de empleados en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        tipos_empleados = session.query(TipoEmpleado).all()
        session.close()
        return tipos_empleados

    @staticmethod
    def create(tipo_empleado: TipoEmpleado) -> TipoEmpleado:
        """
        Crea un nuevo TipoEmpleado en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(tipo_empleado)
        session.commit()
        session.refresh(tipo_empleado)
        session.close()
        return tipo_empleado

    @staticmethod
    def update(tipo_empleado: TipoEmpleado) -> Optional[TipoEmpleado]:
        """
        Actualiza un TipoEmpleado existente. Retorna el objeto actualizado o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        existente = session.query(TipoEmpleado).filter_by(id=tipo_empleado.id).first()
        if not existente:
            session.close()
            return None

        db_tipo = session.merge(tipo_empleado)
        session.commit()
        session.refresh(db_tipo)
        session.close()
        return db_tipo

    @staticmethod
    def delete(tipo_empleado_id: int) -> bool:
        """
        Elimina un TipoEmpleado por su ID. Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        tipo_empleado = session.query(TipoEmpleado).filter_by(id=tipo_empleado_id).first()
        if tipo_empleado:
            session.delete(tipo_empleado)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def get_by_tipo(tipo: str) -> Optional[TipoEmpleado]:
        """
        Obtiene un TipoEmpleado por su campo 'tipo' (nombre), o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        tipo_empleado = session.query(TipoEmpleado).filter_by(tipo=tipo).first()
        session.close()
        return tipo_empleado

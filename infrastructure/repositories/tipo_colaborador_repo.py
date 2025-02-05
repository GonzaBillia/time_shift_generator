from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.tipo_colaborador import TipoEmpleado
from typing import List, Optional

class TipoEmpleadoRepository:
    @staticmethod
    def get_by_id(tipo_empleado_id: int) -> Optional[TipoEmpleado]:
        """Obtiene un tipo de empleado por su ID."""
        session: Session = Database.get_session("rrhh")
        tipo_empleado = session.query(TipoEmpleado).filter_by(id=tipo_empleado_id).first()
        session.close()
        return tipo_empleado

    @staticmethod
    def get_all() -> List[TipoEmpleado]:
        """Obtiene todos los tipos de empleados registrados en la base de datos."""
        session: Session = Database.get_session("rrhh")
        tipos_empleados = session.query(TipoEmpleado).all()
        session.close()
        return tipos_empleados

    @staticmethod
    def create(tipo_empleado: TipoEmpleado) -> TipoEmpleado:
        """Crea un nuevo tipo de empleado en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.add(tipo_empleado)
        session.commit()
        session.refresh(tipo_empleado)
        session.close()
        return tipo_empleado

    @staticmethod
    def update(tipo_empleado: TipoEmpleado) -> TipoEmpleado:
        """Actualiza un tipo de empleado en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.merge(tipo_empleado)
        session.commit()
        session.refresh(tipo_empleado)
        session.close()
        return tipo_empleado

    @staticmethod
    def delete(tipo_empleado_id: int) -> bool:
        """Elimina un tipo de empleado de la base de datos."""
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
        """Obtiene un tipo de empleado por su nombre."""
        session: Session = Database.get_session("rrhh")
        tipo_empleado = session.query(TipoEmpleado).filter_by(tipo=tipo).first()
        session.close()
        return tipo_empleado

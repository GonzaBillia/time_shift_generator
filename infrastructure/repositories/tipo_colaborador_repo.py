from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.models.tipo_colaborador import TipoEmpleado

class TipoEmpleadoRepository:
    @staticmethod
    def get_by_id(tipo_empleado_id: int, db: Session) -> Optional[TipoEmpleado]:
        """
        Obtiene un TipoEmpleado por su ID. Retorna None si no existe.
        """
        return db.query(TipoEmpleado).filter_by(id=tipo_empleado_id).first()

    @staticmethod
    def get_all(db: Session) -> List[TipoEmpleado]:
        """
        Devuelve la lista de todos los tipos de empleados en la base de datos.
        """
        return db.query(TipoEmpleado).all()

    @staticmethod
    def create(tipo_empleado: TipoEmpleado, db: Session) -> TipoEmpleado:
        """
        Crea un nuevo TipoEmpleado en la base de datos.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(tipo_empleado)
        db.flush()  # Sincroniza los cambios para asignar un ID si es necesario
        db.refresh(tipo_empleado)
        return tipo_empleado

    @staticmethod
    def update(tipo_empleado: TipoEmpleado, db: Session) -> Optional[TipoEmpleado]:
        """
        Actualiza un TipoEmpleado existente. Retorna el objeto actualizado o None si no existe.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        existente = db.query(TipoEmpleado).filter_by(id=tipo_empleado.id).first()
        if not existente:
            return None
        db_tipo = db.merge(tipo_empleado)
        db.flush()
        db.refresh(db_tipo)
        return db_tipo

    @staticmethod
    def delete(tipo_empleado_id: int, db: Session) -> bool:
        """
        Elimina un TipoEmpleado por su ID. Retorna True si se elimina, o False si no existe.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        tipo_empleado = db.query(TipoEmpleado).filter_by(id=tipo_empleado_id).first()
        if tipo_empleado:
            db.delete(tipo_empleado)
            db.flush()
            return True
        return False

    @staticmethod
    def get_by_tipo(tipo: str, db: Session) -> Optional[TipoEmpleado]:
        """
        Obtiene un TipoEmpleado por su campo 'tipo' (nombre), o None si no existe.
        """
        return db.query(TipoEmpleado).filter_by(tipo=tipo).first()

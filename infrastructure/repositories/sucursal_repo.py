from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.models.sucursal import Sucursal

class SucursalRepository:
    @staticmethod
    def get_by_id(sucursal_id: int, db: Session) -> Optional[Sucursal]:
        """
        Obtiene una sucursal por su ID.
        """
        return db.query(Sucursal).filter_by(id=sucursal_id).first()

    @staticmethod
    def get_all(db: Session) -> List[Sucursal]:
        """
        Obtiene todas las sucursales.
        """
        return db.query(Sucursal).all()

    @staticmethod
    def create(sucursal: Sucursal, db: Session) -> Sucursal:
        """
        Crea una nueva sucursal en la base de datos.
        Se asume que el commit se realizará externamente.
        """
        db.add(sucursal)
        db.flush()  # Sin commit para sincronizar los cambios sin confirmar la transacción final
        db.refresh(sucursal)
        return sucursal

    @staticmethod
    def update(sucursal: Sucursal, db: Session) -> Optional[Sucursal]:
        """
        Actualiza una sucursal en la base de datos.
        Se asume que el manejo del commit se realizará externamente.
        """
        db_sucursal = db.merge(sucursal)
        db.flush()
        db.refresh(db_sucursal)
        return db_sucursal

    @staticmethod
    def delete(sucursal_id: int, db: Session) -> bool:
        """
        Elimina una sucursal de la base de datos por su ID.
        Retorna True si se elimina, False si no existe.
        Se asume que el manejo del commit se realizará externamente.
        """
        sucursal = db.query(Sucursal).filter_by(id=sucursal_id).first()
        if sucursal:
            db.delete(sucursal)
            db.flush()
            return True
        return False

    @staticmethod
    def get_by_nombre(nombre: str, db: Session) -> Optional[Sucursal]:
        """
        Obtiene una sucursal por su nombre.
        """
        return db.query(Sucursal).filter_by(nombre=nombre).first()

    @staticmethod
    def get_by_empresa(empresa_id: int, db: Session) -> List[Sucursal]:
        """
        Obtiene todas las sucursales de una empresa.
        """
        return db.query(Sucursal).filter_by(empresa_id=empresa_id).all()

    @staticmethod
    def get_horarios(sucursal_id: int, db: Session) -> List:
        """
        Obtiene los horarios asociados a una sucursal.
        """
        sucursal = db.query(Sucursal).filter_by(id=sucursal_id).first()
        return sucursal.horarios if sucursal else []

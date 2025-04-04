from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.models.espacio_disponible_sucursal import EspacioDisponibleSucursal

class EspacioDisponibleSucursalRepository:
    @staticmethod
    def get_by_id(espacio_id: int, db: Session) -> Optional[EspacioDisponibleSucursal]:
        """
        Obtiene un registro de EspacioDisponibleSucursal por su ID.
        """
        return db.query(EspacioDisponibleSucursal).filter_by(id=espacio_id).first()

    @staticmethod
    def get_all(db: Session) -> List[EspacioDisponibleSucursal]:
        """
        Obtiene todos los registros de espacios disponibles en sucursales.
        """
        return db.query(EspacioDisponibleSucursal).all()

    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Session) -> List[EspacioDisponibleSucursal]:
        """
        Obtiene la lista de espacios disponibles asociados a una sucursal específica.
        """
        return db.query(EspacioDisponibleSucursal).filter_by(sucursal_id=sucursal_id).all()

    @staticmethod
    def get_by_rol(sucursal_id: int, rol_colaborador_id: int, db: Session) -> Optional[EspacioDisponibleSucursal]:
        """
        Obtiene el espacio disponible en una sucursal para un rol específico.
        """
        return db.query(EspacioDisponibleSucursal).filter_by(
            sucursal_id=sucursal_id,
            rol_colaborador_id=rol_colaborador_id
        ).first()

    @staticmethod
    def create(espacio: EspacioDisponibleSucursal, db: Session) -> EspacioDisponibleSucursal:
        """
        Crea un nuevo registro de espacio disponible en una sucursal.
        Se asume que se pasa una sesión activa y que el manejo del commit se realizará externamente.
        """
        db.add(espacio)
        db.flush()  # Sincroniza los cambios para asignar un ID si es necesario
        db.refresh(espacio)
        return espacio

    @staticmethod
    def update(espacio: EspacioDisponibleSucursal, db: Session) -> EspacioDisponibleSucursal:
        """
        Actualiza un registro de espacio disponible en una sucursal.
        Se asume que se pasa una sesión activa y que el manejo del commit se realizará externamente.
        """
        db_espacio = db.merge(espacio)
        db.flush()
        db.refresh(db_espacio)
        return db_espacio

    @staticmethod
    def delete(espacio_id: int, db: Session) -> bool:
        """
        Elimina un registro de espacio disponible de la base de datos, por su ID.
        Devuelve True si se ha eliminado correctamente.
        Se asume que se pasa una sesión activa y que el manejo del commit se realizará externamente.
        """
        espacio = db.query(EspacioDisponibleSucursal).filter_by(id=espacio_id).first()
        if espacio:
            db.delete(espacio)
            db.flush()
            return True
        return False

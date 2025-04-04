from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.models.empresa import Empresa

class EmpresaRepository:
    @staticmethod
    def create(empresa: Empresa, db: Session) -> Empresa:
        """
        Crea una nueva Empresa en la base de datos.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(empresa)
        db.flush()  # Sincroniza los cambios para asignar un ID si es necesario
        db.refresh(empresa)
        return empresa

    @staticmethod
    def get_by_id(empresa_id: int, db: Session) -> Optional[Empresa]:
        """
        Obtiene una Empresa por su ID.
        """
        return db.query(Empresa).filter_by(id=empresa_id).first()

    @staticmethod
    def get_by_cuit(cuit: str, db: Session) -> Optional[Empresa]:
        """
        Obtiene una Empresa por su CUIT.
        """
        return db.query(Empresa).filter_by(cuit=cuit).first()

    @staticmethod
    def get_by_razon_social(razon_social: str, db: Session) -> Optional[Empresa]:
        """
        Obtiene una Empresa por su razón social.
        """
        return db.query(Empresa).filter_by(razon_social=razon_social).first()

    @staticmethod
    def get_all(db: Session) -> List[Empresa]:
        """
        Devuelve todas las Empresas.
        """
        return db.query(Empresa).all()

    @staticmethod
    def update(empresa: Empresa, db: Session) -> Empresa:
        """
        Actualiza una Empresa existente en la base de datos.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db_empresa = db.merge(empresa)
        db.flush()
        db.refresh(db_empresa)
        return db_empresa

    @staticmethod
    def delete(empresa_id: int, db: Session) -> bool:
        """
        Elimina una Empresa por su ID.
        Retorna True si se elimina correctamente o False en caso contrario.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        empresa = db.query(Empresa).filter_by(id=empresa_id).first()
        if empresa:
            db.delete(empresa)
            db.flush()
            return True
        return False

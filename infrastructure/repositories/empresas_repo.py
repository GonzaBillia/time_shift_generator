# archivo: empresa_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig
from infrastructure.databases.models.empresa import Empresa

class EmpresaRepository:
    @staticmethod
    def create(empresa: Empresa) -> Empresa:
        """
        Crea una nueva Empresa en la base de datos.
        """
        session: Session = DBConfig.get_session("rrhh")
        session.add(empresa)
        session.commit()
        session.refresh(empresa)
        session.close()
        return empresa

    @staticmethod
    def get_by_id(empresa_id: int) -> Optional[Empresa]:
        """
        Obtiene una Empresa por su ID.
        """
        session: Session = DBConfig.get_session("rrhh")
        empresa = session.query(Empresa).filter_by(id=empresa_id).first()
        session.close()
        return empresa

    @staticmethod
    def get_by_cuit(cuit: str) -> Optional[Empresa]:
        """
        Obtiene una Empresa por su CUIT.
        """
        session: Session = DBConfig.get_session("rrhh")
        empresa = session.query(Empresa).filter_by(cuit=cuit).first()
        session.close()
        return empresa

    @staticmethod
    def get_by_razon_social(razon_social: str) -> Optional[Empresa]:
        """
        Obtiene una Empresa por su razón social.
        """
        session: Session = DBConfig.get_session("rrhh")
        empresa = session.query(Empresa).filter_by(razon_social=razon_social).first()
        session.close()
        return empresa

    @staticmethod
    def get_all() -> List[Empresa]:
        """
        Devuelve todas las Empresas.
        """
        session: Session = DBConfig.get_session("rrhh")
        empresas = session.query(Empresa).all()
        session.close()
        return empresas

    @staticmethod
    def update(empresa: Empresa) -> Empresa:
        """
        Actualiza una Empresa existente en la base de datos.
        """
        session: Session = DBConfig.get_session("rrhh")
        db_empresa = session.merge(empresa)
        session.commit()
        session.refresh(db_empresa)
        session.close()
        return db_empresa

    @staticmethod
    def delete(empresa_id: int) -> bool:
        """
        Elimina una Empresa por su ID.
        Retorna True si se elimina correctamente.
        """
        session: Session = DBConfig.get_session("rrhh")
        empresa = session.query(Empresa).filter_by(id=empresa_id).first()
        if empresa:
            session.delete(empresa)
            session.commit()
            session.close()
            return True
        session.close()
        return False

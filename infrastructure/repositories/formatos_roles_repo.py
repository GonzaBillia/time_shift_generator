from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.formato_rol import FormatosRoles
from infrastructure.databases.models.rol import Rol

class FormatosRolesRepository:
    @staticmethod
    def get_by_ids(rol_colaborador_id: int, formato_id: int) -> Optional[FormatosRoles]:
        """
        Obtiene un registro de FormatosRoles por su clave compuesta.
        """
        session: Session = Database.get_session("rrhh")
        mapping = session.query(FormatosRoles).filter_by(
            rol_colaborador_id=rol_colaborador_id, 
            formato_id=formato_id
        ).first()
        session.close()
        return mapping
    
    @staticmethod
    def get_by_formatos(formato_id: int) -> List[FormatosRoles]:
        """
        Obtiene un registro de FormatosRoles por su clave compuesta.
        """
        session: Session = Database.get_session("rrhh")
        mapping = session.query(FormatosRoles).filter_by( 
            formato_id=formato_id
        )
        session.close()
        return mapping

    @staticmethod
    def get_all() -> List[FormatosRoles]:
        """
        Retorna la lista de todos los registros en FormatosRoles.
        """
        session: Session = Database.get_session("rrhh")
        mappings = session.query(FormatosRoles).all()
        session.close()
        return mappings
    
    @staticmethod
    def get_roles_by_formato(formato_id: int) -> List[Rol]:
        session: Session = Database.get_session("rrhh")
        roles = (
            session.query(Rol)
            .join(FormatosRoles)
            .options(joinedload(Rol.formatos))
            .filter(FormatosRoles.formato_id == formato_id)
            .all()
        )
        session.close()
        return roles

    @staticmethod
    def create(mapping: FormatosRoles) -> FormatosRoles:
        """
        Crea un nuevo registro en FormatosRoles.
        """
        session: Session = Database.get_session("rrhh")
        session.add(mapping)
        session.commit()
        session.refresh(mapping)
        session.close()
        return mapping

    @staticmethod
    def delete(rol_colaborador_id: int, formato_id: int) -> bool:
        """
        Elimina un registro de FormatosRoles por su clave compuesta.
        Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        mapping = session.query(FormatosRoles).filter_by(
            rol_colaborador_id=rol_colaborador_id, 
            formato_id=formato_id
        ).first()
        if mapping:
            session.delete(mapping)
            session.commit()
            session.close()
            return True
        session.close()
        return False

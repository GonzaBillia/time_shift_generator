from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from infrastructure.databases.models.formato_rol import FormatosRoles
from infrastructure.databases.models.rol import Rol

class FormatosRolesRepository:
    @staticmethod
    def get_by_ids(rol_colaborador_id: int, formato_id: int, db: Session) -> Optional[FormatosRoles]:
        """
        Obtiene un registro de FormatosRoles por su clave compuesta.
        """
        mapping = db.query(FormatosRoles).filter_by(
            rol_colaborador_id=rol_colaborador_id, 
            formato_id=formato_id
        ).first()
        return mapping
    
    @staticmethod
    def get_by_formatos(formato_id: int, db: Session) -> List[FormatosRoles]:
        """
        Obtiene todos los registros de FormatosRoles para un Formato dado.
        """
        mapping = db.query(FormatosRoles).filter_by(formato_id=formato_id).all()
        return mapping

    @staticmethod
    def get_all(db: Session) -> List[FormatosRoles]:
        """
        Retorna la lista de todos los registros en FormatosRoles.
        """
        mappings = db.query(FormatosRoles).all()
        return mappings
    
    @staticmethod
    def get_roles_by_formato(formato_id: int, db: Session) -> List[Rol]:
        roles = (
            db.query(Rol)
            .join(FormatosRoles)
            # Se quita el joinedload para evitar la recursión.
            # .options(joinedload(Rol.formatos))
            .filter(FormatosRoles.formato_id == formato_id)
            .all()
        )
        return roles

    @staticmethod
    def create(mapping: FormatosRoles, db: Session) -> FormatosRoles:
        """
        Crea un nuevo registro en FormatosRoles.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(mapping)
        db.flush()  # Sincroniza los cambios para asignar un ID si es necesario
        db.refresh(mapping)
        return mapping

    @staticmethod
    def delete(rol_colaborador_id: int, formato_id: int, db: Session) -> bool:
        """
        Elimina un registro de FormatosRoles por su clave compuesta.
        Retorna True si se elimina, False si no existe.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        mapping = db.query(FormatosRoles).filter_by(
            rol_colaborador_id=rol_colaborador_id, 
            formato_id=formato_id
        ).first()
        if mapping:
            db.delete(mapping)
            db.flush()
            return True
        return False

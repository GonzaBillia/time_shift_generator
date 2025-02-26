from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class FormatosRoles(Base):
    __tablename__ = "formatos_roles"

    rol_colaborador_id = Column(Integer, ForeignKey("roles_colaboradores.id"), primary_key=True)
    formato_id = Column(Integer, ForeignKey("formatos_sucursales.id"), primary_key=True)

    # Relación con Rol y Formato
    rol = relationship("Rol", back_populates="formatos")
    formato = relationship("Formato", back_populates="roles")

    def __repr__(self):
        return f"<FormatosRoles(rol_id={self.rol_id}, formato_id={self.formato_id})>"

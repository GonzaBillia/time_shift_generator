from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import DBConfig as Base

class Formato(Base):
    __tablename__ = "formatos_sucursales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)

    # Relación con `roles_colaboradores` a través de la tabla intermedia `formatos_roles`
    roles = relationship("Rol", secondary="formatos_roles", back_populates="formatos")

    # Relación con `sucursales` (Una formato puede aplicarse a varias sucursales)
    sucursales = relationship("Sucursal", back_populates="formato")

    def __repr__(self):
        return f"<Formato(id={self.id}, nombre={self.nombre})>"

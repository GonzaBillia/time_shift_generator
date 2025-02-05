from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Formato(Base):
    __tablename__ = "formatos_sucursales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)

    # Enfoque de asociación con Rol -> FormatosRoles
    roles = relationship(
        "FormatosRoles",
        back_populates="formato",
        cascade="all, delete-orphan"
    )

    # Relación con Sucursal
    sucursales = relationship("Sucursal", back_populates="formato")

    def __repr__(self):
        return f"<Formato(id={self.id}, nombre={self.nombre})>"

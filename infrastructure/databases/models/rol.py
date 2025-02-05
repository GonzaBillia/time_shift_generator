from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import DBConfig as Base

class Rol(Base):
    __tablename__ = "roles_colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    principal = Column(Boolean, nullable=False, default=False)

    # Relaciones con `formatos_roles` (Many-to-Many con Formatos)
    formatos = relationship("Formato", secondary="formatos_roles", back_populates="roles")

    def __repr__(self):
        return f"<Rol(id={self.id}, nombre={self.nombre}, principal={self.principal})>"

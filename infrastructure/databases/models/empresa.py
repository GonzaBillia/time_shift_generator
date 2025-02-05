# empresa.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    razon_social = Column(String(255), nullable=False)
    cuit = Column(String(15), nullable=False, unique=True)

    # Relación inversa con Sucursal
    sucursales = relationship("Sucursal", back_populates="empresa")

    # Si además tienes una relación con Colaborador:
    colaboradores = relationship("Colaborador", back_populates="empresa")

    def __repr__(self):
        return f"<Empresa(id={self.id}, razon_social={self.razon_social}, cuit={self.cuit})>"

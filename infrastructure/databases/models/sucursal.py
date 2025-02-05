from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import DBConfig as Base

class Sucursal(Base):
    __tablename__ = "sucursales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    direccion = Column(String, nullable=False)
    telefono = Column(String(20), nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    formato_id = Column(Integer, ForeignKey("formatos_sucursales.id"), nullable=False)

    # Relaciones
    empresa = relationship("Empresa", back_populates="sucursales")
    formato = relationship("Formato", back_populates="sucursales")
    horarios = relationship("Horario", back_populates="sucursal")

    def __repr__(self):
        return f"<Sucursal(id={self.id}, nombre={self.nombre}, empresa_id={self.empresa_id}, formato_id={self.formato_id})>"

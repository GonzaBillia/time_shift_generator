from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Dia(Base):
    __tablename__ = "dias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(15), nullable=False, unique=True)

    # Relaciones con otros modelos que referencian "dias.id"
    horarios = relationship("Horario", back_populates="dia")
    horarios_sucursal = relationship("HorarioSucursal", back_populates="dia")
    minimo_puestos = relationship("MinimoPuestosRequeridos", back_populates="dia")
    puestos_cubiertos = relationship("PuestosCubiertosPorHora", back_populates="dia")

    def __repr__(self):
        return f"<Dia(id={self.id}, nombre={self.nombre})>"

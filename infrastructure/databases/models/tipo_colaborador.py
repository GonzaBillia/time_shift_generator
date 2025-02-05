from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import DBConfig as Base

class TipoEmpleado(Base):
    __tablename__ = "tipo_empleado"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String(50), nullable=False, unique=True)
    horas_por_dia_max = Column(Integer, nullable=False)
    horas_semanales = Column(Integer, nullable=False)

    # Relación con `colaboradores` (Un tipo de empleado puede aplicarse a varios colaboradores)
    colaboradores = relationship("Colaborador", back_populates="tipo_empleado")

    def __repr__(self):
        return f"<TipoEmpleado(id={self.id}, tipo={self.tipo}, horas_por_dia_max={self.horas_por_dia_max}, horas_semanales={self.horas_semanales})>"

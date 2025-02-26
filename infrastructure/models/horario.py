from sqlalchemy import Column, Integer, Time, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Horario(Base):
    __tablename__ = "horarios_colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=True)  # puede ser None si es un horario general
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)
    dia_id = Column(Integer, ForeignKey("dias.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    horario_corrido = Column(Boolean, nullable=False, default=True)

    # Relaciones
    colaborador = relationship("Colaborador", back_populates="horarios")
    sucursal = relationship("Sucursal", back_populates="horarios")
    dia = relationship("Dia", back_populates="horarios")

    def __repr__(self):
        return (
            f"<Horario(id={self.id}, colaborador_id={self.colaborador_id}, "
            f"sucursal_id={self.sucursal_id}, fecha={self.fecha}, "
            f"dia_id={self.dia_id}, hora_inicio={self.hora_inicio}, "
            f"hora_fin={self.hora_fin}, horario_corrido={self.horario_corrido})>"
        )

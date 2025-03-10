from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class HorarioPreferidoColaborador(Base):
    __tablename__ = "horarios_preferidos_colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=False)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)  # Nueva FK a sucursales
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    dia_id = Column(Integer, ForeignKey("dias.id"), nullable=False)
    horario_corrido = Column(Boolean, default=False, nullable=False)

    # Relaciones
    colaborador = relationship("Colaborador", back_populates="horarios_preferidos_colaboradores")
    sucursal = relationship("Sucursal", back_populates="horarios_preferidos_colaboradores")  # Relación con sucursal
    dia = relationship("Dia", back_populates="horarios_preferidos_colaboradores")

    def __repr__(self):
        return (
            f"<HorarioPreferidoColaborador(id={self.id}, colaborador_id={self.colaborador_id}, "
            f"sucursal_id={self.sucursal_id}, fecha_inicio={self.hora_inicio}, fecha_fin={self.hora_fin}, "
            f"dia_id={self.dia_id}, horario_corrido={self.horario_corrido})>"
        )

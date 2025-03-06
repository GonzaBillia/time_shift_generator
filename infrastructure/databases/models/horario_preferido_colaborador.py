from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class HorarioPreferidoColaborador(Base):
    __tablename__ = "horarios_preferidos_colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=False)
    fecha_inicio = Column(Time, nullable=False)
    fecha_fin = Column(Time, nullable=False)
    dia_id = Column(Integer, ForeignKey("dias.id"), nullable=False)
    horario_corrido = Column(Boolean, default=False, nullable=False)

    # Relaciones
    colaborador = relationship("Colaborador", back_populates="horarios_preferidos_colaboradores")
    dia = relationship("Dia", back_populates="horarios_preferidos_colaboradores")

    def __repr__(self):
        return (
            f"<HorarioPreferidoColaborador(id={self.id}, colaborador_id={self.colaborador_id}, "
            f"fecha_inicio={self.fecha_inicio}, fecha_fin={self.fecha_fin}, "
            f"dia_id={self.dia_id}, horario_corrido={self.horario_corrido})>"
        )

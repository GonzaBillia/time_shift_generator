from sqlalchemy import Column, Integer, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Horario(Base):
    __tablename__ = "horarios_colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    puesto_id = Column(Integer, ForeignKey("puestos.id"), nullable=False)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    horario_corrido = Column(Boolean, nullable=False, default=True)

    # Relaciones
    puesto = relationship("Puesto", back_populates="horarios")

    def __repr__(self):
        return (
            f"<Horario(id={self.id}, puesto_id={self.puesto_id}, "
            f"hora_inicio={self.hora_inicio}, hora_fin={self.hora_fin}, "
            f"horario_corrido={self.horario_corrido})>"
        )

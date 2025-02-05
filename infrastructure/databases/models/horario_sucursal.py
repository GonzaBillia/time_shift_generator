from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class HorarioSucursal(Base):
    __tablename__ = "horarios_sucursales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)
    dia_id = Column(Integer, ForeignKey("dias.id"), nullable=False)
    hora_apertura = Column(Time, nullable=False)
    hora_cierre = Column(Time, nullable=False)

    # Relaciones
    sucursal = relationship("Sucursal", back_populates="horarios_sucursal")
    dia = relationship("Dia", back_populates="horarios_sucursal")

    def __repr__(self):
        return (
            f"<HorarioSucursal(id={self.id}, sucursal_id={self.sucursal_id}, "
            f"dia_id={self.dia_id}, hora_apertura={self.hora_apertura}, "
            f"hora_cierre={self.hora_cierre})>"
        )

from sqlalchemy import Column, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class HorasExtraColaborador(Base):
    __tablename__ = "horas_extra"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=False)
    tipo = Column(Enum("devolver", "cobrar", name="tipo_horas_extra"), nullable=False)
    cantidad = Column(Integer, nullable=False)

    # Relaciones
    colaborador = relationship("Colaborador", back_populates="horas_extra")

    def __repr__(self):
        return f"<HorasExtraColaborador(id={self.id}, colaborador_id={self.colaborador_id}, tipo={self.tipo}, cantidad={self.cantidad})>"

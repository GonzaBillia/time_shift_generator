from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import DBConfig as Base

class VacacionColaborador(Base):
    __tablename__ = "vacaciones_colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=False)
    fecha = Column(Date, nullable=False)

    # Relaciones
    colaborador = relationship("Colaborador", back_populates="vacaciones")

    def __repr__(self):
        return f"<VacacionColaborador(id={self.id}, colaborador_id={self.colaborador_id}, fecha={self.fecha})>"

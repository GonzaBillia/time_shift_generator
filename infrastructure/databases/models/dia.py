from sqlalchemy import Column, Integer, String
from infrastructure.databases.config.database import DBConfig as Base

class Dia(Base):
    __tablename__ = "dias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(15), nullable=False, unique=True)

    def __repr__(self):
        return f"<Dia(id={self.id}, nombre={self.nombre})>"

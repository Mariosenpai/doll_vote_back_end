from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base

from db import get_base

Base = get_base()

class Jurados(Base):
    __tablename__ = "jurados"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    senha = Column(String)

    # Relacionamento com Pontuacao
    pontuacao = relationship("Pontuacao", back_populates="jurado")
from sqlalchemy import Column, Integer, String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

from db import get_base

Base = get_base()

class Pontuacao(Base):
    __tablename__ = "pontuacao"

    __table_args__ = (
        UniqueConstraint(
            "id_candidato",
            "id_jurado",
            name="uq_candidato_jurado"
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    id_candidato = Column(
        Integer,
        ForeignKey("candidatos.id"),
        nullable=False
    )

    id_jurado = Column(
        Integer,
        ForeignKey("jurados.id"),
        nullable=False
    )

    criatividade_originalidade = Column(Integer)
    identidade_cultural = Column(Integer)
    acabamento = Column(Integer)
    inovacao_design = Column(Integer)
    harmonia_apresentacao = Column(Integer)

    # Relacionamentos
    candidato = relationship("Candidato", back_populates="pontuacao")
    jurado = relationship("Jurados", back_populates="pontuacao")

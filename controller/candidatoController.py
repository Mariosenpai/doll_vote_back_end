from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session

from ModelResponse import CandidatoCreate
from classes.Candidato import Candidato
from classes.Pontuacao import Pontuacao
from db import get_db

router = APIRouter(
    prefix="/candidatos",
    tags=["Candidatos"]
)

@router.post("/candidatos/add")
def create_candidatos(user: CandidatoCreate, db: Session = Depends(get_db)):
    db_candidato = Candidato(nome=user.nome)
    db.add(db_candidato)
    db.commit()
    db.refresh(db_candidato)
    return db_candidato

@router.get("/candidatos/all")
def get_all_candidatos(db: Session = Depends(get_db)):
    users = db.query(Candidato).all()
    return users

@router.delete("/candidatos/{id_candidato}")
def delete_candidato(id_candidato: int, db: Session = Depends(get_db)):
    candidato = db.query(Candidato).filter(
        Candidato.id == id_candidato
    ).first()

    if candidato is None:
        raise HTTPException(
            status_code=404,
            detail="Candidato não encontrado."
        )

    db.query(Pontuacao).filter(Pontuacao.id_candidato == candidato.id).delete()

    db.delete(candidato)
    db.commit()

    return {"message": "Candidato removido com sucesso."}
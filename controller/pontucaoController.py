from typing import List

from sqlalchemy.orm import Session

from ModelResponse import PontuacaoCreate
from classes.Candidato import Candidato
from classes.Jurados import Jurados
from classes.Pontuacao import Pontuacao
from db import get_db

from fastapi import APIRouter, Depends

from dependencies import verificar_token

router = APIRouter(
    prefix="/pontuacao",
    tags=["pontuacao"]
)


@router.post("/pontuacao/add")
def add_pontuacao(
    dados: PontuacaoCreate,
    jurado_att: Jurados = Depends(verificar_token),
    db: Session = Depends(get_db)
):
    # jurado = verificar_token(token=jurado_att)
    pontuacao_existente = db.query(Pontuacao).filter(
        Pontuacao.id_candidato == dados.id_candidato,
        Pontuacao.id_jurado == jurado_att.id
    ).first()

    if pontuacao_existente:
        raise HTTPException(
            status_code=400,
            detail="Este jurado já avaliou este candidato."
        )

    candidato = db.query(Candidato).filter(
        Candidato.id == dados.id_candidato
    ).first()

    if candidato is None:
        raise HTTPException(
            status_code=404,
            detail="Candidato não encontrado."
        )

    pontuacao = Pontuacao(
        id_candidato=dados.id_candidato,
        id_jurado=jurado_att.id,
        criatividade_originalidade=dados.criatividade_originalidade,
        identidade_cultural=dados.identidade_cultural,
        acabamento=dados.acabamento,
        inovacao_design=dados.inovacao_design,
        harmonia_apresentacao=dados.harmonia_apresentacao
    )

    db.add(pontuacao)
    db.commit()
    db.refresh(pontuacao)

    return pontuacao

from fastapi import HTTPException, Depends, APIRouter


@router.get("/pontuacao/candidato/{id_candidato}")
def get_pontuacao_candidato(
    id_candidato: int,
    db: Session = Depends(get_db)
):

    candidato = db.query(Candidato).filter(
        Candidato.id == id_candidato
    ).first()

    if candidato is None:
        raise HTTPException(
            status_code=404,
            detail="Candidato não encontrado."
        )

    pontuacoes = db.query(Pontuacao).filter(
        Pontuacao.id_candidato == id_candidato
    ).all()

    return {
        "id": candidato.id,
        "nome": candidato.nome,
        "pontuacoes": pontuacoes
    }


def soma_pontuacao(
    pontuacoes: List[Pontuacao]
):
    pontuacoes_soma_total = 0
    for pontuacao in pontuacoes:
        pontuacoes_soma_total += pontuacao.criatividade_originalidade
        pontuacoes_soma_total += pontuacao.acabamento
        pontuacoes_soma_total += pontuacao.inovacao_design
        pontuacoes_soma_total += pontuacao.identidade_cultural
        pontuacoes_soma_total += pontuacao.harmonia_apresentacao

    return pontuacoes_soma_total

@router.get("/pontuacao/all")
def get_all_pontuacoes(db: Session = Depends(get_db)):
    candidatos = db.query(Candidato).all()
    list_dic = []
    for candidato in candidatos:
        dic = {
            "nome": candidato.nome,
            "total_pontuacoes": soma_pontuacao(candidato.pontuacao)
        }
        list_dic.append(dic)

    return list_dic
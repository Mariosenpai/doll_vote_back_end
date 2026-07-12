from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ModelResponse import JuradoCreate, LoginRequest
from classes.Candidato import Candidato
from classes.Jurados import Jurados
from classes.Pontuacao import Pontuacao
from db import get_db
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from datetime import datetime, timedelta

from dependencies import verificar_token

SECRET_KEY = "uma-chave-bem-grande-e-secreta"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 200

from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

router = APIRouter(
    prefix="/jurados",
    tags=["jurados"]
)


@router.get("/jurados/candidatos_votados")
def all_candidatos_jurados_votados(jurado_att: Jurados = Depends(verificar_token),db: Session = Depends(get_db)):
    candidatos = db.query(Candidato).all()
    lista_all_candidatos_votados = []

    for candidato in candidatos:
        pontuacao_existente = db.query(Pontuacao).filter(
            Pontuacao.id_candidato == candidato.id,
            Pontuacao.id_jurado == jurado_att.id
        ).first()

        if pontuacao_existente:
            votado = True
        else:
            votado = False

        lista_all_candidatos_votados.append(
            {
                "nome": candidato.nome,
                "id": candidato.id,
                "votado": votado
            }
        )

    return lista_all_candidatos_votados


@router.get("/all")
def all_jurados(db: Session = Depends(get_db)):
    return db.query(Jurados).all()

@router.delete("/jurados/{id_jurado}/senha/{senha_delete}",)
def deletar_jurado(id_jurado, senha_delete: str ,db: Session = Depends(get_db)):

    if senha_delete == "1324":
        jurado = db.query(Jurados).filter(
            Jurados.id == id_jurado
        ).first()

        db.query(Pontuacao).filter(Pontuacao.id_jurado == jurado.id).delete()

        db.delete(jurado)
        db.commit()

        return {"message": "Jurado removido com sucesso."}

@router.get("/jurados/qnt_votos_jurados")
def qnt_faltam_o_jurados_votaram(db: Session = Depends(get_db)):

    todos_jurados = db.query(Jurados).all()
    total_candidatos = len(db.query(Candidato).all())

    qnt_votos_jurados = []
    for jurado in todos_jurados:
        # todos os votos de um jurado
        votos = db.query(Pontuacao).filter(
            Pontuacao.id_jurado == jurado.id
        ).all()
        dic = {
            f"{jurado.nome}": len(votos),
            f"total_participante": total_candidatos,

        }
        qnt_votos_jurados.append(dic)

    return qnt_votos_jurados


@router.post("/jurados/add")
def create_jurado(jurado: JuradoCreate, db: Session = Depends(get_db)):

    senha_hash = pwd_context.hash(jurado.senha)

    db_jurado = Jurados(
        nome=jurado.nome,
        senha=senha_hash
    )

    db.add(db_jurado)
    db.commit()
    db.refresh(db_jurado)

    return db_jurado

def criar_token(id_jurado):

    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    dados = {
        "sub": str(id_jurado),
        "exp": expire
    }

    return jwt.encode(
        dados,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

@router.post("/login")
def login(
    dados: LoginRequest,
    db: Session = Depends(get_db)
):

    jurado = db.query(Jurados).filter(
        Jurados.nome == dados.nome
    ).first()

    if jurado is None:
        raise HTTPException(
            status_code=401,
            detail="Nome ou senha inválidos."
        )

    if not pwd_context.verify(dados.senha, jurado.senha):
        raise HTTPException(
            status_code=401,
            detail="Nome ou senha inválidos."
        )

    token = criar_token(jurado.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ModelResponse import JuradoCreate, LoginRequest
from classes.Jurados import Jurados
from db import get_db
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer

from jose import jwt
from datetime import datetime, timedelta

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

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from classes.Jurados import Jurados
from db import get_db

from jose import jwt, JWTError
SECRET_KEY = "uma-chave-bem-grande-e-secreta"
ALGORITHM = "HS256"

def verificar_token(token, session: Session = Depends(get_db)) -> Jurados:
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_jurados = dic_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado")
    jurado = session.query(Jurados).filter(Jurados.id == id_jurados).first()
    return jurado
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, UniqueConstraint


from controller.candidatoController import router as candidatos_router
from controller.juradoController import router as jurados_router
from controller.pontucaoController import router as pontuacao_router
from db import get_db, get_base

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = get_base()
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(candidatos_router)
app.include_router(jurados_router)
app.include_router(pontuacao_router)

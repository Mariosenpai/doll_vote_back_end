from pydantic import BaseModel

class CandidatoCreate(BaseModel):
    nome: str

class JuradoCreate(BaseModel):
    nome: str
    senha: str

class LoginRequest(BaseModel):
    nome: str
    senha: str

class PontuacaoCreate(BaseModel):
    id_candidato: int
    criatividade_originalidade: int
    identidade_cultural: int
    acabamento: int
    inovacao_design: int
    harmonia_apresentacao: int
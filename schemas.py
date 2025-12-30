# schemas.py
from pydantic import BaseModel

class PerguntaIn(BaseModel):
    pergunta: str

class RespostaOut(BaseModel):
    resposta: str

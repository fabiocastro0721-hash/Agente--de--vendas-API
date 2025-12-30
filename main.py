# main.py
from fastapi import FastAPI, Depends, HTTPException
from logging_config import get_logger

from schemas import PerguntaIn, RespostaOut
from security import verificar_api_key
from agent import agente
from database import criar_banco, inserir_dados_teste

app = FastAPI(title="Agente de Vendas API")
logger = get_logger("api")


@app.on_event("startup")
def startup_event():
    criar_banco()
    inserir_dados_teste()

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.post("/pergunta", response_model=RespostaOut)
def perguntar(
    payload: PerguntaIn,
    _: None = Depends(verificar_api_key)
):
    logger.info("Rota /pergunta chamada")

    try:
        resposta = agente(payload.pergunta)
        logger.info("Rota /pergunta finalizada com sucesso")
        return {"resposta": resposta}

    except Exception as e:
        logger.exception("Erro na rota /pergunta")
        raise HTTPException(status_code=500, detail="Erro interno")


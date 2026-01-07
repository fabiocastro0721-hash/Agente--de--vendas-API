from fastapi import FastAPI, Depends, HTTPException
from logging_config import get_logger
from schemas import PerguntaIn, RespostaOut
from security import verificar_api_key
from agent import agente
from database import criar_banco
from import_google_sheets import importar_google_sheets

app = FastAPI(title="Agente de Vendas API")
logger = get_logger("api")


@app.on_event("startup")
def startup_event():
    criar_banco()
    logger.info("Banco verificado/criado com sucesso")


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.post("/sync")
def sync_google_sheets(_: None = Depends(verificar_api_key)):
    logger.info("Iniciando sincronização com Google Sheets")

    try:
        importar_google_sheets()
        return {
            "status": "ok",
            "message": "Google Sheets sincronizado com sucesso"
        }
    except Exception:
        logger.exception("Erro ao sincronizar Google Sheets")
        raise HTTPException(status_code=500, detail="Erro ao sincronizar")


@app.post("/pergunta", response_model=RespostaOut)
def perguntar(payload: PerguntaIn, _: None = Depends(verificar_api_key)):
    resposta = agente(payload.pergunta)
    return {"resposta": resposta}

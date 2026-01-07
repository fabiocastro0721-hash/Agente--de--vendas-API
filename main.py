from fastapi import FastAPI, Depends, HTTPException
from logging_config import get_logger
from schemas import PerguntaIn, RespostaOut
from security import verificar_api_key
from agent import agente
from database import criar_banco
from import_google_sheets import importar_google_sheets

app = FastAPI(
    title="Agente de Vendas API",
    version="1.0.0",
    servers=[
        {
            "url": "https://agente-de-vendas-api.onrender.com",
            "description": "Produção (Render)"
        }
    ]
)

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
        logger.info("Sincronização concluída com sucesso")
        return {
            "status": "ok",
            "message": "Google Sheets sincronizado com sucesso"
        }
    except Exception as e:
        logger.exception("Erro ao sincronizar Google Sheets")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@app.post("/pergunta", response_model=RespostaOut)
def perguntar(
    payload: PerguntaIn,
    _: None = Depends(verificar_api_key)
):
    logger.info("Rota /pergunta chamada")

    try:
        resposta = agente(payload.pergunta)
        return {"resposta": resposta}

    except Exception as e:
        logger.exception("Erro na rota /pergunta")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

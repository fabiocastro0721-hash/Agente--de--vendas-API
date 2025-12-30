# security.py
from fastapi import Header, HTTPException
from config import API_KEY_INTERNA
from rate_limiter import rate_limit

def verificar_api_key(x_api_key: str = Header(None)):
    if not API_KEY_INTERNA:
        raise HTTPException(status_code=500, detail="API_KEY_INTERNA não configurada")

    if x_api_key != API_KEY_INTERNA:
        raise HTTPException(status_code=403, detail="API Key inválida")

    # ⛔ RATE LIMIT AQUI
    rate_limit(x_api_key)

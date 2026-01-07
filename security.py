# security.py
from fastapi import Header, HTTPException
from config import API_KEY_INTERNA
from rate_limiter import rate_limit


def verificar_api_key(authorization: str = Header(None)):
    if not API_KEY_INTERNA:
        raise HTTPException(
            status_code=500,
            detail="API_KEY_INTERNA não configurada"
        )

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=403,
            detail="Token de autenticação ausente"
        )

    token = authorization.replace("Bearer ", "").strip()

    if token != API_KEY_INTERNA:
        raise HTTPException(
            status_code=403,
            detail="API Key inválida"
        )

    # opcional: rate limit
    rate_limit(token)

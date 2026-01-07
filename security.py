from fastapi import Header, HTTPException
from config import API_KEY_INTERNA
from rate_limiter import rate_limit


def verificar_api_key(authorization: str = Header(None)):
    if not API_KEY_INTERNA:
        raise HTTPException(
            status_code=500,
            detail="API_KEY_INTERNA não configurada"
        )

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Header Authorization ausente"
        )

    try:
        scheme, token = authorization.split()
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Formato inválido do Authorization"
        )

    if scheme.lower() != "bearer" or token != API_KEY_INTERNA:
        raise HTTPException(
            status_code=403,
            detail="API Key inválida"
        )

    rate_limit(token)

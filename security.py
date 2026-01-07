from fastapi import Header, HTTPException
from config import API_KEY_INTERNA
from rate_limiter import rate_limit


def verificar_api_key(x_api_key: str | None = Header(default=None)):
    # 1️⃣ Verifica se a variável de ambiente existe
    if not API_KEY_INTERNA:
        raise HTTPException(
            status_code=500,
            detail="API_KEY_INTERNA não configurada"
        )

    # 2️⃣ Verifica se o header foi enviado
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Header x-api-key não informado"
        )

    # 3️⃣ Compara a chave enviada com a chave interna
    if x_api_key != API_KEY_INTERNA:
        raise HTTPException(
            status_code=403,
            detail="API Key inválida"
        )

    # 4️⃣ Rate limit (opcional, mas recomendado)
    rate_limit(x_api_key)

    # Se passou por tudo, está autorizado
    return True

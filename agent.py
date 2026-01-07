# agent.py
from config import OPENAI_API_KEY
from fastapi import HTTPException
from database import buscar_vendas_por_texto

# Se quiser usar OpenAI futuramente:
# from openai import OpenAI
# client = OpenAI(api_key=OPENAI_API_KEY)


def agente(pergunta: str) -> str:
    """
    Processa perguntas relacionadas à planilha.
    """

    pergunta_lower = pergunta.lower()

    # 👉 EXEMPLO: pergunta sobre nota cancelada
    if "cancelad" in pergunta_lower:
        resultados = buscar_vendas_por_texto("cancel")

        if not resultados:
            return "Não encontrei nenhuma nota fiscal cancelada na planilha."

        return (
            f"Encontrei {len(resultados)} nota(s) fiscal(is) cancelada(s) "
            "na planilha."
        )

    # 👉 Se quiser usar OpenAI (opcional)
    if "resuma" in pergunta_lower or "explique" in pergunta_lower:
        if not OPENAI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="OPENAI_API_KEY não configurada"
            )

        # Aqui você chamaria OpenAI futuramente
        return "Função de IA ainda não implementada."

    # fallback
    return "Não consegui entender a pergunta com base nos dados da planilha."

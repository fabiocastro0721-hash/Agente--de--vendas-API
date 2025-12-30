from openai import OpenAI
from config import OPENAI_API_KEY
from database import buscar_vendas
from logging_config import get_logger

logger = get_logger("agent")

client = OpenAI(api_key=OPENAI_API_KEY)

def agente(pergunta_cliente: str) -> str:
    logger.info(f"Pergunta recebida: {pergunta_cliente}")

    dados = buscar_vendas()

    prompt = f"""
Você é um agente de atendimento da empresa.
Use APENAS os dados abaixo para responder.

Dados:
{dados}

Pergunta:
{pergunta_cliente}
""".strip()

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    resposta = response.output[0].content[0].text
    logger.info("Resposta gerada com sucesso")

    return resposta

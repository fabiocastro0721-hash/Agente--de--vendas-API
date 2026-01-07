from openai import OpenAI
from config import OPENAI_API_KEY
from database import buscar_vendas_por_texto
from logging_config import get_logger

logger = get_logger("agent")

def agente(pergunta_cliente: str) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY não configurada no ambiente")

    client = OpenAI(api_key=OPENAI_API_KEY)

    dados = buscar_vendas_por_texto(pergunta_cliente)
    if not dados:
        dados = "Nenhum dado relevante encontrado."

    prompt = f"""
Você é um agente de atendimento.
Use apenas os dados abaixo.

DADOS:
{dados}

PERGUNTA:
{pergunta_cliente}
""".strip()

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    return response.output[0].content[0].text

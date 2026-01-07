from openai import OpenAI
from .config import OPENAI_API_KEY
from .database import buscar_vendas_por_texto
from .logging_config import get_logger

logger = get_logger("agent")

client = OpenAI(api_key=OPENAI_API_KEY)


def agente(pergunta_cliente: str) -> str:
    logger.info(f"Pergunta recebida: {pergunta_cliente}")

    # 🔍 Busca filtrada baseada na pergunta
    dados = buscar_vendas_por_texto(pergunta_cliente)

    if not dados:
        dados = "Nenhum dado relevante encontrado no banco."

    prompt = f"""
Você é um agente de atendimento da empresa.

REGRAS:
- Responda SOMENTE com base nos dados fornecidos
- Se não houver dados, diga claramente que não encontrou informação
- NÃO invente valores
- NÃO faça suposições

DADOS:
{dados}

PERGUNTA:
{pergunta_cliente}
""".strip()

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )

    resposta = response.output[0].content[0].text
    logger.info("Resposta gerada com sucesso")

    return resposta

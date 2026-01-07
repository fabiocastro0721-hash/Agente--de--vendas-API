# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Chave da OpenAI (opcional – só usada se o agent chamar IA)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Chave interna para proteger a API (obrigatória para endpoints protegidos)
API_KEY_INTERNA = os.getenv("API_KEY_INTERNA")

if not API_KEY_INTERNA:
    print("⚠️ API_KEY_INTERNA não configurada — rotas protegidas podem falhar")

if not OPENAI_API_KEY:
    print("⚠️ OPENAI_API_KEY não configurada — funções de IA desativadas")

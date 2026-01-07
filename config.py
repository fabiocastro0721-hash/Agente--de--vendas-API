# config.py
import os

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# API interna
API_KEY_INTERNA = os.getenv("API_KEY_INTERNA")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY não configurada no ambiente")

if not API_KEY_INTERNA:
    raise RuntimeError("API_KEY_INTERNA não configurada no ambiente")

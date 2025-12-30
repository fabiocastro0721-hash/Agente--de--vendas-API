# config.py
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
API_KEY_INTERNA = os.getenv("API_KEY_INTERNA")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY não encontrada no .env")

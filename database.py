# agente_api/database.py
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "empresa.db"


def criar_banco():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_lancamento TEXT,
            data_vencimento TEXT,
            data_documento TEXT,
            serie TEXT,
            n_doc TEXT,
            n_transacao TEXT,
            conta_controle TEXT,
            ctacontabcodpn TEXT,
            observacoes TEXT
        )
    """)

    conn.commit()
    conn.close()


def buscar_vendas_por_texto(texto: str, limit: int = 20):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    like = f"%{texto.lower()}%"

    cursor.execute("""
        SELECT
            data_documento,
            serie,
            n_doc,
            observacoes
        FROM vendas
        WHERE
            LOWER(serie) LIKE ?
            OR LOWER(n_doc) LIKE ?
            OR LOWER(observacoes) LIKE ?
        ORDER BY id DESC
        LIMIT ?
    """, (like, like, like, limit))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return ""

    return "\n".join(
        f"Data: {d} | Série: {s} | Doc: {n} | Obs: {o}"
        for d, s, n, o in rows
    )

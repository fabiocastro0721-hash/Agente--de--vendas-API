# database.py
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
            cliente TEXT NOT NULL,
            produto TEXT NOT NULL,
            valor REAL NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def inserir_dados_teste():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM vendas")
    qtd = cursor.fetchone()[0]

    if qtd == 0:
        cursor.executemany("""
            INSERT INTO vendas (cliente, produto, valor)
            VALUES (?, ?, ?)
        """, [
            ("João", "Notebook", 3500),
            ("Maria", "Smartphone", 1500)
        ])
        conn.commit()

    conn.close()

def buscar_vendas():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT cliente, produto, valor FROM vendas")
    rows = cursor.fetchall()
    conn.close()

    return "\n".join(
        f"Cliente: {c}, Produto: {p}, Valor: {v}"
        for c, p, v in rows
    )

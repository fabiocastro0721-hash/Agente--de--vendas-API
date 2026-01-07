import pandas as pd
import sqlite3
from pathlib import Path
import unicodedata

SHEET_URL = "https://docs.google.com/spreadsheets/d/1wH4Yq76iiWRtGC7BLA0FxbR2fiNakHZg/export?format=csv"

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "empresa.db"


def normalizar_coluna(col: str) -> str:
    col = col.strip().lower()
    col = unicodedata.normalize("NFKD", col)
    col = col.encode("ascii", "ignore").decode("ascii")
    col = col.replace(" ", "_").replace(".", "").replace("/", "")
    return col


def importar_google_sheets():
    df = pd.read_csv(SHEET_URL)

    # Normaliza nomes das colunas (100% seguro)
    df.columns = [normalizar_coluna(c) for c in df.columns]

    print("Colunas encontradas:", df.columns.tolist())

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM vendas")

    for _, row in df.iterrows():
        cursor.execute(
            """
            INSERT INTO vendas (
                data_lancamento,
                data_vencimento,
                data_documento,
                serie,
                n_doc,
                n_transacao,
                conta_controle,
                ctacontabcodpn,
                observacoes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row.get("data_de_lancamento"),
                row.get("data_de_vencimento"),
                row.get("data_do_documento"),
                row.get("serie"),
                row.get("n_doc"),
                row.get("n_transacao"),
                row.get("conta_controle"),
                row.get("ctacontabcodpn"),
                row.get("observacoes"),
            )
        )

    conn.commit()
    conn.close()

    print("✅ Google Sheets importado com sucesso!")


if __name__ == "__main__":
    importar_google_sheets()

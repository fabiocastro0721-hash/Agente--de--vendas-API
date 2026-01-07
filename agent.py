from typing import List
from database import buscar_vendas_por_texto, carregar_planilha
import pandas as pd


def detectar_intencoes(pergunta: str) -> List[str]:
    p = pergunta.lower()
    intencoes = []

    if "cancelad" in p:
        intencoes.append("notas_canceladas")

    if "vencimento" in p and ("antig" in p or "mais antiga" in p):
        intencoes.append("vencimento_mais_antigo")

    if "quantas" in p or "total" in p:
        intencoes.append("total_lancamentos")

    return intencoes
def consultar_notas_canceladas():
    resultados = buscar_vendas_por_texto("cancel")
    return len(resultados)


def consultar_vencimento_mais_antigo(df):
    df["Data de vencimento"] = pd.to_datetime(
        df["Data de vencimento"], errors="coerce"
    )
    data = df["Data de vencimento"].min()
    return None if pd.isna(data) else data.date()


def consultar_total_lancamentos(df):
    return len(df)

def agente(pergunta: str) -> str:
    intencoes = detectar_intencoes(pergunta)

    if not intencoes:
        return (
            "Não consegui identificar o que você deseja consultar na planilha. "
            "Você pode perguntar, por exemplo:\n"
            "- Existe nota fiscal cancelada?\n"
            "- Qual a data de vencimento mais antiga?\n"
            "- Quantos lançamentos existem?"
        )

    respostas = []
    df = carregar_planilha()

    for intencao in intencoes:

        if intencao == "notas_canceladas":
            total = consultar_notas_canceladas()
            if total == 0:
                respostas.append("❌ Não há notas fiscais canceladas.")
            else:
                respostas.append(
                    f"⚠️ Existem {total} notas fiscais canceladas."
                )

        elif intencao == "vencimento_mais_antigo":
            data = consultar_vencimento_mais_antigo(df)
            if data:
                respostas.append(
                    f"📅 A data de vencimento mais antiga é {data}."
                )

        elif intencao == "total_lancamentos":
            total = consultar_total_lancamentos(df)
            respostas.append(
                f"📊 A planilha possui {total} lançamentos."
            )

    return "\n".join(respostas)

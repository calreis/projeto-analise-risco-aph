from pathlib import Path

import pandas as pd


DIRETORIO = Path(__file__).resolve().parent
CAMINHO_CSV = DIRETORIO / "atendimentos_aph.csv"

COLUNAS_OBRIGATORIAS = [
    "id_atendimento",
    "id_paciente",
    "idade",
    "hipertensao",
    "diabetes",
    "tabagismo",
    "sedentarismo",
    "obesidade",
    "doenca_cardiaca",
    "motivo_chamado",
    "chamados_anteriores",
    "desfecho_registrado",
]


def carregar_dados(caminho=CAMINHO_CSV):
    """Carrega o CSV e verifica sua estrutura básica."""

    try:
        df = pd.read_csv(
            caminho,
            dtype={"id_paciente": "string"}
        )

    except FileNotFoundError as erro:
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}"
        ) from erro

    except pd.errors.EmptyDataError as erro:
        raise ValueError(
            "O arquivo CSV está vazio."
        ) from erro

    except pd.errors.ParserError as erro:
        raise ValueError(
            "Não foi possível interpretar a estrutura do CSV."
        ) from erro

    colunas_ausentes = [
        coluna
        for coluna in COLUNAS_OBRIGATORIAS
        if coluna not in df.columns
    ]

    if colunas_ausentes:
        raise ValueError(
            f"Colunas obrigatórias ausentes: {colunas_ausentes}"
        )

    return df


if __name__ == "__main__":
    try:
        df = carregar_dados()

        print("PRIMEIRAS CINCO LINHAS")
        print(df.head())

        print("\nDIMENSÕES DA BASE")
        print(f"Linhas: {df.shape[0]}")
        print(f"Colunas: {df.shape[1]}")

        print("\nNOMES DAS COLUNAS")
        print(df.columns.tolist())

        print("\nTIPOS DE DADOS E VALORES NÃO NULOS")
        df.info()

        print("\nVALORES AUSENTES")
        print(df.isna().sum())

    except (FileNotFoundError, ValueError) as erro:
        print(f"Falha na importação: {erro}")
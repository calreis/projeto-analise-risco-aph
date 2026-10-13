from pathlib import Path

import numpy as np
import pandas as pd

from import_dados import carregar_dados


COLUNAS_BINARIAS = [
    "hipertensao",
    "diabetes",
    "tabagismo",
    "sedentarismo",
    "obesidade",
    "doenca_cardiaca",
]

MAPA_BINARIO = {
    "1": 1,
    "1.0": 1,
    "sim": 1,
    "s": 1,
    "true": 1,
    "verdadeiro": 1,

    "0": 0,
    "0.0": 0,
    "não": 0,
    "nao": 0,
    "n": 0,
    "false": 0,
    "falso": 0,
}


def tratar_dados(df_bruto):
    """Limpa e valida os registros de atendimento."""

    df = df_bruto.copy()

    quantidade_inicial = len(df)

    # 1. Normalização do identificador do paciente
    df["id_paciente"] = (
        df["id_paciente"]
        .astype("string")
        .str.strip()
        .replace("", pd.NA)
    )

    # 2. Conversão e validação do identificador do atendimento
    id_numerico = pd.to_numeric(
        df["id_atendimento"],
        errors="coerce"
    )

    id_valido = (
        id_numerico.notna()
        & id_numerico.mod(1).eq(0)
    )

    ids_invalidos = int((~id_valido).sum())

    df = df.loc[id_valido].copy()

    df["id_atendimento"] = (
        id_numerico.loc[id_valido]
        .astype("int64")
    )

    # 3. Conversão da idade
    df["idade"] = pd.to_numeric(
        df["idade"],
        errors="coerce"
    )

    # Primeiro invalidamos idades fora do intervalo definido.
    idade_valida = df["idade"].between(0, 120)

    df.loc[~idade_valida, "idade"] = np.nan

    # Idade deve ser expressa em anos completos.
    idade_nao_inteira = (
        df["idade"].notna()
        & df["idade"].mod(1).ne(0)
    )

    df.loc[idade_nao_inteira, "idade"] = np.nan
    df["idade"] = df["idade"].astype("Int64")

    # 4. Conversão e validação de chamadas anteriores
    df["chamados_anteriores"] = pd.to_numeric(
        df["chamados_anteriores"],
        errors="coerce"
    )

    chamadas_invalidas = (
        df["chamados_anteriores"].notna()
        & (
            df["chamados_anteriores"].lt(0)
            | df["chamados_anteriores"].mod(1).ne(0)
        )
    )

    df.loc[
        chamadas_invalidas,
        "chamados_anteriores"
    ] = np.nan

    df["chamados_anteriores"] = (
        df["chamados_anteriores"].astype("Int64")
    )

    # 5. Tratamento das variáveis binárias
    for coluna in COLUNAS_BINARIAS:
        valores = (
            df[coluna]
            .astype("string")
            .str.strip()
            .str.lower()
        )

        # Valores não reconhecidos viram ausentes,
        # em vez de serem interpretados automaticamente como zero.
        df[coluna] = valores.map(
            MAPA_BINARIO
        ).astype("Int64")

    # 6. Padronização das categorias textuais
    for coluna in [
        "motivo_chamado",
        "desfecho_registrado",
    ]:
        df[coluna] = (
            df[coluna]
            .astype("string")
            .str.strip()
            .str.lower()
            .replace("", pd.NA)
        )

    # 7. Remoção de linhas integralmente duplicadas
    duplicados_exatos = int(df.duplicated().sum())

    df = df.drop_duplicates().copy()

    # Não removemos automaticamente registros com o mesmo ID
    # e conteúdos diferentes: eles exigem investigação.
    ids_repetidos = int(
        df["id_atendimento"].duplicated().sum()
    )

    # 8. Relatório de qualidade
    print("\nRELATÓRIO DE TRATAMENTO")
    print(f"Registros iniciais: {quantidade_inicial}")
    print(f"IDs inválidos removidos: {ids_invalidos}")
    print(f"Linhas integralmente duplicadas removidas: {duplicados_exatos}")
    print(f"Registros restantes: {len(df)}")
    print(f"IDs de atendimento repetidos restantes: {ids_repetidos}")

    print("\nVALORES AUSENTES APÓS O TRATAMENTO")
    print(df.isna().sum())

    if ids_repetidos:
        print(
            "\nATENÇÃO: existem IDs de atendimento repetidos "
            "com conteúdos diferentes. Investigue antes da carga."
        )

    return df


if __name__ == "__main__":
    try:
        df_bruto = carregar_dados()
        df_tratado = tratar_dados(df_bruto)

        caminho_saida = (
            Path(__file__).resolve().parent
            / "atendimentos_aph_tratados.csv"
        )

        df_tratado.to_csv(
            caminho_saida,
            index=False
        )

        print(f"\nArquivo tratado salvo em: {caminho_saida}")

    except (FileNotFoundError, ValueError) as erro:
        print(f"Falha no tratamento: {erro}")
import pandas as pd
from scipy.stats import chi2_contingency

from import_dados import carregar_dados
from tratamento import tratar_dados


def executar_analise():
    df_bruto = carregar_dados()
    df = tratar_dados(df_bruto)

    # ==========================================
    # 1. MEDIDAS DE POSIÇÃO E VARIABILIDADE
    # ==========================================

    idade = df["idade"].dropna()

    if idade.empty:
        raise ValueError(
            "Não há idades válidas para calcular as estatísticas."
        )

    print("\nDIAGNÓSTICO ESTATÍSTICO: IDADE")

    print(f"Média: {idade.mean():.2f}")
    print(f"Mediana: {idade.median():.2f}")
    print(f"Moda: {idade.mode().tolist()}")

    print("\nQuartis e percentis:")
    print(idade.quantile([0.25, 0.50, 0.75, 0.90, 0.95]))

    print(f"\nVariância amostral: {idade.var():.2f}")
    print(f"Desvio padrão amostral: {idade.std():.2f}")

    amplitude = idade.max() - idade.min()
    print(f"Amplitude: {amplitude:.2f}")

    q1 = idade.quantile(0.25)
    q3 = idade.quantile(0.75)
    iqr = q3 - q1

    print(f"Intervalo interquartil (IQR): {iqr:.2f}")

    # ==========================================
    # 2. FREQUÊNCIA DAS CATEGORIAS
    # ==========================================

    print("\nFREQUÊNCIA DOS MOTIVOS DOS CHAMADOS")

    print(
        df["motivo_chamado"]
        .value_counts(dropna=False)
    )

    # ==========================================
    # 3. TESTE QUI-QUADRADO
    # ==========================================

    print("\nTESTE DE HIPÓTESE: QUI-QUADRADO")

    dados_teste = df[
        ["motivo_chamado", "desfecho_registrado"]
    ].dropna()

    tabela = pd.crosstab(
        dados_teste["motivo_chamado"],
        dados_teste["desfecho_registrado"]
    )

    if tabela.shape[0] < 2 or tabela.shape[1] < 2:
        print(
            "Não há categorias suficientes para executar "
            "o teste de independência."
        )
        return

    qui2, p_valor, gl, esperado = chi2_contingency(tabela)

    print(f"Qui-quadrado: {qui2:.4f}")
    print(f"Graus de liberdade: {gl}")
    print(f"p-valor: {p_valor:.6f}")

    # Verificação das frequências esperadas
    percentual_menor_que_5 = (esperado < 5).mean() * 100
    existe_menor_que_1 = (esperado < 1).any()

    print(
        "Percentual de células com frequência esperada "
        f"inferior a 5: {percentual_menor_que_5:.1f}%"
    )

    if existe_menor_que_1 or percentual_menor_que_5 > 20:
        print(
            "ATENÇÃO: as frequências esperadas podem não "
            "satisfazer os critérios usuais da aproximação "
            "do Qui-quadrado. Avalie outro método ou "
            "uma estratégia justificada para categorias raras."
        )

    # Hipóteses
    print("\nH0: motivo do chamado e desfecho são independentes.")
    print("H1: existe associação entre motivo e desfecho.")

    alpha = 0.05

    if p_valor < alpha:
        print(
            "Resultado: rejeitamos H0 ao nível de 5%. "
            "Há evidência estatística de associação."
        )
    else:
        print(
            "Resultado: não rejeitamos H0 ao nível de 5%. "
            "Não há evidência estatística suficiente para "
            "concluir que existe associação."
        )


if __name__ == "__main__":
    try:
        executar_analise()

    except (FileNotFoundError, ValueError) as erro:
        print(f"Falha na análise: {erro}")
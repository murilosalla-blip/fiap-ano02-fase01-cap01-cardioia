"""Gera análises, intervalos de confiança e visualizações da Fase 2."""

from __future__ import annotations

from pathlib import Path

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    auc,
    precision_recall_curve,
    roc_curve,
)
from sklearn.model_selection import train_test_split

from treinar_baselines import (
    DIRETORIO_RESULTADOS,
    ROTULOS_FAIXA_ETARIA,
    SEMENTE,
    calcular_metricas,
    carregar_dados,
    categorizar_faixa_etaria,
)


DIRETORIO_GRAFICOS = DIRETORIO_RESULTADOS / "graficos"
CAMINHO_MODELO = DIRETORIO_RESULTADOS / "melhor_modelo.joblib"
N_BOOTSTRAP = 2_000
COR_PRINCIPAL = "#C81D77"
CORES_GRUPOS = {
    "feminino": "#6750A4",
    "masculino": "#00796B",
}


def preparar_teste() -> tuple[pd.DataFrame, pd.Series]:
    """Reproduz exatamente a divisão usada no treinamento."""
    atributos, alvo = carregar_dados()
    _, atributos_teste, _, alvo_teste = train_test_split(
        atributos,
        alvo,
        test_size=0.20,
        stratify=alvo,
        random_state=SEMENTE,
    )
    return atributos_teste, alvo_teste


def estimar_intervalos(
    atributos_teste: pd.DataFrame,
    alvo_teste: pd.Series,
    predicoes: np.ndarray,
    probabilidades: np.ndarray,
) -> pd.DataFrame:
    """Calcula IC 95% por bootstrap geral, por sexo e por faixa etária."""
    rng = np.random.default_rng(SEMENTE)
    grupos: dict[str, tuple[str, np.ndarray]] = {
        "geral": ("geral", np.ones(len(atributos_teste), dtype=bool)),
    }
    for sexo in sorted(atributos_teste["sexo"].dropna().unique()):
        grupos[str(sexo)] = (
            "sexo",
            atributos_teste["sexo"].eq(sexo).to_numpy(),
        )
    faixas_etarias = categorizar_faixa_etaria(atributos_teste["idade"])
    for faixa in ROTULOS_FAIXA_ETARIA:
        grupos[faixa] = ("faixa_etaria", faixas_etarias.eq(faixa).to_numpy())

    nomes_metricas = [
        "acuracia",
        "precisao",
        "recall_sensibilidade",
        "f1",
        "taxa_falso_positivo",
        "taxa_falso_negativo",
        "roc_auc",
    ]
    linhas: list[dict[str, float | int | str]] = []

    for grupo, (dimensao, mascara) in grupos.items():
        y_grupo = alvo_teste.to_numpy()[mascara]
        pred_grupo = predicoes[mascara]
        prob_grupo = probabilidades[mascara]
        estimativas = calcular_metricas(y_grupo, pred_grupo, prob_grupo)
        amostras = {metrica: [] for metrica in nomes_metricas}

        for _ in range(N_BOOTSTRAP):
            indices = rng.integers(0, len(y_grupo), size=len(y_grupo))
            metricas = calcular_metricas(
                y_grupo[indices],
                pred_grupo[indices],
                prob_grupo[indices],
            )
            for metrica in nomes_metricas:
                valor = float(metricas[metrica])
                if np.isfinite(valor):
                    amostras[metrica].append(valor)

        for metrica in nomes_metricas:
            valores = np.asarray(amostras[metrica], dtype=float)
            linhas.append(
                {
                    "dimensao": dimensao,
                    "grupo": grupo,
                    "n": int(len(y_grupo)),
                    "metrica": metrica,
                    "estimativa": float(estimativas[metrica]),
                    "ic95_inferior": (
                        float(np.quantile(valores, 0.025)) if valores.size else np.nan
                    ),
                    "ic95_superior": (
                        float(np.quantile(valores, 0.975)) if valores.size else np.nan
                    ),
                    "reamostragens_validas": int(valores.size),
                }
            )

    return pd.DataFrame(linhas)


def configurar_grafico(titulo: str, xlabel: str, ylabel: str) -> None:
    plt.title(titulo, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(alpha=0.2)
    plt.tight_layout()


def salvar_matriz_confusao(
    alvo_teste: pd.Series,
    predicoes: np.ndarray,
) -> None:
    _, eixo = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(
        alvo_teste,
        predicoes,
        display_labels=["Ausente", "Presente"],
        cmap="RdPu",
        colorbar=False,
        ax=eixo,
    )
    eixo.set_title("Matriz de confusão — conjunto de teste", fontweight="bold")
    eixo.set_xlabel("Classe predita")
    eixo.set_ylabel("Classe real")
    plt.tight_layout()
    plt.savefig(DIRETORIO_GRAFICOS / "matriz_confusao.png", dpi=180)
    plt.close()


def salvar_curva_roc(
    atributos_teste: pd.DataFrame,
    alvo_teste: pd.Series,
    probabilidades: np.ndarray,
) -> None:
    plt.figure(figsize=(7, 6))
    fpr, tpr, _ = roc_curve(alvo_teste, probabilidades)
    plt.plot(
        fpr,
        tpr,
        color=COR_PRINCIPAL,
        linewidth=2.5,
        label=f"Geral (AUC = {auc(fpr, tpr):.3f})",
    )

    for sexo, cor in CORES_GRUPOS.items():
        mascara = atributos_teste["sexo"].eq(sexo).to_numpy()
        y_grupo = alvo_teste.to_numpy()[mascara]
        if np.unique(y_grupo).size < 2:
            continue
        fpr_grupo, tpr_grupo, _ = roc_curve(y_grupo, probabilidades[mascara])
        plt.plot(
            fpr_grupo,
            tpr_grupo,
            color=cor,
            linewidth=1.8,
            label=f"{sexo.capitalize()} (AUC = {auc(fpr_grupo, tpr_grupo):.3f})",
        )

    plt.plot([0, 1], [0, 1], linestyle="--", color="#666666", label="Aleatório")
    plt.legend(loc="lower right")
    configurar_grafico(
        "Curva ROC — geral e por sexo",
        "Taxa de falso positivo",
        "Taxa de verdadeiro positivo",
    )
    plt.savefig(DIRETORIO_GRAFICOS / "curva_roc.png", dpi=180)
    plt.close()


def salvar_curva_precisao_recall(
    atributos_teste: pd.DataFrame,
    alvo_teste: pd.Series,
    probabilidades: np.ndarray,
) -> None:
    plt.figure(figsize=(7, 6))
    precisao, recall, _ = precision_recall_curve(alvo_teste, probabilidades)
    plt.plot(
        recall,
        precisao,
        color=COR_PRINCIPAL,
        linewidth=2.5,
        label=f"Geral (AUC = {auc(recall, precisao):.3f})",
    )

    for sexo, cor in CORES_GRUPOS.items():
        mascara = atributos_teste["sexo"].eq(sexo).to_numpy()
        y_grupo = alvo_teste.to_numpy()[mascara]
        if np.unique(y_grupo).size < 2:
            continue
        precisao_grupo, recall_grupo, _ = precision_recall_curve(
            y_grupo,
            probabilidades[mascara],
        )
        plt.plot(
            recall_grupo,
            precisao_grupo,
            color=cor,
            linewidth=1.8,
            label=(
                f"{sexo.capitalize()} "
                f"(AUC = {auc(recall_grupo, precisao_grupo):.3f})"
            ),
        )

    plt.axhline(
        alvo_teste.mean(),
        linestyle="--",
        color="#666666",
        label="Prevalência observada no teste",
    )
    plt.legend(loc="lower left")
    configurar_grafico(
        "Curva precisão-recall — geral e por sexo",
        "Recall",
        "Precisão",
    )
    plt.savefig(DIRETORIO_GRAFICOS / "curva_precisao_recall.png", dpi=180)
    plt.close()


def salvar_curva_calibracao(
    alvo_teste: pd.Series,
    probabilidades: np.ndarray,
) -> None:
    proporcao_positivos, probabilidade_media = calibration_curve(
        alvo_teste,
        probabilidades,
        n_bins=6,
        strategy="quantile",
    )
    plt.figure(figsize=(7, 6))
    plt.plot([0, 1], [0, 1], linestyle="--", color="#666666", label="Ideal")
    plt.plot(
        probabilidade_media,
        proporcao_positivos,
        marker="o",
        color=COR_PRINCIPAL,
        linewidth=2.2,
        label="Regressão Logística",
    )
    plt.legend(loc="upper left")
    configurar_grafico(
        "Curva de calibração — conjunto de teste",
        "Probabilidade média prevista",
        "Fração observada de positivos",
    )
    plt.savefig(DIRETORIO_GRAFICOS / "curva_calibracao.png", dpi=180)
    plt.close()


def salvar_distribuicao_alvo(
    atributos_teste: pd.DataFrame,
    alvo_teste: pd.Series,
) -> None:
    dados = pd.DataFrame(
        {
            "sexo": atributos_teste["sexo"].to_numpy(),
            "diagnostico": alvo_teste.map({0: "Ausente", 1: "Presente"}).to_numpy(),
        }
    )
    contagens = pd.crosstab(dados["sexo"], dados["diagnostico"])
    contagens = contagens.reindex(columns=["Ausente", "Presente"], fill_value=0)

    eixo = contagens.plot(
        kind="bar",
        stacked=True,
        figsize=(7, 5),
        color=["#B8B8B8", COR_PRINCIPAL],
    )
    eixo.set_xticklabels([texto.get_text().capitalize() for texto in eixo.get_xticklabels()])
    eixo.legend(title="Diagnóstico")
    configurar_grafico(
        "Distribuição do diagnóstico por sexo — teste",
        "Sexo",
        "Número de pacientes",
    )
    plt.savefig(DIRETORIO_GRAFICOS / "distribuicao_alvo_por_sexo.png", dpi=180)
    plt.close()


def salvar_distribuicao_alvo_por_faixa_etaria(
    atributos_teste: pd.DataFrame,
    alvo_teste: pd.Series,
) -> None:
    """Mostra tamanho e composição do teste em cada faixa etária."""
    dados = pd.DataFrame(
        {
            "faixa_etaria": categorizar_faixa_etaria(
                atributos_teste["idade"]
            ).to_numpy(),
            "diagnostico": alvo_teste.map(
                {0: "Ausente", 1: "Presente"}
            ).to_numpy(),
        }
    )
    contagens = pd.crosstab(dados["faixa_etaria"], dados["diagnostico"])
    contagens = contagens.reindex(
        index=ROTULOS_FAIXA_ETARIA,
        columns=["Ausente", "Presente"],
        fill_value=0,
    )
    eixo = contagens.plot(
        kind="bar",
        stacked=True,
        figsize=(8, 5),
        color=["#B8B8B8", COR_PRINCIPAL],
    )
    eixo.set_xticklabels(eixo.get_xticklabels(), rotation=0)
    eixo.legend(title="Diagnóstico")
    configurar_grafico(
        "Distribuição do diagnóstico por faixa etária — teste",
        "Faixa etária",
        "Número de pacientes",
    )
    plt.savefig(
        DIRETORIO_GRAFICOS / "distribuicao_alvo_por_faixa_etaria.png",
        dpi=180,
    )
    plt.close()


def salvar_importancia_variaveis(modelo: object) -> pd.DataFrame:
    """Extrai coeficientes ou importâncias do pipeline selecionado."""
    preprocessador = modelo.named_steps["preprocessamento"]
    estimador = modelo.named_steps["modelo"]
    nomes = preprocessador.get_feature_names_out()

    if hasattr(estimador, "coef_"):
        valores = estimador.coef_[0]
        tipo = "coeficiente"
    elif hasattr(estimador, "feature_importances_"):
        valores = estimador.feature_importances_
        tipo = "importancia"
    else:
        raise TypeError("O modelo selecionado não expõe coeficientes ou importâncias.")

    nomes_limpos = [
        nome.replace("numerico__", "").replace("categorico__", "")
        for nome in nomes
    ]
    tabela = pd.DataFrame(
        {
            "variavel_transformada": nomes_limpos,
            tipo: valores,
            "magnitude_absoluta": np.abs(valores),
        }
    ).sort_values("magnitude_absoluta", ascending=False)
    tabela.to_csv(
        DIRETORIO_RESULTADOS / "importancia_variaveis.csv",
        index=False,
    )

    principais = tabela.head(15).sort_values(tipo)
    cores = [
        "#00796B" if valor >= 0 else "#C81D77"
        for valor in principais[tipo]
    ]
    plt.figure(figsize=(9, 7))
    plt.barh(principais["variavel_transformada"], principais[tipo], color=cores)
    plt.axvline(0, color="#333333", linewidth=0.8)
    configurar_grafico(
        "Variáveis com maior influência no modelo",
        "Coeficiente padronizado" if tipo == "coeficiente" else "Importância",
        "Variável transformada",
    )
    plt.savefig(DIRETORIO_GRAFICOS / "importancia_variaveis.png", dpi=180)
    plt.close()

    return tabela


def main() -> None:
    if not CAMINHO_MODELO.exists():
        raise FileNotFoundError(
            "Modelo não encontrado. Execute primeiro: "
            "python fase2/src/treinar_baselines.py"
        )

    DIRETORIO_GRAFICOS.mkdir(parents=True, exist_ok=True)
    atributos_teste, alvo_teste = preparar_teste()
    modelo = joblib.load(CAMINHO_MODELO)
    predicoes = modelo.predict(atributos_teste)
    probabilidades = modelo.predict_proba(atributos_teste)[:, 1]

    intervalos = estimar_intervalos(
        atributos_teste,
        alvo_teste,
        predicoes,
        probabilidades,
    )
    intervalos.to_csv(
        DIRETORIO_RESULTADOS / "intervalos_confianca_bootstrap.csv",
        index=False,
    )

    salvar_matriz_confusao(alvo_teste, predicoes)
    salvar_curva_roc(atributos_teste, alvo_teste, probabilidades)
    salvar_curva_precisao_recall(atributos_teste, alvo_teste, probabilidades)
    salvar_curva_calibracao(alvo_teste, probabilidades)
    salvar_distribuicao_alvo(atributos_teste, alvo_teste)
    salvar_distribuicao_alvo_por_faixa_etaria(atributos_teste, alvo_teste)
    salvar_importancia_variaveis(modelo)

    print(f"Intervalos calculados com {N_BOOTSTRAP} reamostragens.")
    print(f"Análises salvas em: {DIRETORIO_RESULTADOS}")


if __name__ == "__main__":
    main()

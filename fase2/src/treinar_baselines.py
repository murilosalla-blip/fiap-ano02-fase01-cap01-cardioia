"""Treina baselines tabulares reprodutíveis para a Fase 2 do CardioIA.

Execute a partir de qualquer diretório:
    python fase2/src/treinar_baselines.py
"""

from __future__ import annotations

import json
import random
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_validate, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


SEMENTE = 42
RAIZ_REPOSITORIO = Path(__file__).resolve().parents[2]
CAMINHO_DADOS = (
    RAIZ_REPOSITORIO
    / "assets"
    / "dados"
    / "processed"
    / "heart_disease_cleveland.csv"
)
DIRETORIO_RESULTADOS = RAIZ_REPOSITORIO / "fase2" / "resultados"
COLUNA_ALVO = "diagnostico_doenca_cardiaca"

COLUNAS_NUMERICAS = [
    "idade",
    "pressao_arterial_repouso",
    "colesterol",
    "frequencia_cardiaca_maxima",
    "depressao_st_exercicio",
    "num_vasos_principais",
]

COLUNAS_CATEGORICAS = [
    "sexo",
    "tipo_dor_peito",
    "acucar_jejum_maior_120",
    "eletrocardiograma_repouso",
    "angina_induzida_exercicio",
    "inclinacao_st_pico_exercicio",
    "resultado_thal",
]

ROTULOS_FAIXA_ETARIA = [
    "até 49 anos",
    "50 a 59 anos",
    "60 anos ou mais",
]


def carregar_dados() -> tuple[pd.DataFrame, pd.Series]:
    """Carrega e valida o dataset processado da Fase 1."""
    if not CAMINHO_DADOS.exists():
        raise FileNotFoundError(
            f"Dataset não encontrado em {CAMINHO_DADOS}. "
            "Execute o script a partir de uma cópia completa do repositório."
        )

    dados = pd.read_csv(CAMINHO_DADOS)

    colunas_esperadas = set(COLUNAS_NUMERICAS + COLUNAS_CATEGORICAS + [COLUNA_ALVO])
    colunas_ausentes = colunas_esperadas.difference(dados.columns)
    if colunas_ausentes:
        raise ValueError(
            "O dataset não contém todas as colunas esperadas: "
            + ", ".join(sorted(colunas_ausentes))
        )

    if dados.empty:
        raise ValueError("O dataset está vazio.")

    valores_alvo = set(dados[COLUNA_ALVO].dropna().unique())
    if valores_alvo != {"ausente", "presente"}:
        raise ValueError(
            "Valores inesperados na variável-alvo: "
            + ", ".join(sorted(map(str, valores_alvo)))
        )

    atributos = dados[COLUNAS_NUMERICAS + COLUNAS_CATEGORICAS].copy()
    alvo = dados[COLUNA_ALVO].map({"ausente": 0, "presente": 1}).astype(int)

    # Na Fase 1, ausências herdadas da UCI foram preservadas como texto.
    atributos["num_vasos_principais"] = pd.to_numeric(
        atributos["num_vasos_principais"].replace("ausente", np.nan),
        errors="coerce",
    )
    atributos["resultado_thal"] = atributos["resultado_thal"].replace("ausente", np.nan)

    return atributos, alvo


def criar_preprocessador() -> ColumnTransformer:
    """Define transformações ajustadas exclusivamente dentro de cada treino."""
    pipeline_numerico = Pipeline(
        steps=[
            ("imputacao", SimpleImputer(strategy="median")),
            ("padronizacao", StandardScaler()),
        ]
    )
    pipeline_categorico = Pipeline(
        steps=[
            ("imputacao", SimpleImputer(strategy="most_frequent")),
            (
                "one_hot",
                OneHotEncoder(handle_unknown="ignore", sparse_output=False),
            ),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("numerico", pipeline_numerico, COLUNAS_NUMERICAS),
            ("categorico", pipeline_categorico, COLUNAS_CATEGORICAS),
        ],
        remainder="drop",
    )


def criar_modelos() -> dict[str, Pipeline]:
    """Cria modelos simples e interpretáveis para comparação inicial."""
    return {
        "regressao_logistica": Pipeline(
            steps=[
                ("preprocessamento", criar_preprocessador()),
                (
                    "modelo",
                    LogisticRegression(
                        class_weight="balanced",
                        max_iter=2_000,
                        random_state=SEMENTE,
                    ),
                ),
            ]
        ),
        "random_forest": Pipeline(
            steps=[
                ("preprocessamento", criar_preprocessador()),
                (
                    "modelo",
                    RandomForestClassifier(
                        n_estimators=500,
                        min_samples_leaf=2,
                        class_weight="balanced",
                        n_jobs=-1,
                        random_state=SEMENTE,
                    ),
                ),
            ]
        ),
    }


def categorizar_faixa_etaria(idades: pd.Series) -> pd.Series:
    """Agrupa idades em três faixas com amostras comparáveis na base Cleveland."""
    return pd.cut(
        idades,
        bins=[-np.inf, 49, 59, np.inf],
        labels=ROTULOS_FAIXA_ETARIA,
    )


def calcular_metricas(
    y_verdadeiro: pd.Series | np.ndarray,
    y_predito: np.ndarray,
    y_probabilidade: np.ndarray,
) -> dict[str, float | int]:
    """Calcula métricas de classificação, incluindo erros por classe."""
    y_real = np.asarray(y_verdadeiro)
    matriz = confusion_matrix(y_real, y_predito, labels=[0, 1])
    verdadeiros_negativos, falsos_positivos, falsos_negativos, verdadeiros_positivos = (
        matriz.ravel()
    )

    negativos = verdadeiros_negativos + falsos_positivos
    positivos = verdadeiros_positivos + falsos_negativos

    metricas: dict[str, float | int] = {
        "n": int(len(y_real)),
        "n_positivos": int(y_real.sum()),
        "prevalencia_observada": float(y_real.mean()),
        "acuracia": float(accuracy_score(y_real, y_predito)),
        "precisao": float(
            precision_score(y_real, y_predito, zero_division=0)
        ),
        "recall_sensibilidade": float(
            recall_score(y_real, y_predito, zero_division=0)
        ),
        "f1": float(f1_score(y_real, y_predito, zero_division=0)),
        "taxa_falso_positivo": (
            float(falsos_positivos / negativos) if negativos else np.nan
        ),
        "taxa_falso_negativo": (
            float(falsos_negativos / positivos) if positivos else np.nan
        ),
    }

    metricas["roc_auc"] = (
        float(roc_auc_score(y_real, y_probabilidade))
        if np.unique(y_real).size == 2
        else np.nan
    )
    return metricas


def avaliar_validacao_cruzada(
    modelos: dict[str, Pipeline],
    atributos_treino: pd.DataFrame,
    alvo_treino: pd.Series,
) -> pd.DataFrame:
    """Compara modelos sem consultar o conjunto de teste."""
    validacao = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=SEMENTE,
    )
    pontuacoes = {
        "acuracia": "accuracy",
        "precisao": "precision",
        "recall_sensibilidade": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc",
    }

    linhas: list[dict[str, float | str]] = []
    for nome, pipeline in modelos.items():
        resultados = cross_validate(
            pipeline,
            atributos_treino,
            alvo_treino,
            cv=validacao,
            scoring=pontuacoes,
            # Execução sequencial evita falhas em computadores com pouca memória.
            n_jobs=1,
            return_train_score=False,
        )
        for metrica in pontuacoes:
            valores = resultados[f"test_{metrica}"]
            linhas.append(
                {
                    "modelo": nome,
                    "metrica": metrica,
                    "media": float(np.mean(valores)),
                    "desvio_padrao": float(np.std(valores, ddof=1)),
                    "n_folds": int(len(valores)),
                }
            )

    return pd.DataFrame(linhas)


def main() -> None:
    random.seed(SEMENTE)
    np.random.seed(SEMENTE)
    DIRETORIO_RESULTADOS.mkdir(parents=True, exist_ok=True)

    atributos, alvo = carregar_dados()
    atributos_treino, atributos_teste, alvo_treino, alvo_teste = train_test_split(
        atributos,
        alvo,
        test_size=0.20,
        stratify=alvo,
        random_state=SEMENTE,
    )

    modelos = criar_modelos()
    metricas_cv = avaliar_validacao_cruzada(
        modelos,
        atributos_treino,
        alvo_treino,
    )
    metricas_cv.to_csv(
        DIRETORIO_RESULTADOS / "metricas_validacao_cruzada.csv",
        index=False,
    )

    ranking_auc = (
        metricas_cv[metricas_cv["metrica"] == "roc_auc"]
        .sort_values(["media", "desvio_padrao"], ascending=[False, True])
        .reset_index(drop=True)
    )
    melhor_nome = str(ranking_auc.loc[0, "modelo"])
    melhor_modelo = modelos[melhor_nome]
    melhor_modelo.fit(atributos_treino, alvo_treino)

    predicoes = melhor_modelo.predict(atributos_teste)
    probabilidades = melhor_modelo.predict_proba(atributos_teste)[:, 1]

    metricas_teste = calcular_metricas(
        alvo_teste,
        predicoes,
        probabilidades,
    )
    pd.DataFrame([{"modelo": melhor_nome, **metricas_teste}]).to_csv(
        DIRETORIO_RESULTADOS / "metricas_teste.csv",
        index=False,
    )

    linhas_subgrupo: list[dict[str, float | int | str]] = []
    for sexo in sorted(atributos_teste["sexo"].dropna().unique()):
        mascara = atributos_teste["sexo"].eq(sexo).to_numpy()
        metricas = calcular_metricas(
            alvo_teste.to_numpy()[mascara],
            predicoes[mascara],
            probabilidades[mascara],
        )
        linhas_subgrupo.append(
            {"modelo": melhor_nome, "sexo": str(sexo), **metricas}
        )

    pd.DataFrame(linhas_subgrupo).to_csv(
        DIRETORIO_RESULTADOS / "metricas_por_sexo.csv",
        index=False,
    )

    faixas_etarias = categorizar_faixa_etaria(atributos_teste["idade"])
    linhas_faixa_etaria: list[dict[str, float | int | str]] = []
    for faixa in ROTULOS_FAIXA_ETARIA:
        mascara = faixas_etarias.eq(faixa).to_numpy()
        metricas = calcular_metricas(
            alvo_teste.to_numpy()[mascara],
            predicoes[mascara],
            probabilidades[mascara],
        )
        linhas_faixa_etaria.append(
            {"modelo": melhor_nome, "faixa_etaria": faixa, **metricas}
        )

    pd.DataFrame(linhas_faixa_etaria).to_csv(
        DIRETORIO_RESULTADOS / "metricas_por_faixa_etaria.csv",
        index=False,
    )

    previsoes = atributos_teste[["idade", "sexo"]].copy()
    previsoes.insert(0, "indice_original", previsoes.index)
    previsoes["faixa_etaria"] = faixas_etarias.astype("string")
    previsoes["diagnostico_real"] = alvo_teste.map({0: "ausente", 1: "presente"})
    previsoes["diagnostico_predito"] = pd.Series(
        predicoes,
        index=atributos_teste.index,
    ).map({0: "ausente", 1: "presente"})
    previsoes["probabilidade_doenca"] = probabilidades
    previsoes.to_csv(
        DIRETORIO_RESULTADOS / "previsoes_teste.csv",
        index=False,
    )

    joblib.dump(
        melhor_modelo,
        DIRETORIO_RESULTADOS / "melhor_modelo.joblib",
    )

    metadados = {
        "semente": SEMENTE,
        "dataset": str(CAMINHO_DADOS.relative_to(RAIZ_REPOSITORIO)),
        "n_total": int(len(atributos)),
        "n_treino": int(len(atributos_treino)),
        "n_teste": int(len(atributos_teste)),
        "estratificacao": COLUNA_ALVO,
        "criterio_selecao": "maior ROC AUC média na validação cruzada do treino",
        "modelo_selecionado": melhor_nome,
        "modalidade": "dados clínicos tabulares",
    }
    (DIRETORIO_RESULTADOS / "metadados_execucao.json").write_text(
        json.dumps(metadados, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Modelo selecionado: {melhor_nome}")
    print(f"Resultados salvos em: {DIRETORIO_RESULTADOS}")


if __name__ == "__main__":
    main()

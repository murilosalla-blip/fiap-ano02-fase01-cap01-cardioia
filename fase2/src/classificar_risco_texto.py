"""Classificador textual acadêmico de risco com TF-IDF.

A base é inteiramente simulada. O modelo demonstra uma etapa de triagem textual,
mas não deve ser usado para diagnóstico, priorização real ou decisão clínica.
"""

from __future__ import annotations

import json
import random
import re
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline


SEMENTE = 42
RAIZ_FASE2 = Path(__file__).resolve().parents[1]
CAMINHO_DADOS = RAIZ_FASE2 / "dados" / "classificacao_risco.csv"
DIRETORIO_RESULTADOS = RAIZ_FASE2 / "resultados" / "nlp"


def carregar_dataset(caminho: Path = CAMINHO_DADOS) -> pd.DataFrame:
    dados = pd.read_csv(caminho)
    colunas = {"id_cenario", "sexo_referencia", "frase", "situacao"}
    ausentes = colunas.difference(dados.columns)
    if ausentes:
        raise ValueError("Colunas ausentes: " + ", ".join(sorted(ausentes)))
    if dados["frase"].isna().any() or dados["frase"].str.strip().eq("").any():
        raise ValueError("Existem frases vazias no dataset.")
    if set(dados["situacao"]) != {"baixo risco", "alto risco"}:
        raise ValueError("Os rótulos devem ser 'baixo risco' e 'alto risco'.")
    if dados["frase"].duplicated().any():
        raise ValueError("O dataset contém frases duplicadas.")
    if dados["id_cenario"].nunique() < 40:
        raise ValueError("O dataset precisa de maior diversidade de cenários.")
    return dados


def dividir_por_cenario(
    dados: pd.DataFrame,
    proporcao_teste: float = 0.2,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Separa pares contrafactuais sem vazar um cenário entre treino e teste."""
    gerador = random.Random(SEMENTE)
    ids_teste: set[str] = set()

    for _, grupo in dados.groupby("situacao", sort=True):
        ids = sorted(grupo["id_cenario"].unique())
        gerador.shuffle(ids)
        quantidade = max(1, round(len(ids) * proporcao_teste))
        ids_teste.update(ids[:quantidade])

    teste = dados[dados["id_cenario"].isin(ids_teste)].copy()
    treino = dados[~dados["id_cenario"].isin(ids_teste)].copy()

    if set(treino["id_cenario"]).intersection(teste["id_cenario"]):
        raise AssertionError("Um mesmo cenário apareceu em treino e teste.")
    if set(treino["situacao"]) != {"baixo risco", "alto risco"}:
        raise AssertionError("O treino perdeu uma das classes.")
    if set(teste["situacao"]) != {"baixo risco", "alto risco"}:
        raise AssertionError("O teste perdeu uma das classes.")
    return treino, teste


def criar_pipeline() -> Pipeline:
    return Pipeline(
        steps=[
            (
                "tfidf",
                TfidfVectorizer(
                    lowercase=True,
                    strip_accents="unicode",
                    ngram_range=(1, 2),
                    min_df=1,
                    sublinear_tf=True,
                ),
            ),
            (
                "modelo",
                LogisticRegression(
                    max_iter=2_000,
                    class_weight="balanced",
                    random_state=SEMENTE,
                ),
            ),
        ]
    )


def probabilidade_alto_risco(modelo: Pipeline, frases: pd.Series | list[str]):
    indice = list(modelo.classes_).index("alto risco")
    return modelo.predict_proba(frases)[:, indice]


def avaliar_entrada_textual(modelo: Pipeline, frase: str) -> dict[str, object]:
    """Classifica e explicita limites observáveis da entrada demonstrativa."""
    if not frase.strip():
        raise ValueError("A frase não pode estar vazia.")
    termos = int(modelo.named_steps["tfidf"].transform([frase]).nnz)
    probabilidade = float(probabilidade_alto_risco(modelo, [frase])[0])
    alertas = []
    if termos == 0:
        alertas.append("Nenhum termo conhecido pelo TF-IDF foi identificado.")
    if re.search(r"\b(?:não|nao|nunca|nego|nega|negou|sem|nem)\b", frase.lower()):
        alertas.append("Há possível negação; este classificador não interpreta contexto linguístico complexo.")
    return {
        "classe": str(modelo.predict([frase])[0]),
        "probabilidade_alto_risco": probabilidade,
        "termos_reconhecidos": termos,
        "alertas": alertas,
        "confiavel_para_demonstracao": not alertas,
    }


def avaliar_modelo(
    modelo: Pipeline,
    teste: pd.DataFrame,
) -> tuple[dict[str, object], pd.DataFrame]:
    previsoes = modelo.predict(teste["frase"])
    probabilidades = probabilidade_alto_risco(modelo, teste["frase"])
    verdadeiro_binario = (teste["situacao"] == "alto risco").astype(int)

    metricas: dict[str, object] = {
        "n_treino": None,
        "n_teste": int(len(teste)),
        "acuracia": float(accuracy_score(teste["situacao"], previsoes)),
        "precisao_alto_risco": float(
            precision_score(
                teste["situacao"],
                previsoes,
                pos_label="alto risco",
                zero_division=0,
            )
        ),
        "recall_alto_risco": float(
            recall_score(
                teste["situacao"],
                previsoes,
                pos_label="alto risco",
                zero_division=0,
            )
        ),
        "f1_alto_risco": float(
            f1_score(
                teste["situacao"],
                previsoes,
                pos_label="alto risco",
                zero_division=0,
            )
        ),
        "roc_auc": float(roc_auc_score(verdadeiro_binario, probabilidades)),
        "relatorio_classificacao": classification_report(
            teste["situacao"],
            previsoes,
            output_dict=True,
            zero_division=0,
        ),
    }

    tabela = teste[
        ["id_cenario", "sexo_referencia", "frase", "situacao"]
    ].copy()
    tabela["predicao"] = previsoes
    tabela["probabilidade_alto_risco"] = probabilidades
    return metricas, tabela


def analisar_vies_contrafactual(
    modelo: Pipeline,
    dados: pd.DataFrame,
) -> tuple[dict[str, float], pd.DataFrame]:
    """Compara versões feminina e masculina do mesmo relato."""
    tabela = dados[
        ["id_cenario", "sexo_referencia", "frase", "situacao"]
    ].copy()
    tabela["probabilidade_alto_risco"] = probabilidade_alto_risco(
        modelo,
        tabela["frase"],
    )
    pares = tabela.pivot(
        index=["id_cenario", "situacao"],
        columns="sexo_referencia",
        values="probabilidade_alto_risco",
    ).reset_index()
    if {"feminino", "masculino"}.difference(pares.columns):
        raise ValueError("Os pares contrafactuais por sexo estão incompletos.")

    pares["diferenca_absoluta"] = (
        pares["feminino"] - pares["masculino"]
    ).abs()
    resumo = {
        "media_probabilidade_feminino": float(pares["feminino"].mean()),
        "media_probabilidade_masculino": float(pares["masculino"].mean()),
        "diferenca_media_absoluta": float(pares["diferenca_absoluta"].mean()),
        "maior_diferenca_absoluta": float(pares["diferenca_absoluta"].max()),
    }
    return resumo, pares


def termos_mais_influentes(
    modelo: Pipeline,
    quantidade: int = 15,
) -> pd.DataFrame:
    vetorizador = modelo.named_steps["tfidf"]
    estimador = modelo.named_steps["modelo"]
    termos = vetorizador.get_feature_names_out()
    pesos = estimador.coef_[0]
    tabela = pd.DataFrame({"termo": termos, "coeficiente": pesos})
    maiores = tabela.nlargest(quantidade, "coeficiente").assign(
        direcao=str(estimador.classes_[1])
    )
    menores = tabela.nsmallest(quantidade, "coeficiente").assign(
        direcao=str(estimador.classes_[0])
    )
    return pd.concat([maiores, menores], ignore_index=True)


def treinar_e_avaliar():
    dados = carregar_dataset()
    treino, teste = dividir_por_cenario(dados)
    modelo = criar_pipeline()
    modelo.fit(treino["frase"], treino["situacao"])
    metricas, previsoes = avaliar_modelo(modelo, teste)
    metricas["n_treino"] = int(len(treino))
    vies, pares = analisar_vies_contrafactual(modelo, teste)
    return modelo, treino, teste, metricas, previsoes, vies, pares


def treinar_modelo_completo() -> Pipeline:
    dados = carregar_dataset()
    modelo = criar_pipeline()
    modelo.fit(dados["frase"], dados["situacao"])
    return modelo


def salvar_resultados() -> dict[str, object]:
    (
        modelo,
        treino,
        teste,
        metricas,
        previsoes,
        vies,
        pares,
    ) = treinar_e_avaliar()
    DIRETORIO_RESULTADOS.mkdir(parents=True, exist_ok=True)

    payload = {
        "semente": SEMENTE,
        "tipo_modelo": "Regressão Logística",
        "representacao": "TF-IDF com unigramas e bigramas",
        "separacao": "estratificada por classe e agrupada por id_cenario",
        "metricas": metricas,
        "analise_vies_contrafactual_sexo": vies,
        "aviso": "Base simulada; uso exclusivamente acadêmico.",
    }
    (DIRETORIO_RESULTADOS / "metricas_classificador_texto.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    previsoes.to_csv(
        DIRETORIO_RESULTADOS / "previsoes_teste_texto.csv",
        index=False,
    )
    pares.to_csv(
        DIRETORIO_RESULTADOS / "vies_contrafactual_sexo.csv",
        index=False,
    )
    termos_mais_influentes(modelo).to_csv(
        DIRETORIO_RESULTADOS / "termos_influentes.csv",
        index=False,
    )
    joblib.dump(modelo, DIRETORIO_RESULTADOS / "classificador_risco_texto.joblib")

    matriz = confusion_matrix(
        teste["situacao"],
        modelo.predict(teste["frase"]),
        labels=["baixo risco", "alto risco"],
    )
    exibicao = ConfusionMatrixDisplay(
        matriz,
        display_labels=["Baixo risco", "Alto risco"],
    )
    exibicao.plot(cmap="RdPu", colorbar=False)
    plt.title("Matriz de confusão — classificador textual")
    plt.tight_layout()
    plt.savefig(
        DIRETORIO_RESULTADOS / "matriz_confusao_texto.png",
        dpi=160,
    )
    plt.close()
    return payload


def main() -> None:
    resultado = salvar_resultados()
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

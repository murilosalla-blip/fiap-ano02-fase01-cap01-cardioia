"""Valida a avaliação tabular por faixa etária solicitada no feedback."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


DIRETORIO_FASE2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DIRETORIO_FASE2 / "src"))

from treinar_baselines import (  # noqa: E402
    ROTULOS_FAIXA_ETARIA,
    categorizar_faixa_etaria,
)


def main() -> None:
    exemplos = pd.Series([29, 49, 50, 59, 60, 77], name="idade")
    faixas = categorizar_faixa_etaria(exemplos).astype("string").tolist()
    assert faixas == [
        "até 49 anos",
        "até 49 anos",
        "50 a 59 anos",
        "50 a 59 anos",
        "60 anos ou mais",
        "60 anos ou mais",
    ]

    caminho_metricas = (
        DIRETORIO_FASE2 / "resultados" / "metricas_por_faixa_etaria.csv"
    )
    if not caminho_metricas.exists():
        raise AssertionError("Execute treinar_baselines.py antes deste teste.")

    metricas = pd.read_csv(caminho_metricas)
    assert metricas["faixa_etaria"].tolist() == ROTULOS_FAIXA_ETARIA
    assert metricas["n"].tolist() == [18, 25, 18]
    assert metricas["n"].sum() == 61
    assert metricas["n_positivos"].tolist() == [5, 12, 11]
    for coluna in ["acuracia", "precisao", "recall_sensibilidade", "f1", "roc_auc"]:
        assert metricas[coluna].between(0, 1).all()

    caminho_intervalos = (
        DIRETORIO_FASE2 / "resultados" / "intervalos_confianca_bootstrap.csv"
    )
    intervalos = pd.read_csv(caminho_intervalos)
    por_idade = intervalos[intervalos["dimensao"].eq("faixa_etaria")]
    assert set(por_idade["grupo"]) == set(ROTULOS_FAIXA_ETARIA)
    assert len(por_idade) == len(ROTULOS_FAIXA_ETARIA) * 7

    print("Avaliação por faixa etária e intervalos de confiança validados.")


if __name__ == "__main__":
    main()

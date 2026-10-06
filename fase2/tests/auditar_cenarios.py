"""Audita cenários sintéticos do front e associações observadas na base.

Este script não altera o modelo. Ele ajuda a verificar se resultados aparentemente
contraintuitivos decorrem dos dados, dos valores padrão ou do pipeline.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd


DIRETORIO_FASE2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DIRETORIO_FASE2 / "src"))

from treinar_baselines import carregar_dados, criar_modelos  # noqa: E402


def registro_base() -> dict[str, object]:
    """Representa aproximadamente o cenário descrito na interface."""
    return {
        "idade": 54,
        "pressao_arterial_repouso": 130.0,
        "colesterol": 245.0,
        "frequencia_cardiaca_maxima": 150.0,
        "depressao_st_exercicio": 1.0,
        "num_vasos_principais": np.nan,
        "sexo": "feminino",
        "tipo_dor_peito": "angina_tipica",
        "acucar_jejum_maior_120": "sim",
        "eletrocardiograma_repouso": "anormalidade_onda_st_t",
        "angina_induzida_exercicio": "nao",
        "inclinacao_st_pico_exercicio": "ascendente",
        "resultado_thal": np.nan,
    }


def criar_cenarios() -> pd.DataFrame:
    base = registro_base()
    cenarios: list[dict[str, object]] = []

    def adicionar(nome: str, **mudancas: object) -> None:
        registro = {**base, **mudancas}
        registro["cenario"] = nome
        cenarios.append(registro)

    adicionar("A — descrição aproximada")
    adicionar(
        "B — com angina no exercício",
        angina_induzida_exercicio="sim",
    )
    adicionar(
        "C — ST mais alterado",
        angina_induzida_exercicio="sim",
        depressao_st_exercicio=2.5,
        inclinacao_st_pico_exercicio="plana",
    )
    adicionar(
        "D — exames adicionais alterados",
        angina_induzida_exercicio="sim",
        depressao_st_exercicio=2.5,
        inclinacao_st_pico_exercicio="plana",
        num_vasos_principais=2.0,
        resultado_thal="defeito_reversivel",
    )
    adicionar(
        "E — assintomático na codificação UCI",
        tipo_dor_peito="assintomatico",
        angina_induzida_exercicio="sim",
        depressao_st_exercicio=2.5,
        inclinacao_st_pico_exercicio="plana",
        num_vasos_principais=2.0,
        resultado_thal="defeito_reversivel",
    )

    return pd.DataFrame(cenarios).set_index("cenario")


def contribuicoes(modelo, registro: pd.DataFrame) -> pd.DataFrame:
    preprocessador = modelo.named_steps["preprocessamento"]
    estimador = modelo.named_steps["modelo"]
    valores = preprocessador.transform(registro)[0]
    nomes = preprocessador.get_feature_names_out()
    pesos = estimador.coef_[0]
    tabela = pd.DataFrame(
        {
            "variavel": [
                nome.replace("numerico__", "").replace("categorico__", "")
                for nome in nomes
            ],
            "valor_transformado": valores,
            "coeficiente": pesos,
            "contribuicao": valores * pesos,
        }
    )
    tabela["magnitude"] = tabela["contribuicao"].abs()
    return tabela.sort_values("magnitude", ascending=False)


def main() -> None:
    atributos, alvo = carregar_dados()
    modelo = criar_modelos()["regressao_logistica"]
    modelo.fit(atributos, alvo)

    cenarios = criar_cenarios()
    probabilidades = modelo.predict_proba(cenarios)[:, 1]
    resultado = pd.DataFrame(
        {
            "cenario": cenarios.index,
            "probabilidade": probabilidades,
        }
    )

    print("=== Probabilidades dos cenários sintéticos ===")
    print(resultado.to_csv(index=False))

    print("=== Maiores contribuições do cenário A ===")
    print(contribuicoes(modelo, cenarios.iloc[[0]]).head(12).to_csv(index=False))

    dados_auditoria = atributos.copy()
    dados_auditoria["alvo"] = alvo.to_numpy()

    print("=== Frequência observada por tipo de dor ===")
    print(
        dados_auditoria.groupby("tipo_dor_peito", dropna=False)["alvo"]
        .agg(["count", "mean"])
        .sort_values("mean", ascending=False)
        .to_csv()
    )

    print("=== Frequência observada por angina induzida por exercício ===")
    print(
        dados_auditoria.groupby("angina_induzida_exercicio", dropna=False)["alvo"]
        .agg(["count", "mean"])
        .sort_values("mean", ascending=False)
        .to_csv()
    )


if __name__ == "__main__":
    main()

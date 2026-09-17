"""Garante que os notebooks entregues exibem resultados sem exigir execução local."""

from __future__ import annotations

import json
from pathlib import Path


FASE2 = Path(__file__).resolve().parents[1]
NOTEBOOKS = {
    "analise_baseline.ipynb": 5,
    "classificacao_textual_tfidf.ipynb": 8,
    "mlp_ecg_binaria.ipynb": 7,
    "mlp_ecg_ampliada.ipynb": 8,
}


def main() -> None:
    for nome, quantidade_esperada in NOTEBOOKS.items():
        caminho = FASE2 / "notebooks" / nome
        notebook = json.loads(caminho.read_text(encoding="utf-8"))
        codigos = [
            celula for celula in notebook["cells"] if celula["cell_type"] == "code"
        ]

        assert len(codigos) == quantidade_esperada, (
            f"{nome}: quantidade inesperada de células de código."
        )
        assert all(celula.get("execution_count") is not None for celula in codigos), (
            f"{nome}: há células sem evidência de execução."
        )
        assert not any(
            saida.get("output_type") == "error"
            for celula in codigos
            for saida in celula.get("outputs", [])
        ), f"{nome}: há erro salvo nas saídas."
        assert sum(len(celula.get("outputs", [])) for celula in codigos) > 0, (
            f"{nome}: nenhuma saída visível foi versionada."
        )

    print("Notebooks versionados com execução e saídas visíveis validadas.")


if __name__ == "__main__":
    main()

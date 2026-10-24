"""Valida a revisão ampliada do experimento visual, sem treinar o modelo."""

from __future__ import annotations

import sys
import json
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image


DIRETORIO_FASE2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DIRETORIO_FASE2 / "src"))

from treinar_mlp_ecg_ampliada import dividir, inventario, modelo, pixels  # noqa: E402


def main() -> None:
    caminho_notebook = DIRETORIO_FASE2 / "notebooks" / "mlp_ecg_ampliada.ipynb"
    notebook = json.loads(caminho_notebook.read_text())
    codigos = [
        "".join(celula["source"])
        for celula in notebook["cells"]
        if celula["cell_type"] == "code"
    ]
    assert any("treinar_mlp_ecg_ampliada" in codigo for codigo in codigos)
    codigo_completo = "\n".join(codigos)
    for etapa in [
        "pixels(dados)",
        "dividir(dados, x)",
        "compute_class_weight",
        "rede.fit",
        "balanced_accuracy_score",
        "confusion_matrix",
    ]:
        assert etapa in codigo_completo, f"Etapa ausente do notebook: {etapa}"
    assert len(codigos) >= 8, "O notebook deve detalhar as etapas em células próprias."
    for indice, codigo in enumerate(codigos):
        compile(codigo, f"celula_{indice}", "exec")

    dados = inventario()
    assert len(dados) == 491
    assert dados["hash_original"].nunique() == 491
    assert dados["hash_derivado"].nunique() == 491
    assert set(dados["alvo"]) == {0, 1}
    assert int((dados["classe_original"] == "normal").sum()) == 142
    assert int((dados["classe_original"] != "normal").sum()) == 349
    for caminho in dados["arquivo"]:
        with Image.open(DIRETORIO_FASE2.parent / caminho) as imagem:
            assert imagem.size == (384, 224)
            assert imagem.mode == "L"
            assert not imagem.getexif(), "O derivado não deve preservar EXIF."

    matriz = pixels(dados)
    assert matriz.shape == (491, 96 * 56)
    assert matriz.dtype == np.float32
    assert 0.0 <= float(matriz.min()) <= float(matriz.max()) <= 1.0

    treino, validacao, teste = dividir(dados, matriz)
    assert len(treino) + len(validacao) + len(teste) == 491
    assert len(teste) == 99
    hashes = [set(dados.iloc[idx]["hash_original"]) for idx in (treino, validacao, teste)]
    assert hashes[0].isdisjoint(hashes[1])
    assert hashes[0].isdisjoint(hashes[2])
    assert hashes[1].isdisjoint(hashes[2])
    for indices in (treino, validacao, teste):
        assert dados.iloc[indices]["classe_original"].nunique() == 4

    rede = modelo(matriz.shape[1])
    assert isinstance(rede, tf.keras.Model)
    assert rede.input_shape == (None, 96 * 56)
    assert rede.output_shape == (None, 1)
    assert any(isinstance(camada, tf.keras.layers.Dropout) for camada in rede.layers)
    print("Revisão visual ampliada, separação e arquitetura validadas.")


if __name__ == "__main__":
    main()

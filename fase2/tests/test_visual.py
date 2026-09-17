"""Valida dados, pré-processamento e arquitetura da MLP visual."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import tensorflow as tf


DIRETORIO_FASE2 = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(DIRETORIO_FASE2 / "src"))

from treinar_mlp_ecg import (  # noqa: E402
    carregar_pixels,
    criar_mlp,
    dividir_dados,
    inventariar_imagens,
)


def main() -> None:
    inventario = inventariar_imagens()
    assert len(inventario) == 60
    assert inventario["hash_sha256"].nunique() == 60
    assert inventario["classe_original"].nunique() == 4
    assert set(inventario["classe_binaria"]) == {"normal", "anormal"}
    assert int((inventario["classe_binaria"] == "normal").sum()) == 30
    assert int((inventario["classe_binaria"] == "anormal").sum()) == 30

    pixels = carregar_pixels(inventario)
    assert pixels.shape == (60, 4096)
    assert pixels.dtype == np.float32
    assert 0.0 <= float(pixels.min()) <= float(pixels.max()) <= 1.0

    (
        x_treino,
        x_teste,
        y_treino,
        y_teste,
        treino_idx,
        teste_idx,
    ) = dividir_dados(inventario, pixels)
    assert len(x_treino) == 48
    assert len(x_teste) == 12
    assert set(inventario.iloc[treino_idx]["hash_sha256"]).isdisjoint(
        set(inventario.iloc[teste_idx]["hash_sha256"])
    )
    assert set(y_treino) == {0, 1}
    assert set(y_teste) == {0, 1}

    modelo = criar_mlp(4096)
    assert isinstance(modelo, tf.keras.Model)
    assert modelo.input_shape == (None, 4096)
    assert modelo.output_shape == (None, 1)
    assert any(
        isinstance(camada, tf.keras.layers.Dropout)
        for camada in modelo.layers
    )
    print("Dados visuais, separação e arquitetura MLP validados.")


if __name__ == "__main__":
    main()

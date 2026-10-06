"""MLP acadêmica para classificação binária de imagens de ECG.

O dataset não fornece identificador de paciente. A separação é feita por exames
deduplicados por hash e essa limitação é registrada explicitamente.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
from pathlib import Path

os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")
os.environ.setdefault("TF_DETERMINISTIC_OPS", "1")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from PIL import Image, ImageOps
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight


SEMENTE = 42
TAMANHO_IMAGEM = (64, 64)
RAIZ_REPOSITORIO = Path(__file__).resolve().parents[2]
DIRETORIO_IMAGENS = RAIZ_REPOSITORIO / "assets" / "imagens" / "ecg"
DIRETORIO_RESULTADOS = RAIZ_REPOSITORIO / "fase2" / "resultados" / "visual"
CLASSE_NORMAL = "normal"


def fixar_sementes() -> None:
    random.seed(SEMENTE)
    np.random.seed(SEMENTE)
    tf.keras.utils.set_random_seed(SEMENTE)


def inventariar_imagens() -> pd.DataFrame:
    linhas = []
    for caminho in sorted(DIRETORIO_IMAGENS.glob("*/*.jpg")):
        classe_original = caminho.parent.name
        linhas.append(
            {
                "caminho": str(caminho),
                "arquivo": caminho.name,
                "classe_original": classe_original,
                "classe_binaria": (
                    "normal" if classe_original == CLASSE_NORMAL else "anormal"
                ),
                "alvo": 0 if classe_original == CLASSE_NORMAL else 1,
                "hash_sha256": hashlib.sha256(caminho.read_bytes()).hexdigest(),
            }
        )
    dados_completos = pd.DataFrame(linhas)
    if len(dados_completos) != 120:
        raise ValueError(
            f"Esperadas 120 imagens; encontradas {len(dados_completos)}."
        )
    if dados_completos["hash_sha256"].duplicated().any():
        raise ValueError("A amostra contém imagens binárias duplicadas.")

    normais = dados_completos[
        dados_completos["classe_binaria"] == "normal"
    ]
    anormais = (
        dados_completos[dados_completos["classe_binaria"] == "anormal"]
        .groupby("classe_original", group_keys=False)
        .sample(n=10, random_state=SEMENTE)
    )
    dados = pd.concat([normais, anormais], ignore_index=True).sample(
        frac=1,
        random_state=SEMENTE,
    ).reset_index(drop=True)
    if dados["classe_binaria"].value_counts().to_dict() != {
        "normal": 30,
        "anormal": 30,
    }:
        raise AssertionError("A amostra binária não ficou equilibrada.")
    return dados


def carregar_pixels(
    inventario: pd.DataFrame,
) -> np.ndarray:
    pixels = []
    for caminho in inventario["caminho"]:
        with Image.open(caminho) as imagem:
            cinza = ImageOps.autocontrast(ImageOps.grayscale(imagem))
            redimensionada = cinza.resize(
                TAMANHO_IMAGEM,
                Image.Resampling.LANCZOS,
            )
            vetor = np.asarray(redimensionada, dtype=np.float32) / 255.0
            vetor = 1.0 - vetor
            pixels.append(vetor.reshape(-1))
    matriz = np.stack(pixels)
    if matriz.shape != (len(inventario), 64 * 64):
        raise AssertionError(f"Formato inesperado: {matriz.shape}")
    return matriz


def aumentar_dados_treino(
    pixels: np.ndarray,
    alvos: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Cria pequenos deslocamentos somente a partir do conjunto de treino."""
    imagens = pixels.reshape(-1, 64, 64)
    lotes = [imagens]
    rotulos = [alvos]
    for deslocamento_linha, deslocamento_coluna in [
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
    ]:
        deslocadas = np.roll(
            imagens,
            shift=(deslocamento_linha, deslocamento_coluna),
            axis=(1, 2),
        )
        if deslocamento_linha == 1:
            deslocadas[:, 0, :] = 0
        elif deslocamento_linha == -1:
            deslocadas[:, -1, :] = 0
        if deslocamento_coluna == 1:
            deslocadas[:, :, 0] = 0
        elif deslocamento_coluna == -1:
            deslocadas[:, :, -1] = 0
        lotes.append(deslocadas)
        rotulos.append(alvos)
    aumentados = np.concatenate(lotes, axis=0).reshape(-1, 4096)
    return aumentados.astype(np.float32), np.concatenate(rotulos)


def selecionar_limiar(
    verdadeiros: np.ndarray,
    probabilidades: np.ndarray,
) -> float:
    """Seleciona na validação o limiar de maior acurácia balanceada."""
    candidatos = np.linspace(0.2, 0.8, 61)
    pontuacoes = [
        balanced_accuracy_score(
            verdadeiros,
            (probabilidades >= limiar).astype(int),
        )
        for limiar in candidatos
    ]
    return float(candidatos[int(np.argmax(pontuacoes))])


def dividir_dados(
    inventario: pd.DataFrame,
    pixels: np.ndarray,
):
    indices = np.arange(len(inventario))
    treino_idx, teste_idx = train_test_split(
        indices,
        test_size=0.2,
        random_state=SEMENTE,
        stratify=inventario["alvo"],
    )
    hashes_treino = set(inventario.iloc[treino_idx]["hash_sha256"])
    hashes_teste = set(inventario.iloc[teste_idx]["hash_sha256"])
    if hashes_treino.intersection(hashes_teste):
        raise AssertionError("Há exame duplicado entre treino e teste.")
    return (
        pixels[treino_idx],
        pixels[teste_idx],
        inventario.iloc[treino_idx]["alvo"].to_numpy(),
        inventario.iloc[teste_idx]["alvo"].to_numpy(),
        treino_idx,
        teste_idx,
    )


def criar_mlp(numero_entradas: int) -> tf.keras.Model:
    modelo = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(numero_entradas,)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.35),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ],
        name="mlp_ecg_binaria",
    )
    modelo.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        loss="binary_crossentropy",
        metrics=[
            "accuracy",
            tf.keras.metrics.Precision(name="precision"),
            tf.keras.metrics.Recall(name="recall"),
            tf.keras.metrics.AUC(name="auc"),
        ],
    )
    return modelo


def treinar_mlp(epocas: int = 40):
    fixar_sementes()
    inventario = inventariar_imagens()
    pixels = carregar_pixels(inventario)
    (
        x_treino,
        x_teste,
        y_treino,
        y_teste,
        treino_idx,
        teste_idx,
    ) = dividir_dados(inventario, pixels)

    (
        x_ajuste,
        x_validacao,
        y_ajuste,
        y_validacao,
    ) = train_test_split(
        x_treino,
        y_treino,
        test_size=0.25,
        random_state=SEMENTE,
        stratify=y_treino,
    )
    x_ajuste_aumentado, y_ajuste_aumentado = aumentar_dados_treino(
        x_ajuste,
        y_ajuste,
    )
    classes = np.unique(y_ajuste_aumentado)
    pesos = compute_class_weight(
        class_weight="balanced",
        classes=classes,
        y=y_ajuste_aumentado,
    )
    pesos_classe = {
        int(classe): float(peso)
        for classe, peso in zip(classes, pesos, strict=True)
    }

    modelo = criar_mlp(x_treino.shape[1])
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=7,
            restore_best_weights=True,
        )
    ]
    historico = modelo.fit(
        x_ajuste_aumentado,
        y_ajuste_aumentado,
        validation_data=(x_validacao, y_validacao),
        epochs=epocas,
        batch_size=8,
        class_weight=pesos_classe,
        callbacks=callbacks,
        verbose=0,
        shuffle=True,
    )

    probabilidades_validacao = modelo.predict(
        x_validacao,
        verbose=0,
    ).reshape(-1)
    limiar = selecionar_limiar(y_validacao, probabilidades_validacao)
    probabilidades = modelo.predict(x_teste, verbose=0).reshape(-1)
    previsoes = (probabilidades >= limiar).astype(int)
    metricas = {
        "limiar_selecionado_na_validacao": limiar,
        "n_ajuste_apos_aumento": int(len(y_ajuste_aumentado)),
        "acuracia": float(accuracy_score(y_teste, previsoes)),
        "acuracia_balanceada": float(
            balanced_accuracy_score(y_teste, previsoes)
        ),
        "precisao_anormal": float(
            precision_score(y_teste, previsoes, zero_division=0)
        ),
        "recall_anormal": float(
            recall_score(y_teste, previsoes, zero_division=0)
        ),
        "f1_anormal": float(f1_score(y_teste, previsoes, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_teste, probabilidades)),
        "n_treino": int(len(y_treino)),
        "n_teste": int(len(y_teste)),
        "epocas_executadas": int(len(historico.history["loss"])),
        "relatorio": classification_report(
            y_teste,
            previsoes,
            target_names=["normal", "anormal"],
            output_dict=True,
            zero_division=0,
        ),
    }
    previsoes_df = inventario.iloc[teste_idx][
        ["arquivo", "classe_original", "classe_binaria", "hash_sha256"]
    ].copy()
    previsoes_df["probabilidade_anormal"] = probabilidades
    previsoes_df["predicao"] = np.where(previsoes == 1, "anormal", "normal")
    return modelo, historico, inventario, metricas, previsoes_df, y_teste, previsoes


def salvar_resultados() -> dict[str, object]:
    (
        modelo,
        historico,
        inventario,
        metricas,
        previsoes,
        y_teste,
        y_predito,
    ) = treinar_mlp()
    DIRETORIO_RESULTADOS.mkdir(parents=True, exist_ok=True)

    payload = {
        "modelo": "MLP Keras binária",
        "entrada": "ECG 64x64 em tons de cinza, achatado em 4096 pixels",
        "classes": {"normal": 0, "anormal": 1},
        "metricas": metricas,
        "governanca": {
            "imagens_duplicadas": 0,
            "separacao": "estratificada por exame único após deduplicação",
            "identificador_paciente_disponivel": False,
            "limitacao": (
                "A fonte não fornece ID de paciente; não é possível garantir "
                "separação por indivíduo."
            ),
            "prevalencia": (
                "A fonte curada tem 30 imagens por classe original; a amostra "
                "binária usa 30 normais e 30 anormais e não representa prevalência clínica."
            ),
        },
    }
    (DIRETORIO_RESULTADOS / "metricas_mlp_ecg.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    inventario.to_csv(DIRETORIO_RESULTADOS / "inventario_binario.csv", index=False)
    previsoes.to_csv(DIRETORIO_RESULTADOS / "previsoes_mlp_ecg.csv", index=False)
    modelo.save(DIRETORIO_RESULTADOS / "modelo_mlp_ecg.keras")

    pd.DataFrame(historico.history).plot(
        y=["loss", "val_loss"],
        title="Perda durante o treinamento",
    )
    plt.xlabel("Época")
    plt.ylabel("Binary cross-entropy")
    plt.tight_layout()
    plt.savefig(DIRETORIO_RESULTADOS / "curva_perda_mlp.png", dpi=160)
    plt.close()

    matriz = confusion_matrix(y_teste, y_predito, labels=[0, 1])
    fig, eixo = plt.subplots()
    eixo.imshow(matriz, cmap="RdPu")
    eixo.set(
        xticks=[0, 1],
        yticks=[0, 1],
        xticklabels=["Normal", "Anormal"],
        yticklabels=["Normal", "Anormal"],
        xlabel="Predição",
        ylabel="Real",
        title="Matriz de confusão — MLP de ECG",
    )
    for linha in range(2):
        for coluna in range(2):
            eixo.text(coluna, linha, matriz[linha, coluna], ha="center", va="center")
    fig.tight_layout()
    fig.savefig(DIRETORIO_RESULTADOS / "matriz_confusao_mlp.png", dpi=160)
    plt.close(fig)
    return payload


def main() -> None:
    print(json.dumps(salvar_resultados(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

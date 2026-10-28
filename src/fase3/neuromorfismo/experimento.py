"""Comparamos representações estatísticas e uma rede LIF em sinais sintéticos.

Não utilizamos dados de pacientes, diagnóstico ou dados de teste no ajuste.
A rede LIF é um reservatório fixo; treinamos somente sua leitura logística.
"""
from __future__ import annotations

import hashlib
import json
import platform
from importlib.metadata import version
from pathlib import Path
from time import perf_counter

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, balanced_accuracy_score, confusion_matrix,
                             f1_score, precision_score, recall_score, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from threadpoolctl import threadpool_limits

CLASSES = ["regular_simulado", "oscilante_simulado"]
SEED = 42
N_SESSIONS = 240
SAMPLES = 120
WINDOW = 24
STRIDE = 12
SAMPLE_SECONDS = 5
C_GRID = [0.01, 0.1, 1.0, 10.0]


def gerar_sessoes(seed=SEED, n=N_SESSIONS):
    """Rótulo identifica o regime do gerador, não uma doença nem um limiar.

    As duas classes compartilham frequência média, ruído e deriva; a classe 1
    recebe oscilação mais rápida. A classe 0 também oscila, mais lentamente.
    Geramos sessões inteiras antes de qualquer recorte ou divisão em janelas.
    """
    if n < 40 or n % 2:
        raise ValueError("Utilizar um número par de pelo menos 40 sessões.")
    rng = np.random.default_rng(seed)
    labels = np.repeat([0, 1], n // 2)
    rng.shuffle(labels)
    t = np.arange(SAMPLES, dtype=float)
    series = []
    for label in labels:
        baseline = rng.uniform(65, 110)
        phase = rng.uniform(0, 2 * np.pi)
        noise = rng.normal(0, rng.uniform(2, 5), SAMPLES)
        drift = np.cumsum(rng.normal(0, 0.28, SAMPLES))
        period = rng.uniform(9, 18) if label else rng.uniform(35, 65)
        amplitude = rng.uniform(6, 17)
        signal = baseline + drift + amplitude * np.sin(2 * np.pi * t / period + phase) + noise
        series.append(np.clip(signal, 35, 180))
    return np.asarray(series), labels.astype(int)


def dividir_sessoes(labels, seed=SEED):
    """60/20/20 estratificado por sessão; não fazemos split de janelas."""
    ids = np.arange(len(labels))
    train, rest = train_test_split(ids, test_size=0.4, stratify=labels, random_state=seed)
    valid, test = train_test_split(rest, test_size=0.5, stratify=labels[rest], random_state=seed)
    return {"treino": np.sort(train), "validacao": np.sort(valid), "teste": np.sort(test)}


def criar_janelas(series, labels, ids):
    x, y, groups, starts = [], [], [], []
    for sid in ids:
        for start in range(0, SAMPLES - WINDOW + 1, STRIDE):
            x.append(series[sid, start:start + WINDOW])
            y.append(labels[sid])
            groups.append(sid)
            starts.append(start)
    return np.asarray(x), np.asarray(y), np.asarray(groups), np.asarray(starts)


def atributos_tradicionais(x):
    """Incluímos características temporais, além da média e dispersão."""
    diff = np.diff(x, axis=1)
    centered = x - x.mean(axis=1, keepdims=True)
    lag = np.sum(centered[:, :-1] * centered[:, 1:], axis=1)
    lag /= np.maximum(np.sum(centered ** 2, axis=1), 1e-9)
    return np.column_stack([x.mean(1), x.std(1), x.min(1), x.max(1),
                            np.sqrt(np.mean(diff ** 2, axis=1)),
                            np.mean(np.abs(diff), axis=1), lag,
                            x[:, -1] - x[:, 0]])


class RedeLIF:
    """24 neurônios recorrentes com fuga, limiar, reset e refratariedade.

    Euler: v[t+1] = v[t] + dt/tau * (-v[t] + I[t]).
    dt=1 ms, tau=10 ms, limiar=1, reset=0 e refratário=2 ms.
    Cada leitura IoT (5 s) vira 20 passos neurais (20 ms): escalas distintas.
    A normalização da corrente é ajustada exclusivamente nas janelas de treino.
    Pesos aleatórios fixos, sem STDP/backprop; readout supervisionado externo.
    Reiniciamos o estado entre janelas, sem carregar estado entre sessões.
    """
    def __init__(self, seed=SEED, neurons=24):
        self.neurons = neurons
        rng = np.random.default_rng(seed)
        self.win = rng.uniform(-0.5, 1.4, (4, neurons))
        self.bias = rng.uniform(0.45, 1.25, neurons)
        self.wrec = rng.normal(0, 0.15, (neurons, neurons))
        self.wrec *= rng.random((neurons, neurons)) < 0.15
        np.fill_diagonal(self.wrec, 0)

    def fit(self, x):
        self.mean = float(x.mean())
        self.scale = max(float(x.std()), 1e-8)
        self.diff_scale = max(float(np.diff(x, axis=1).std()), 1e-8)
        return self

    def transform(self, x, trace=False):
        z = np.clip((x - self.mean) / self.scale, -4, 4)
        delta = np.clip(np.diff(x, axis=1, prepend=x[:, :1]) / self.diff_scale, -4, 4)
        inputs = np.stack([np.maximum(z, 0), np.maximum(-z, 0),
                           np.maximum(delta, 0), np.maximum(-delta, 0)], axis=2)
        currents = self.bias + inputs @ self.win
        v = np.zeros((len(x), self.neurons))
        refractory = np.zeros_like(v, dtype=int)
        spikes = np.zeros_like(v)
        bins = np.zeros((len(x), 4, self.neurons))
        history_v, history_s = [], []
        for sample in range(x.shape[1]):
            for _ in range(20):
                free = refractory == 0
                refractory = np.maximum(refractory - 1, 0)
                current = currents[:, sample] + spikes @ self.wrec.T
                v = np.where(free, v + 0.1 * (-v + current), 0)
                spikes = ((v >= 1) & free).astype(float)
                if trace:
                    history_v.append(v[0].copy())
                    history_s.append(spikes[0].copy())
                v = np.where(spikes > 0, 0, v)
                refractory = np.where(spikes > 0, 2, refractory)
                bins[:, sample * 4 // x.shape[1]] += spikes
        # Quatro blocos de 120 ms e potencial final: 5 x 24 = 120 atributos.
        features = np.concatenate([bins.reshape(len(x), -1) / 120, v], axis=1)
        if trace:
            return features, np.asarray(history_v), np.asarray(history_s)
        return features


def agregar_sessoes(y, probabilities, groups):
    ids = np.unique(groups)
    labels = np.asarray([y[groups == sid][0] for sid in ids])
    p = np.asarray([probabilities[groups == sid].mean() for sid in ids])
    return ids, labels, p


def metricas(y, p):
    pred = p >= 0.5
    return {"acuracia": float(accuracy_score(y, pred)),
            "acuracia_balanceada": float(balanced_accuracy_score(y, pred)),
            "f1_macro": float(f1_score(y, pred, average="macro", zero_division=0)),
            "precisao_classe1": float(precision_score(y, pred, zero_division=0)),
            "recall_classe1": float(recall_score(y, pred, zero_division=0)),
            "roc_auc": float(roc_auc_score(y, p)),
            "matriz_confusao": confusion_matrix(y, pred, labels=[0, 1]).tolist()}


def ajustar_readout(x, y, xv, yv, gv):
    candidates = []
    best, score = None, -1.0
    for c in C_GRID:
        pipeline = make_pipeline(StandardScaler(), LogisticRegression(C=c, max_iter=1000, random_state=SEED))
        pipeline.fit(x, y)
        _, sy, sp = agregar_sessoes(yv, pipeline.predict_proba(xv)[:, 1], gv)
        value = f1_score(sy, sp >= 0.5, average="macro", zero_division=0)
        candidates.append({"C": c, "f1_macro_validacao_sessoes": float(value)})
        if value > score:  # Empate mantém o primeiro C, mais regularizado.
            best, score = pipeline, value
    return best, candidates


def intervalo_pareado(y, pa, pb, seed):
    """Bootstrap estratificado de sessões (não janelas sobrepostas), 2.000 réplicas."""
    rng = np.random.default_rng(seed)
    classes = [np.flatnonzero(y == k) for k in [0, 1]]
    values = []
    for _ in range(2000):
        idx = np.concatenate([rng.choice(ids, len(ids), replace=True) for ids in classes])
        # Classes balanceadas: acurácia = acurácia balanceada nesta reamostragem.
        a = np.mean((pa[idx] >= 0.5) == y[idx])
        b = np.mean((pb[idx] >= 0.5) == y[idx])
        values.append([a, b, b - a])
    q = np.quantile(values, [0.025, 0.975], axis=0)
    return dict(zip(["tradicional", "lif", "diferenca_lif_menos_tradicional"], q.T.tolist()))


def salvar_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def executar(saida, seed=SEED):
    """Executamos protocolo fixo; C é escolhido em validação, teste fica separado."""
    with threadpool_limits(limits=1):
        return _executar(Path(saida), seed)


def _executar(out, seed):
    out.mkdir(parents=True, exist_ok=True)
    series, labels = gerar_sessoes(seed)
    splits = dividir_sessoes(labels, seed)
    windows = {key: criar_janelas(series, labels, ids) for key, ids in splits.items()}
    xt, yt, _, _ = windows["treino"]
    xv, yv, gv, _ = windows["validacao"]
    xe, ye, ge, starts = windows["teste"]
    results, session_preds, window_preds = {}, {}, {}
    lif = RedeLIF(seed).fit(xt)
    for name, transform in [("tradicional", atributos_tradicionais), ("lif", lif.transform)]:
        start = perf_counter()
        ft, fv = transform(xt), transform(xv)
        model, candidates = ajustar_readout(ft, yt, fv, yv, gv)
        fit_time = perf_counter() - start
        # Somente agora calculamos a representação e a previsão do teste.
        start = perf_counter()
        fe = transform(xe)
        pe = model.predict_proba(fe)[:, 1]
        predict_time = perf_counter() - start
        ids, sy, sp = agregar_sessoes(ye, pe, ge)
        session_preds[name], window_preds[name] = sp, pe
        results[name] = {"sessoes": metricas(sy, sp), "janelas": metricas(ye, pe),
                         "C_escolhido": float(model[-1].C), "busca_validacao": candidates,
                         "atributos": int(ft.shape[1]), "ajuste_com_transformacao_s": fit_time,
                         "previsao_com_transformacao_s": predict_time,
                         "erros_sessoes": ids[(sp >= 0.5) != sy].tolist()}
    digest = hashlib.sha256(series.astype("<f8").tobytes() + labels.astype("<i8").tobytes()).hexdigest()
    summary = {"seed": seed, "origem": "sintetica; sem pacientes e sem diagnostico",
               "sha256_sinais_rotulos": digest, "classes": CLASSES,
               "protocolo": {"sessoes": N_SESSIONS, "amostras_por_sessao": SAMPLES,
                              "intervalo_s": SAMPLE_SECONDS, "janela_amostras": WINDOW,
                              "passo_amostras": STRIDE, "fronteira_decisao": 0.5,
                              "agregacao_sessao": "media das probabilidades das nove janelas",
                              "particoes_sessoes": {k: len(v) for k, v in splits.items()},
                              "particoes_janelas": {k: len(v[0]) for k, v in windows.items()}},
               "lif": {"neuronios": 24, "dt_ms": 1, "tau_ms": 10, "passos_por_leitura": 20,
                       "limiar": 1, "reset": 0, "refratario_ms": 2,
                       "normalizacao_treino": {"media": lif.mean, "desvio": lif.scale,
                                                "desvio_diferencas": lif.diff_scale},
                       "pesos": "fixos pela semente; somente readout logistico treinado"},
               "modelos": results,
               "ic95_bootstrap_sessoes": intervalo_pareado(sy, session_preds["tradicional"], session_preds["lif"], seed),
               "ambiente": {"python": platform.python_version(), "sistema": platform.system(),
                            **{m: version(m) for m in ["numpy", "scipy", "scikit-learn", "matplotlib"]}},
               "limites": ["Rotulos do regime gerador; nao sao arritmia ou diagnostico.",
                            "Mesma media de BPM pode pertencer a ambas as classes.",
                            "Janelas da mesma sessao se sobrepoem; metricas principais sao por sessao.",
                            "Tempos de uma execucao em CPU, sem benchmark energetico ou de hardware.",
                            "Comparacao de pipelines: 8 atributos tradicionais versus 120 LIF.",
                            "Nao treinamos pesos internos nem validamos em pacientes reais."]}
    predictions = {"sessoes": [{"sessao": int(sid), "rotulo": int(label),
                                **{name: float(session_preds[name][i]) for name in results}}
                               for i, (sid, label) in enumerate(zip(ids, sy))],
                   "janelas": [{"sessao": int(sid), "inicio_amostra": int(starts[i]), "rotulo": int(ye[i]),
                                **{name: float(window_preds[name][i]) for name in results}}
                               for i, sid in enumerate(ge)]}
    salvar_json(out / "metricas.json", summary)
    salvar_json(out / "divisao.json", {k: v.tolist() for k, v in splits.items()})
    salvar_json(out / "previsoes_teste.json", predictions)
    gerar_figuras(out, series, labels, splits, lif, summary)
    return summary


def gerar_figuras(out, series, labels, splits, lif, summary):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
    ids = [next(int(sid) for sid in splits["teste"] if labels[sid] == c) for c in [0, 1]]
    fig, axes = plt.subplots(2, 1, figsize=(9, 4.8), sharex=True, constrained_layout=True)
    for c, ax in enumerate(axes):
        ax.plot(np.arange(SAMPLES) * SAMPLE_SECONDS, series[ids[c]], color=["#218577", "#ed145b"][c])
        ax.set(title=f"Sessão {ids[c]}: {CLASSES[c]}", ylabel="BPM artificial")
    axes[-1].set_xlabel("Tempo simulado da série (s)")
    fig.savefig(out / "series.png", dpi=150)
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.6), constrained_layout=True)
    for name, ax in zip(["tradicional", "lif"], axes):
        cm = np.asarray(summary["modelos"][name]["sessoes"]["matriz_confusao"])
        ax.imshow(cm, cmap="Blues", vmin=0, vmax=len(splits["teste"]) // 2)
        for row in range(2):
            for col in range(2):
                ax.text(col, row, str(cm[row, col]), ha="center", va="center", fontsize=15,
                        color="white" if cm[row, col] > 12 else "#183247")
        ax.set(title=name + " - teste por sessão", xlabel="Predito", ylabel="Real",
               xticks=[0, 1], yticks=[0, 1], xticklabels=["regular", "oscilante"], yticklabels=["regular", "oscilante"])
    fig.savefig(out / "matrizes_confusao.png", dpi=150)
    plt.close(fig)
    _, potentials, spikes = lif.transform(series[ids[1]:ids[1] + 1, :WINDOW], trace=True)
    fig, axes = plt.subplots(2, 1, figsize=(9, 4.5), sharex=True, constrained_layout=True)
    axes[0].plot(potentials[:, 0], color="#218577", label="Neurônio 0: potencial antes do reset")
    axes[0].axhline(1, color="#ed145b", linestyle="--", label="Limiar")
    axes[0].legend(fontsize=8)
    steps, neurons = np.nonzero(spikes)
    axes[1].scatter(steps, neurons, s=4, color="#183247")
    axes[1].set(ylabel="Neurônio", xlabel="Tempo do modelo LIF (ms); 20 ms representam cada leitura de 5 s")
    fig.savefig(out / "atividade_lif.png", dpi=150)
    plt.close(fig)

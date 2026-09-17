"""Sondagem sintética de linguagem, separada do treinamento e da métrica original."""
import json
from pathlib import Path

import pandas as pd

from classificar_risco_texto import probabilidade_alto_risco, treinar_e_avaliar


CASOS = [
    ("afirmacao", "Tenho dor no peito e falta de ar."),
    ("negacao", "Não tenho dor no peito nem falta de ar."),
    ("contraste", "Não tenho febre, mas sinto dor no peito e falta de ar."),
    ("historico", "Há dez anos tive dor no peito; hoje estou sem sintomas."),
    ("terceiro", "Meu vizinho teve dor no peito; eu estou bem."),
    ("hipotese", "Se eu tivesse dor no peito, o que aconteceria?"),
    ("maiusculas", "TENHO DOR NO PEITO E FALTA DE AR."),
    ("pontuacao", "Tenho dor no peito! E falta de ar!"),
    ("sem_acentos", "Sinto pressao no torax e nauseas."),
    ("parafrase", "Parece que estão apertando meu peito e está difícil puxar o ar."),
    ("vago", "Estou estranho hoje."),
    ("fora_dominio", "Preciso trocar a senha do computador."),
    ("desconhecido", "xyzqwerty zzzqwerty"),
    ("vazio", ""),
    ("espacos", "   "),
    ("leve", "Depois de digitar a tarde inteira meu punho ficou um pouco dolorido."),
]


def avaliar():
    modelo, *_ = treinar_e_avaliar()
    linhas = []
    for categoria, frase in CASOS:
        vetor = modelo.named_steps["tfidf"].transform([frase])
        linhas.append(
            {
                "categoria": categoria,
                "frase": frase,
                "predicao": str(modelo.predict([frase])[0]),
                "probabilidade_alto_risco": float(
                    probabilidade_alto_risco(modelo, [frase])[0]
                ),
                "termos_reconhecidos": int(vetor.nnz),
            }
        )
    tabela = pd.DataFrame(linhas)
    base = linhas[0]["probabilidade_alto_risco"]
    resumo = {
        "n_casos": len(linhas),
        "diferenca_afirmacao_negacao": (
            base - linhas[1]["probabilidade_alto_risco"]
        ),
        "diferenca_caixa": abs(base - linhas[6]["probabilidade_alto_risco"]),
        "entradas_sem_vocabulario": int((tabela.termos_reconhecidos == 0).sum()),
        "limite": (
            "Sondagem simulada sem rótulos clínicos; não é acurácia externa. "
            "O estimador binário sempre produz uma classe, inclusive sem evidência textual."
        ),
    }
    return tabela, resumo


if __name__ == "__main__":
    tabela, resumo = avaliar()
    destino = Path(__file__).resolve().parents[1] / "resultados/nlp/revisao"
    destino.mkdir(parents=True, exist_ok=True)
    tabela.to_csv(destino / "sondagem_linguagem.csv", index=False)
    (destino / "resumo_sondagem.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2)
    )
    print(json.dumps(resumo, ensure_ascii=False, indent=2))

"""
Converte o dataset bruto UCI Heart Disease (Cleveland) em CSV com cabeçalho
e valores categóricos legíveis, sem alterar o arquivo original em
assets/dados/raw/.

Fonte original: assets/dados/raw/heart+disease/processed.cleveland.data
Saída: assets/dados/processed/heart_disease_cleveland.csv
"""

import csv
from pathlib import Path

RAW_PATH = Path("assets/dados/raw/heart+disease/processed.cleveland.data")
OUT_PATH = Path("assets/dados/processed/heart_disease_cleveland.csv")

COLUNAS = [
    "idade",
    "sexo",
    "tipo_dor_peito",
    "pressao_arterial_repouso",
    "colesterol",
    "acucar_jejum_maior_120",
    "eletrocardiograma_repouso",
    "frequencia_cardiaca_maxima",
    "angina_induzida_exercicio",
    "depressao_st_exercicio",
    "inclinacao_st_pico_exercicio",
    "num_vasos_principais",
    "resultado_thal",
    "diagnostico_doenca_cardiaca",
]

MAPA_SEXO = {"1.0": "masculino", "0.0": "feminino"}
MAPA_TIPO_DOR = {
    "1.0": "angina_tipica",
    "2.0": "angina_atipica",
    "3.0": "dor_nao_anginosa",
    "4.0": "assintomatico",
}
MAPA_BOOL = {"1.0": "sim", "0.0": "nao"}
MAPA_ECG = {"0.0": "normal", "1.0": "anormalidade_onda_st_t", "2.0": "hipertrofia_ventricular_esquerda"}
MAPA_INCLINACAO = {"1.0": "ascendente", "2.0": "plana", "3.0": "descendente"}
MAPA_THAL = {"3.0": "normal", "6.0": "defeito_fixo", "7.0": "defeito_reversivel"}


def traduzir_linha(campos):
    idade, sexo, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, num = campos

    diagnostico = "ausente" if num == "0" else "presente"

    return [
        str(int(float(idade))),
        MAPA_SEXO.get(sexo, sexo),
        MAPA_TIPO_DOR.get(cp, cp),
        trestbps,
        chol,
        MAPA_BOOL.get(fbs, fbs),
        MAPA_ECG.get(restecg, restecg),
        thalach,
        MAPA_BOOL.get(exang, exang),
        oldpeak,
        MAPA_INCLINACAO.get(slope, slope),
        ca if ca != "?" else "ausente",
        MAPA_THAL.get(thal, "ausente" if thal == "?" else thal),
        diagnostico,
    ]


def main():
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with RAW_PATH.open(encoding="utf-8") as f_in, OUT_PATH.open("w", newline="", encoding="utf-8") as f_out:
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        writer.writerow(COLUNAS)

        total = 0
        for linha in reader:
            if not linha:
                continue
            writer.writerow(traduzir_linha(linha))
            total += 1

    print(f"Linhas processadas: {total}")
    print(f"Arquivo gerado em: {OUT_PATH}")


if __name__ == "__main__":
    main()

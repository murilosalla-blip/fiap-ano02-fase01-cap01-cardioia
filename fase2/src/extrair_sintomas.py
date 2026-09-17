"""Extração acadêmica de sintomas baseada em mapa de conhecimento.

O módulo trabalha apenas com frases simuladas e associações didáticas. As saídas
não são diagnósticos e não devem orientar decisões de saúde.
"""

from __future__ import annotations

import csv
import re
import unicodedata
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


RAIZ_FASE2 = Path(__file__).resolve().parents[1]
CAMINHO_RELATOS = RAIZ_FASE2 / "dados" / "relatos_sintomas.txt"
CAMINHO_MAPA = RAIZ_FASE2 / "dados" / "mapa_conhecimento.csv"


@dataclass(frozen=True)
class Associacao:
    sintomas: tuple[str, ...]
    doenca: str
    prioridade: str


def normalizar_texto(texto: str) -> str:
    """Remove diferenças de caixa, acentuação e pontuação."""
    sem_acentos = "".join(
        caractere
        for caractere in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(caractere)
    )
    minusculo = sem_acentos.lower()
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", minusculo)).strip()


def carregar_mapa(caminho: Path = CAMINHO_MAPA) -> list[Associacao]:
    """Carrega e valida o mapa de conhecimento."""
    with caminho.open(encoding="utf-8", newline="") as arquivo:
        linhas = list(csv.DictReader(arquivo))

    colunas = {"sintoma_1", "sintoma_2", "doenca_associada", "nivel_prioridade"}
    if not linhas or not colunas.issubset(linhas[0]):
        raise ValueError("Mapa de conhecimento vazio ou com colunas inválidas.")

    associacoes: list[Associacao] = []
    for linha in linhas:
        sintomas = tuple(
            sintoma.strip()
            for sintoma in (linha["sintoma_1"], linha["sintoma_2"])
            if sintoma.strip()
        )
        if not sintomas or not linha["doenca_associada"].strip():
            raise ValueError("O mapa contém associação sem sintoma ou doença.")
        associacoes.append(
            Associacao(
                sintomas=sintomas,
                doenca=linha["doenca_associada"].strip(),
                prioridade=linha["nivel_prioridade"].strip(),
            )
        )
    return associacoes


def mencoes_afirmadas(relato: str, sintoma: str) -> bool:
    """Heurística local de negação; não interpreta temporalidade ou terceiros.

    Pontuação e adversativas encerram o escopo. Um novo verbo afirmativo
    após uma conjunção também encerra a negação. Listas com 'nem' mantêm
    o escopo. Casos complexos continuam exigindo revisão humana.
    """
    partes = re.split(r"[.!?;,\n]+", relato)
    padrao = r"\b" + re.escape(normalizar_texto(sintoma)) + r"\b"
    for parte in partes:
        texto = normalizar_texto(parte)
        oracoes = re.split(
            r"\b(?:mas|porem|contudo|entretanto)\b|"
            r"\be\s+(?=(?:sinto|tenho|apresento|percebo|noto)\b)", texto
        )
        for oracao in oracoes:
            for ocorrencia in re.finditer(padrao, oracao):
                prefixo = oracao[:ocorrencia.start()]
                prefixo = re.sub(r"\bnao\s+(?:so|apenas|somente)\b", "", prefixo)
                negado = re.search(
                    r"\b(?:sem|nego|nega|negou|nunca|nem|ausencia de)\b|"
                    r"\bnao\s+(?:tenho|tem|sinto|sente|apresento|apresenta|"
                    r"percebo|percebe|ha|houve|tive|teve|relato|relata)\b", prefixo
                )
                if not negado:
                    return True
    return False


def analisar_relato(
    relato: str,
    associacoes: list[Associacao] | None = None,
) -> dict[str, object]:
    """Identifica expressões e hipóteses associadas a um relato."""
    if not relato.strip():
        raise ValueError("O relato não pode estar vazio.")

    mapa = associacoes if associacoes is not None else carregar_mapa()
    achados: dict[str, dict[str, object]] = defaultdict(
        lambda: {"expressoes": set(), "prioridades": set()}
    )

    for associacao in mapa:
        for sintoma in associacao.sintomas:
            if mencoes_afirmadas(relato, sintoma):
                achados[associacao.doenca]["expressoes"].add(sintoma)
                achados[associacao.doenca]["prioridades"].add(
                    associacao.prioridade
                )

    ordem_prioridade = {"alta": 0, "moderada": 1, "baixa": 2}
    hipoteses = []
    for doenca, detalhes in achados.items():
        prioridades = sorted(
            detalhes["prioridades"],
            key=lambda item: ordem_prioridade.get(item, 99),
        )
        expressoes = sorted(detalhes["expressoes"])
        hipoteses.append(
            {
                "doenca_associada": doenca,
                "prioridade_no_mapa": prioridades[0],
                "sintomas_identificados": expressoes,
                "quantidade_correspondencias": len(expressoes),
            }
        )

    hipoteses.sort(
        key=lambda item: (
            ordem_prioridade.get(str(item["prioridade_no_mapa"]), 99),
            -int(item["quantidade_correspondencias"]),
            str(item["doenca_associada"]),
        )
    )

    return {
        "relato": relato.strip(),
        "sintomas_identificados": sorted(
            {
                sintoma
                for hipotese in hipoteses
                for sintoma in hipotese["sintomas_identificados"]
            }
        ),
        "hipoteses_associadas": hipoteses,
        "encontrou_correspondencia": bool(hipoteses),
        "aviso": (
            "Associação acadêmica baseada em palavras-chave; não é diagnóstico."
        ),
    }


def carregar_relatos(caminho: Path = CAMINHO_RELATOS) -> list[str]:
    relatos = [
        linha.strip()
        for linha in caminho.read_text(encoding="utf-8").splitlines()
        if linha.strip()
    ]
    if len(relatos) != 10:
        raise ValueError(
            f"Esperados exatamente 10 relatos; encontrados {len(relatos)}."
        )
    return relatos


def analisar_arquivo() -> list[dict[str, object]]:
    mapa = carregar_mapa()
    return [analisar_relato(relato, mapa) for relato in carregar_relatos()]


def main() -> None:
    for indice, resultado in enumerate(analisar_arquivo(), start=1):
        nomes = [
            str(item["doenca_associada"])
            for item in resultado["hipoteses_associadas"]
        ]
        sugestoes = ", ".join(nomes) if nomes else "nenhuma associação"
        print(f"{indice:02d}. {sugestoes}")
        print(
            "    Sintomas: "
            + (", ".join(resultado["sintomas_identificados"]) or "não identificados")
        )
    print("\nUso exclusivamente educacional; as saídas não são diagnósticos.")


if __name__ == "__main__":
    main()

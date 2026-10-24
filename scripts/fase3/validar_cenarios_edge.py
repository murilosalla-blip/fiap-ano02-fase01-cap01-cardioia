"""Confere as evidências reais dos cenários ampliados executados no Wokwi.

Não gera leituras: lê os registros de interface e valida as mensagens capturadas.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2] / "src/fase3"


def require(condition: bool, description: str) -> None:
    if not condition:
        raise ValueError(description)


def check_evidence(folder: Path) -> dict:
    def read(name: str) -> str:
        return (folder / name).read_text(encoding="utf-8")

    offline = read("fila_cheia_offline.txt")
    recovery = read("fila_cheia_recuperacao.txt")
    before = read("antes_reinicio.txt")
    after = read("apos_reinicio.txt")
    restored = read("capacidade_restaurada.txt")
    rows = [json.loads(line.strip()) for line in recovery.splitlines()
            if line.lstrip().startswith("{")]
    schema = json.loads((ROOT.parents[1] / "config/fase3/contratos/telemetria.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    for row in rows:
        validator.validate(row)
        expected_bpm = row["pulse_count"] * 60000 / row["window_ms"]
        require(abs(row["heart_rate_bpm"] - expected_bpm) <= 0.011,
                "BPM incompatível com pulsos e duração da janela")

    require("capacidade=3" in offline, "Teste não usou fila reduzida")
    require("coleta seq=4 fila=3 perdas=1 resultado=fila_cheia" in offline,
            "Não há evidência do descarte da quarta leitura")
    require(not any(line.lstrip().startswith("{") for line in offline.splitlines()),
            "Houve envio durante o cenário inicial offline")
    sequences = [row["sequence"] for row in rows]
    require(sequences[:4] == [1, 2, 3, 7], "Pendências não foram preservadas em FIFO")
    require(all(a < b for a, b in zip(sequences, sequences[1:])),
            "Mensagens repetidas ou fora de ordem")
    require(all(row["dropped_total"] == 3 for row in rows),
            "Contagem de perdas diferente da observada antes da recuperação")
    require(sum(row["pulse_count"] for row in rows) == 1,
            "Botão segurado produziu contagem diferente de um pulso")
    require(all(1 <= row["backlog_samples"] <= 3 for row in rows),
            "Backlog excedeu a capacidade do teste")

    def session(text: str) -> str:
        match = re.search(r"# sessao=([a-f0-9]{16}) capacidade=", text)
        require(match is not None, "Sessão ausente no registro de inicialização")
        return match.group(1)

    old_session, new_session = session(before), session(after)
    require(old_session != new_session, "Reinício não alterou a sessão")
    require("coleta seq=14 fila=3 perdas=3 resultado=armazenada" in before,
            "Não há evidência das três pendências anteriores ao reinício")
    require("coleta seq=1 fila=1 perdas=0 resultado=armazenada" in after,
            "Sequência, fila ou perdas não reiniciaram como esperado")
    require("coleta seq=2 fila=2 perdas=0 resultado=armazenada" in after,
            "Coleta não continuou após o reinício")
    require(old_session not in after, "Registro posterior ainda contém a sessão anterior")
    require("capacidade=2000" in restored, "Capacidade padrão não foi restaurada")
    require("#define CARDIOIA_QUEUE_CAPACITY 3" not in restored,
            "Definição temporária ainda aparece no editor")
    return {
        "fonte": "registros de interface do Wokwi",
        "fila_cheia": "aprovado",
        "botao_segurado": "aprovado: um pulso nas mensagens capturadas",
        "reinicio": "aprovado: nova sessao e nova fila em RAM",
        "capacidade_restaurada": 2000,
        "mensagens_validadas": len(rows),
        "sequencias_recuperadas": sequences,
        "perdas_antes_da_recuperacao": 3,
        "sessao_antes": old_session,
        "sessao_apos": new_session,
        "transporte": "serial_demo",
        "limite": "A fila em RAM e perdida ao reiniciar; isto nao valida MQTT.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pasta", type=Path, default=ROOT.parents[1] / "document/other/fase3/evidencias/2026-10-24")
    args = parser.parse_args()
    result = check_evidence(args.pasta)
    output = args.pasta / "validacao_cenarios.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))

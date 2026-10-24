"""Confiro as evidências Serial e os eventos persistidos do ensaio MQTT."""
import argparse
import json
import re
from pathlib import Path

from jsonschema import Draft202012Validator


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("diretorio", type=Path)
    args = parser.parse_args()
    root = args.diretorio
    contract = Path(__file__).resolve().parents[2] / "config/fase3/contratos/telemetria.schema.json"
    validator = Draft202012Validator(json.loads(contract.read_text(encoding="utf-8")))
    events = [json.loads(line) for line in (root / "eventos_consumidor.jsonl").read_text(encoding="utf-8").splitlines()]

    def read(name):
        return (root / name).read_text(encoding="utf-8")

    def session(text):
        return re.search(r"sessao=([a-f0-9]{16})", text).group(1)

    def packets(text):
        result = [json.loads(line.strip()) for line in text.splitlines() if line.strip().startswith("{")]
        for row in result:
            validator.validate(row)
            assert row["transport"] == "mqtt" and row["simulated"] is True
            assert row["dropped_total"] == 0
        return result

    def confirmed(text, sid):
        acks = [(int(seq), int(size)) for seq, size in re.findall(r"# ack_confirmado seq=(\d+) fila=(\d+)", text)]
        assert acks and acks[-1][1] == 0, "A fila ainda nao foi recuperada."
        sequences = [seq for seq, _ in acks]
        assert sequences == list(range(sequences[0], sequences[-1] + 1))
        for seq in sequences:
            stored = [e for e in events if e["event"] == "stored" and e["sample"]["session_id"] == sid and e["sample"]["sequence"] == seq]
            assert len(stored) == 1, (sid, seq, "persistencia ausente ou duplicada")
        packets(text)
        return {"primeira_sequencia_confirmada": sequences[0], "ultima_sequencia_confirmada": sequences[-1], "fila_final": 0}

    first = read("wokwi_primeira_troca.txt")
    sid = session(first)
    attempts = [row for row in packets(first) if row["sequence"] == 1]
    assert attempts[1]["attempt"] == 2
    assert attempts[1]["sent_uptime_ms"] - attempts[0]["sent_uptime_ms"] == 3000
    for kind in ("ack_withheld", "duplicate"):
        assert any(e["event"] == kind and e.get("ack", {}).get("session_id") == sid and e["ack"]["sequence"] == 1 for e in events)
    assert "# ack_confirmado seq=1" in first

    absent = read("wokwi_sem_consumidor.txt")
    pending = packets(absent)
    assert len(pending) >= 2 and {row["sequence"] for row in pending} == {1}
    assert "# ack_confirmado" not in absent
    resumed = read("wokwi_apos_reiniciar_consumidor.txt")
    resumed_result = confirmed(resumed, session(resumed))

    fault = read("wokwi_mqtt_final_broker_off.txt")
    fault_tail = fault.split("# teste_broker: endpoint TCP indisponivel")[-1]
    assert "porta=1" in fault_tail and "# coleta seq=" in fault_tail
    assert "# ack_confirmado" not in fault_tail
    restored = read("wokwi_mqtt_final_broker_recuperado.txt")
    restored_tail = restored.split("# teste_broker: endpoint normal restaurado")[-1]
    assert "# mqtt_conectado" in restored_tail
    fault_result = confirmed(restored_tail, session(restored))
    assert any(row["replay"] for row in packets(restored_tail))

    offline = read("wokwi_mqtt_final_chave_offline.txt").rsplit("# conexao_simulada=offline", 1)[1]
    assert len(re.findall(r"# coleta seq=", offline)) >= 2
    assert "# ack_confirmado" not in offline
    online = read("wokwi_mqtt_final_chave_recuperada.txt")
    online_tail = online.rsplit("# conexao_simulada=online", 1)[1]
    switch_result = confirmed(online_tail, session(online))

    final_configuration = read("wokwi_mqtt_timeout_final.txt")
    final_result = confirmed(final_configuration, session(final_configuration))

    result = {"resultado": "aprovado", "ack_omitido_reenvio_ms": 3000,
              "tentativas_sem_consumidor": len(pending), "reinicio_consumidor": resumed_result,
              "recuperacao_endpoint": fault_result, "recuperacao_chave": switch_result,
              "comunicacao_apos_ajuste_timeout": final_result,
              "perdas_reportadas_nos_pacotes_conferidos": 0}
    (root / "validacao_cenarios.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

"""Testo o consumidor real pelo broker com um publicador Python identificado.

Este teste não representa execução do ESP32 nem substitui a validação no Wokwi.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import queue
import sqlite3
import subprocess
import sys
import threading
import time
import uuid

ROOT = Path(__file__).resolve().parents[2] / "src/fase3"


def main():
    import paho.mqtt.client as mqtt

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", type=Path, required=True)
    args = parser.parse_args()
    args.saida.mkdir(parents=True, exist_ok=True)
    run_id = uuid.uuid4().hex[:16]
    topic_root = f"cardioia/aura/fase3/478054573982428161/teste-python/{run_id}"
    db = ROOT.parents[1] / f"fase3/runtime/teste_rede_{run_id}.sqlite3"
    events = args.saida / "eventos_consumidor.jsonl"
    log = (args.saida / "consumidor_stdout.txt").open("w", encoding="utf-8")
    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
    process = subprocess.Popen([
        sys.executable, str(ROOT / "python/consumidor_mqtt.py"),
        "--topico", topic_root, "--db", str(db), "--eventos", str(events),
        "--reter-primeiro-ack", "--duracao", "60",
    ], stdout=log, stderr=subprocess.STDOUT, creationflags=creationflags)
    ready = threading.Event()
    acknowledgements = queue.Queue()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="aura-test-" + run_id)
    device = "cardioia-publicador-python"
    telemetry_topic = f"{topic_root}/devices/{device}/telemetry"
    ack_topic = f"{topic_root}/devices/{device}/ack"

    def on_connect(client, userdata, flags, reason_code, properties):
        if reason_code == 0:
            client.subscribe(ack_topic, qos=1)

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        ready.set()

    def on_message(client, userdata, message):
        acknowledgements.put(json.loads(message.payload))

    client.on_connect, client.on_subscribe, client.on_message = on_connect, on_subscribe, on_message

    def read_events():
        return [json.loads(line) for line in events.read_text(encoding="utf-8").splitlines()] if events.exists() else []

    def send(data):
        info = client.publish(telemetry_topic, json.dumps(data), qos=1, retain=False)
        info.wait_for_publish(timeout=5)
        if not info.is_published():
            raise RuntimeError("Não confirmei a publicação no broker")

    def receive_ack(sequence, timeout=5):
        ack = acknowledgements.get(timeout=timeout)
        if ack != {"schema_version": 1, "device_id": device, "session_id": run_id,
                   "sequence": sequence, "status": "stored"}:
            raise RuntimeError("Confirmação recebida com identidade incorreta")

    try:
        deadline = time.monotonic() + 15
        while len([e for e in read_events() if e["event"] == "subscribed"]) < 2:
            if time.monotonic() > deadline or process.poll() is not None:
                raise RuntimeError("Consumidor não assinou os tópicos do teste")
            time.sleep(0.1)
        client.connect("broker.hivemq.com", 1883, keepalive=15)
        client.loop_start()
        if not ready.wait(10):
            raise RuntimeError("Publicador não assinou o tópico de confirmação")
        sample = json.loads((ROOT.parents[1] / "config/fase3/contratos/exemplo_telemetria.json").read_text(encoding="utf-8"))
        sample.update(device_id=device, session_id=run_id, transport="mqtt",
                      sent_uptime_ms=5100, age_ms=100, attempt=1, replay=False)
        send(sample)
        try:
            receive_ack(1, timeout=2)
            raise RuntimeError("Primeiro ACK não foi omitido conforme o cenário")
        except queue.Empty:
            pass
        retry = sample | {"attempt": 2, "sent_uptime_ms": 8100, "age_ms": 3100}
        send(retry)
        receive_ack(1)
        send(retry | {"attempt": 3})
        receive_ack(1)
        send(sample | {"pulse_count": 7, "heart_rate_bpm": 84})
        try:
            receive_ack(1, timeout=2)
            raise RuntimeError("Mensagem conflitante recebeu confirmação")
        except queue.Empty:
            pass
        replay = sample | {"sequence": 2, "collected_uptime_ms": 10000,
                           "sent_uptime_ms": 30000, "age_ms": 20000, "replay": True}
        send(replay)
        receive_ack(2)
        rows = read_events()
        with sqlite3.connect(db) as connection:
            count = connection.execute("SELECT COUNT(*) FROM samples").fetchone()[0]
        if count != 2:
            raise RuntimeError(f"Esperava duas medições únicas, encontrei {count}")
        result = {
            "executado_em": datetime.now(timezone.utc).isoformat(),
            "origem": "publicador Python; nao e o ESP32/Wokwi",
            "broker": "broker.hivemq.com:1883", "topic_root": topic_root,
            "sessao": run_id, "medicoes_unicas": count,
            "duplicatas": sum(e["event"] == "duplicate" for e in rows),
            "confirmacoes_omitidas": sum(e["event"] == "ack_withheld" for e in rows),
            "conflitos_rejeitados": sum(e["event"] == "rejected" for e in rows),
            "resultado": "aprovado",
        }
        if result["duplicatas"] != 2 or result["confirmacoes_omitidas"] != 1 or result["conflitos_rejeitados"] != 1:
            raise RuntimeError("Eventos capturados não correspondem aos cenários")
        (args.saida / "resultado.json").write_text(json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        client.disconnect()
        client.loop_stop()
        if process.poll() is None:
            process.terminate()
        process.wait(timeout=10)
        log.close()


if __name__ == "__main__":
    main()

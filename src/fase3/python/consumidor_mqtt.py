"""Recebo telemetria simulada, gravo em SQLite e só então confirmo ao ESP32."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sqlite3
import time
import uuid

from mqtt_store import DEFAULT_TOPIC, InvalidTelemetry, ROOT, TelemetryStore


def main():
    import paho.mqtt.client as mqtt

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="broker.hivemq.com")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--topico", default=DEFAULT_TOPIC)
    parser.add_argument("--db", type=Path, default=ROOT.parents[1] / ".tools/runtime/fase3/telemetria.sqlite3")
    parser.add_argument("--eventos", type=Path, default=ROOT.parents[1] / ".tools/runtime/fase3/eventos_mqtt.jsonl")
    parser.add_argument("--sem-ack", action="store_true", help="Recebo e persisto sem confirmar, para testar reenvio")
    parser.add_argument("--reter-primeiro-ack", action="store_true", help="Omito apenas o primeiro ACK para testar deduplicação")
    parser.add_argument("--duracao", type=float, default=0, help="Segundos de execução; 0 mantém ativo")
    args = parser.parse_args()
    args.eventos.parent.mkdir(parents=True, exist_ok=True)
    store = TelemetryStore(args.db, args.topico)
    events = args.eventos.open("a", encoding="utf-8", buffering=1)
    omitted = False

    def emit(event):
        line = json.dumps(event, ensure_ascii=False, allow_nan=False)
        events.write(line + "\n")
        print(line, flush=True)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="aura-store-" + uuid.uuid4().hex[:12])
    client.reconnect_delay_set(min_delay=1, max_delay=15)
    client.max_queued_messages_set(100)

    def on_connect(client, userdata, flags, reason_code, properties):
        emit({"event": "broker_connected", "reason": str(reason_code)})
        if reason_code == 0:
            client.subscribe(f"{args.topico}/devices/+/telemetry", qos=1)
            client.subscribe(f"{args.topico}/devices/+/status", qos=1)

    def on_subscribe(client, userdata, mid, reason_codes, properties):
        emit({"event": "subscribed", "mid": mid, "reasons": [str(code) for code in reason_codes]})

    def on_disconnect(client, userdata, flags, reason_code, properties):
        emit({"event": "broker_disconnected", "reason": str(reason_code)})

    def on_connect_fail(client, userdata):
        emit({"event": "connect_error", "reason": "broker indisponivel; nova tentativa automatica"})

    def on_message(client, userdata, message):
        nonlocal omitted
        if message.topic.endswith("/status"):
            emit({"event": "device_status", "topic": message.topic,
                  "payload": message.payload[:512].decode("utf-8", errors="replace")})
            return
        # Retained antigo não deve retirar uma leitura atual da fila.
        if message.retain:
            emit({"event": "rejected", "reason": "telemetria retained", "topic": message.topic})
            return
        try:
            result = store.receive(message.topic, message.payload)
        except (InvalidTelemetry, sqlite3.Error) as error:
            emit({"event": "rejected", "reason": str(error), "topic": message.topic})
            return
        emit(result)
        if args.sem_ack or (args.reter_primeiro_ack and not omitted):
            omitted = True
            emit({"event": "ack_withheld", "ack": result["ack"]})
            return
        info = client.publish(result["ack_topic"], json.dumps(result["ack"]), qos=1, retain=False)
        emit({"event": "ack_queued", "rc": int(info.rc), "ack": result["ack"]})

    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_disconnect = on_disconnect
    client.on_connect_fail = on_connect_fail
    client.on_message = on_message
    try:
        # O loop também lida com falha na primeira conexão e reconexões.
        client.connect_async(args.host, args.port, keepalive=20)
        client.loop_start()
        started = time.monotonic()
        while args.duracao <= 0 or time.monotonic() - started < args.duracao:
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass
    finally:
        client.disconnect()
        client.loop_stop()
        store.close()
        events.close()


if __name__ == "__main__":
    main()

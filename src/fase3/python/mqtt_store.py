"""Validação e persistência antes da confirmação de cada leitura MQTT."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sqlite3

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TOPIC = "cardioia/aura/fase3/478054573982428161/v1"
MEASUREMENTS = (
    "schema_version", "device_id", "session_id", "sequence", "collected_uptime_ms",
    "window_ms", "temperature_c", "humidity_pct", "pulse_count", "heart_rate_bpm",
    "dht_valid", "simulated", "transport",
)


class InvalidTelemetry(ValueError):
    pass


class ConflictingTelemetry(InvalidTelemetry):
    pass


def decode_packet(payload: bytes) -> dict:
    if len(payload) > 2048:
        raise InvalidTelemetry("Mensagem maior que 2048 bytes")
    try:
        def reject_constant(value):
            raise ValueError(f"Constante JSON inválida: {value}")

        def reject_duplicate_keys(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"Campo repetido: {key}")
                result[key] = value
            return result

        result = json.loads(payload.decode("utf-8"), parse_constant=reject_constant,
                            object_pairs_hook=reject_duplicate_keys)
    except (UnicodeDecodeError, ValueError) as error:
        raise InvalidTelemetry("JSON inválido") from error
    if not isinstance(result, dict):
        raise InvalidTelemetry("A mensagem deve ser um objeto")
    return result


class TelemetryStore:
    def __init__(self, path: Path, topic_root: str = DEFAULT_TOPIC):
        self.topic_root = topic_root.rstrip("/")
        self.validator = Draft202012Validator(json.loads(
            (ROOT.parents[1] / "config/fase3/contratos/telemetria.schema.json").read_text(encoding="utf-8")))
        path.parent.mkdir(parents=True, exist_ok=True)
        # Uso esta conexão em um único callback de rede por vez. A criação
        # ocorre antes de iniciar a thread Paho; o fechamento ocorre após pará-la.
        self.connection = sqlite3.connect(path, check_same_thread=False)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=FULL")
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS samples (
                device_id TEXT NOT NULL, session_id TEXT NOT NULL,
                sequence INTEGER NOT NULL, fingerprint TEXT NOT NULL,
                payload TEXT NOT NULL, received_at TEXT NOT NULL,
                PRIMARY KEY (device_id, session_id, sequence)
            )
        """)
        self.connection.commit()

    def close(self):
        self.connection.close()

    def receive(self, topic: str, payload: bytes) -> dict:
        data = decode_packet(payload)
        errors = sorted(self.validator.iter_errors(data), key=lambda e: str(e.path))
        if errors:
            raise InvalidTelemetry(errors[0].message)
        if data["transport"] != "mqtt":
            raise InvalidTelemetry("O consumidor aceita apenas transporte MQTT")
        expected_topic = f"{self.topic_root}/devices/{data['device_id']}/telemetry"
        if topic != expected_topic:
            raise InvalidTelemetry("Dispositivo e tópico não correspondem")
        age = data["sent_uptime_ms"] - data["collected_uptime_ms"]
        if age < 0 or age != data["age_ms"] or data["replay"] != (age > 10000):
            raise InvalidTelemetry("Metadados temporais inconsistentes")
        bpm = data["pulse_count"] * 60000 / data["window_ms"]
        if not math.isfinite(data["heart_rate_bpm"]) or abs(bpm - data["heart_rate_bpm"]) > 0.011:
            raise InvalidTelemetry("BPM incompatível com a janela de pulsos")
        immutable = {name: data[name] for name in MEASUREMENTS}
        canonical = json.dumps(immutable, sort_keys=True, separators=(",", ":"), allow_nan=False)
        fingerprint = hashlib.sha256(canonical.encode()).hexdigest()
        identity = (data["device_id"], data["session_id"], data["sequence"])
        received_at = datetime.now(timezone.utc).isoformat()
        encoded = json.dumps(data, ensure_ascii=False, allow_nan=False)
        # A transação termina antes de preparar o ACK. Erros de armazenamento
        # propagam e não geram confirmação ao dispositivo.
        with self.connection:
            row = self.connection.execute(
                "SELECT fingerprint, payload, received_at FROM samples "
                "WHERE device_id=? AND session_id=? AND sequence=?", identity).fetchone()
            if row is not None and row[0] != fingerprint:
                raise ConflictingTelemetry("Mesma identidade contém medições diferentes")
            duplicate = row is not None
            if not duplicate:
                self.connection.execute("INSERT INTO samples VALUES (?, ?, ?, ?, ?, ?)",
                                        (*identity, fingerprint, encoded, received_at))
        ack = {
            "schema_version": 1, "device_id": data["device_id"],
            "session_id": data["session_id"], "sequence": data["sequence"], "status": "stored",
        }
        return {
            "event": "duplicate" if duplicate else "stored", "received_at": received_at,
            "first_received_at": row[2] if duplicate else received_at,
            "sample": json.loads(row[1]) if duplicate else data,
            "attempt": data["attempt"], "age_ms": data["age_ms"],
            "ack_topic": f"{self.topic_root}/devices/{data['device_id']}/ack", "ack": ack,
        }

"""Verifico persistência e integridade sem depender de um broker externo."""
import copy
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from mqtt_store import ConflictingTelemetry, DEFAULT_TOPIC, InvalidTelemetry, TelemetryStore


class MqttStoreTest(unittest.TestCase):
    def setUp(self):
        (ROOT / "build").mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=ROOT / "build")
        self.path = Path(self.temp.name) / "telemetria.sqlite3"
        self.store = TelemetryStore(self.path)
        self.sample = json.loads((ROOT.parents[1] / "config/fase3/contratos/exemplo_telemetria.json").read_text(encoding="utf-8"))
        self.sample.update(transport="mqtt", sent_uptime_ms=5100, age_ms=100, attempt=1, replay=False)
        self.topic = f"{DEFAULT_TOPIC}/devices/{self.sample['device_id']}/telemetry"

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def send(self, data=None, topic=None):
        return self.store.receive(topic or self.topic, json.dumps(data or self.sample).encode())

    def test_ack_depois_de_commit_visivel_por_outra_conexao(self):
        result = self.send()
        self.assertEqual(result["ack"]["status"], "stored")
        self.assertEqual(result["event"], "stored")
        with closing(sqlite3.connect(self.path)) as other:
            row = other.execute("SELECT sequence FROM samples").fetchone()
        self.assertEqual(row, (result["ack"]["sequence"],))
        self.assertTrue(result["received_at"].endswith("+00:00"))

    def test_reenvio_atualiza_metadados_sem_duplicar_medicao(self):
        first = self.send()
        retry = self.sample | {"sent_uptime_ms": 19000, "age_ms": 14000,
                               "attempt": 2, "replay": True, "backlog_samples": 3, "dropped_total": 2}
        second = self.send(retry)
        self.assertEqual(second["event"], "duplicate")
        self.assertEqual(first["ack"], second["ack"])
        self.assertEqual(first["received_at"], second["first_received_at"])
        self.assertEqual(self.store.connection.execute("SELECT COUNT(*) FROM samples").fetchone()[0], 1)

    def test_deduplicacao_sobrevive_reinicio_do_consumidor(self):
        self.send()
        self.store.close()
        self.store = TelemetryStore(self.path)
        self.assertEqual(self.send()["event"], "duplicate")

    def test_mudanca_de_sessao_permitem_mesma_sequencia(self):
        self.send()
        self.assertEqual(self.send(self.sample | {"session_id": "fedcba9876543210"})["event"], "stored")
        self.assertEqual(self.store.connection.execute("SELECT COUNT(*) FROM samples").fetchone()[0], 2)

    def test_identidade_conflitante_nao_altera_registro(self):
        self.send()
        with self.assertRaises(ConflictingTelemetry):
            self.send(self.sample | {"pulse_count": 7, "heart_rate_bpm": 84})
        original = json.loads(self.store.connection.execute("SELECT payload FROM samples").fetchone()[0])
        self.assertEqual(original["pulse_count"], 6)

    def test_contrato_e_semantica_rejeitam_entradas_incoerentes(self):
        cases = [
            {"transport": "serial_demo"}, {"simulated": False}, {"window_ms": 0},
            {"sent_uptime_ms": 4900, "age_ms": 0}, {"age_ms": 50},
            {"replay": True}, {"heart_rate_bpm": 200}, {"attempt": 0},
            {"dht_valid": False}, {"humidity_pct": 110}, {"paciente": "nao permitido"},
            {"sequence": 2**64},
        ]
        for change in cases:
            with self.subTest(change=change), self.assertRaises(InvalidTelemetry):
                self.send(self.sample | change)
        self.assertEqual(self.store.connection.execute("SELECT COUNT(*) FROM samples").fetchone()[0], 0)

    def test_topico_de_outro_dispositivo_nao_recebe_ack(self):
        with self.assertRaises(InvalidTelemetry):
            self.send(topic=f"{DEFAULT_TOPIC}/devices/outro/telemetry")

    def test_json_invalido_nao_recebe_ack(self):
        for payload in [b'{"x": NaN}', b'{"x":1,"x":2}', b'[]', b'\xff', b'x' * 2049]:
            with self.subTest(payload=payload[:20]), self.assertRaises(InvalidTelemetry):
                self.store.receive(self.topic, payload)

    def test_falha_de_gravacao_nao_produz_ack(self):
        self.store.connection.execute("PRAGMA query_only=ON")
        with self.assertRaises(sqlite3.OperationalError):
            self.send()

    def test_nucleo_edge_preservado_na_variante_mqtt(self):
        original = ROOT / "firmware/cardioia_edge/edge_core.h"
        variant = ROOT / "firmware/cardioia_mqtt/edge_core.h"
        self.assertEqual(original.read_bytes(), variant.read_bytes())


if __name__ == "__main__":
    unittest.main()

"""Conferimos HTTP real, regras, persistência e e-mails locais do Ir Além 1."""
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src/fase3/python"))
from cliente_rest import demonstrate, request
from servico_rest import RestStore, make_server


class RestTest(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".tools/tmp"
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.store = RestStore(self.temp.name)
        self.server = make_server(self.store, 0)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"
        self.sample = json.loads((ROOT / "config/fase3/contratos/exemplo_telemetria.json").read_text(encoding="utf-8"))

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        self.store.close()
        self.temp.cleanup()

    def post(self, **updates):
        self.sample.update(updates)
        return request(self.base, "POST", "/leituras", self.sample)

    def test_fluxo_envio_consulta_episodios_e_reenvio(self):
        result = demonstrate(self.base)
        self.assertEqual(5, len(result["received"]))
        self.assertTrue(result["repeated"]["duplicate"])
        self.assertEqual([False, True, False, False, True], [r["email_id"] is not None for r in result["sent"]])
        emails = list((Path(self.temp.name) / "emails").glob("*.eml"))
        self.assertEqual(2, len(emails))
        from email import policy
        from email.parser import BytesParser
        mail = BytesParser(policy=policy.default).parsebytes(emails[0].read_bytes())
        self.assertEqual("grupo-aura@example.invalid", mail["To"])
        self.assertIn("temperatura_ambiente_acima_30_c", mail.get_content())

    def test_dados_invalidos_e_conflito(self):
        with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
            self.post(heart_rate_bpm=999)
        self.post(heart_rate_bpm=72)
        with self.assertRaisesRegex(RuntimeError, "HTTP 409"):
            self.post(temperature_c=31)
        self.assertEqual(1, len(request(self.base, "GET", "/leituras")["readings"]))

    def test_historico_nao_dispara_alerta(self):
        result = self.post(transport="mqtt", sent_uptime_ms=20000, age_ms=15000,
                           attempt=2, replay=True, temperature_c=40)
        self.assertEqual("historico_sem_alerta", result["evaluation"])
        self.assertIsNone(result["email_id"])

    def test_sensor_invalido_nao_resolve_alerta_temperatura(self):
        first = self.post(temperature_c=31)
        self.assertIsNotNone(first["email_id"])
        missing = self.post(sequence=2, dht_valid=False, temperature_c=None, humidity_pct=None)
        self.assertEqual(first["active_episodes"], missing["active_episodes"])
        restored = self.post(sequence=3, dht_valid=True, temperature_c=31, humidity_pct=40)
        self.assertIsNone(restored["email_id"])

    def test_reinicio_preserva_episodio_e_reconstroi_email(self):
        self.post(temperature_c=31)
        # Encerramos HTTP antes de substituir a conexão de persistência.
        self.server.shutdown()
        self.thread.join()
        self.store.close()
        mail = next((Path(self.temp.name) / "emails").glob("*.eml"))
        mail.unlink()
        self.store = RestStore(self.temp.name)
        self.assertTrue(mail.exists())
        self.sample.update(sequence=2)
        result = self.store.receive(json.dumps(self.sample).encode())
        self.assertIsNone(result["email_id"])

    def test_ordem_e_metadados(self):
        self.post(sequence=3)
        with self.assertRaisesRegex(RuntimeError, "HTTP 409"):
            self.post(sequence=2)
        with self.assertRaisesRegex(RuntimeError, "HTTP 400"):
            self.post(sequence=4, transport="mqtt", age_ms=0, sent_uptime_ms=20000, replay=False, attempt=1)

    def test_erro_http_e_indisponibilidade(self):
        with self.assertRaisesRegex(RuntimeError, "HTTP 404"):
            request(self.base, "GET", "/inexistente")
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()
        with self.assertRaisesRegex(RuntimeError, "API indisponível"):
            request(self.base, "GET", "/saude")


if __name__ == "__main__":
    unittest.main()

"""Valida o contrato e mensagens negativas com unittest e jsonschema."""
import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


class TelemetriaTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = json.loads((ROOT / "contratos/telemetria.schema.json").read_text(encoding="utf-8"))
        Draft202012Validator.check_schema(cls.schema)
        cls.validator = Draft202012Validator(cls.schema)
        cls.example = json.loads((ROOT / "contratos/exemplo_telemetria.json").read_text(encoding="utf-8"))

    def test_exemplo_valido(self):
        self.validator.validate(self.example)

    def test_falha_sensor_usa_null(self):
        message = copy.deepcopy(self.example)
        message.update(dht_valid=False, temperature_c=None, humidity_pct=None)
        self.validator.validate(message)
        message["temperature_c"] = 0
        self.assertFalse(self.validator.is_valid(message))

    def test_inconsistencias_rejeitadas(self):
        for changes in [
            {"temperature_c": None}, {"window_ms": 0}, {"sequence": 0},
            {"humidity_pct": 101}, {"backlog_samples": 2001},
            {"simulated": False}, {"transport": "cloud_confirmada"},
            {"session_id": "sem_sessao"}, {"paciente_nome": "nao permitido"},
        ]:
            with self.subTest(changes=changes):
                self.assertFalse(self.validator.is_valid(self.example | changes))

    def test_cada_campo_obrigatorio(self):
        for key in self.schema["required"]:
            message = self.example.copy()
            del message[key]
            with self.subTest(key=key):
                self.assertFalse(self.validator.is_valid(message))


if __name__ == "__main__":
    unittest.main()

"""Confiro a preservação do WAL e a proteção de destinos com dados anteriores."""
import json
from contextlib import closing
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

REPOSITORIO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPOSITORIO / "scripts/fase3"))
from migrar_runtime import conferir_banco, migrar


class RuntimeMigrationTest(unittest.TestCase):
    def setUp(self):
        base = REPOSITORIO / ".tools/tmp"
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "origem"
        self.target = self.root / "destino"
        self.source.mkdir()

    def test_copio_dados_confirmados_ainda_no_wal_e_preservo_origem(self):
        dbfile = self.source / "telemetria.sqlite3"
        with closing(sqlite3.connect(dbfile)) as db:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("PRAGMA wal_autocheckpoint=0")
            db.execute("CREATE TABLE samples (sequence INTEGER)")
            db.executemany("INSERT INTO samples VALUES (?)", [(1,), (2,)])
            db.commit()
            self.assertGreater(Path(str(dbfile) + "-wal").stat().st_size, 0)
            (self.source / "eventos.jsonl").write_text('{"event":"stored"}\n')
            modules = self.source / "node_modules"
            modules.mkdir()
            (modules / "cache.js").write_text("cache")
            resultado = migrar(self.source, self.target)
        self.assertTrue(resultado["origem_preservada"])
        self.assertEqual(conferir_banco(self.target / dbfile.name), {"samples": 2})
        self.assertEqual(conferir_banco(dbfile), {"samples": 2})
        self.assertEqual((self.target / "eventos.jsonl").read_bytes(), (self.source / "eventos.jsonl").read_bytes())
        self.assertFalse((self.target / "node_modules").exists())
        self.assertEqual(json.loads((self.target / "migracao.json").read_text())["resultado"], "aprovado")

    def test_nao_sobrescrevo_destino_preexistente(self):
        self.target.mkdir()
        marker = self.target / "preservo.txt"
        marker.write_text("execução anterior", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            migrar(self.source, self.target)
        self.assertEqual(marker.read_text(encoding="utf-8"), "execução anterior")

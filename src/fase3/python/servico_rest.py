"""API REST local do Ir Além 1: leituras simuladas e caixa de saída didática."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from email.message import EmailMessage
from email.policy import SMTP
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
import sqlite3

from jsonschema import Draft202012Validator
from mqtt_store import decode_packet, InvalidTelemetry

ROOT = Path(__file__).resolve().parents[3]


class Conflict(ValueError):
    pass


class RestStore:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(self.directory / "rest.sqlite3", check_same_thread=False)
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS readings (
                device TEXT, session TEXT, sequence INTEGER, payload TEXT,
                result TEXT, PRIMARY KEY(device, session, sequence));
            CREATE TABLE IF NOT EXISTS episodes (
                device TEXT, session TEXT, active TEXT,
                PRIMARY KEY(device, session));
            CREATE TABLE IF NOT EXISTS outbox (
                id INTEGER PRIMARY KEY, content BLOB NOT NULL);
        """)
        self.validator = Draft202012Validator(json.loads(
            (ROOT / "config/fase3/contratos/telemetria.schema.json").read_text(encoding="utf-8")))
        self.export_mail()

    def close(self):
        self.db.close()

    def export_mail(self):
        # A caixa persistente permite reconstruir arquivos após interrupção.
        folder = self.directory / "emails"
        folder.mkdir(exist_ok=True)
        for number, content in self.db.execute("SELECT id, content FROM outbox"):
            destination = folder / f"alerta-{number:04d}.eml"
            if not destination.exists():
                temporary = destination.with_suffix(".tmp")
                temporary.write_bytes(content)
                temporary.replace(destination)

    def receive(self, raw):
        sample = decode_packet(raw)
        errors = list(self.validator.iter_errors(sample))
        if errors:
            raise InvalidTelemetry(errors[0].message)
        if abs(sample["heart_rate_bpm"] - sample["pulse_count"] * 60000 / sample["window_ms"]) > .011:
            raise InvalidTelemetry("BPM incompatível com a janela")
        if sample["transport"] == "mqtt":
            age = sample["sent_uptime_ms"] - sample["collected_uptime_ms"]
            if age < 0 or age != sample["age_ms"] or sample["replay"] != (age > 10000):
                raise InvalidTelemetry("Metadados temporais inconsistentes")
        identity = (sample["device_id"], sample["session_id"], sample["sequence"])
        payload = json.dumps(sample, sort_keys=True, allow_nan=False)
        with self.db:
            previous = self.db.execute("SELECT payload, result FROM readings WHERE device=? AND session=? AND sequence=?", identity).fetchone()
            if previous:
                if previous[0] != payload:
                    raise Conflict("Identidade já registrada com conteúdo diferente")
                result = json.loads(previous[1])
                result["duplicate"] = True
                self.export_mail()
                return result
            last = self.db.execute("SELECT MAX(sequence) FROM readings WHERE device=? AND session=?", identity[:2]).fetchone()[0]
            if last is not None and sample["sequence"] <= last:
                raise Conflict("Enviar leituras em ordem crescente por sessão")
            eligible = not sample.get("replay", False) and sample.get("age_ms", 0) <= 10000 and sample["backlog_samples"] == 1
            reasons = []
            if eligible:
                if sample["heart_rate_bpm"] > 120:
                    reasons.append("pulsos_simulados_acima_120_bpm")
                if sample["dht_valid"] and sample["temperature_c"] > 30:
                    reasons.append("temperatura_ambiente_acima_30_c")
            row = self.db.execute("SELECT active FROM episodes WHERE device=? AND session=?", identity[:2]).fetchone()
            active = set(json.loads(row[0])) if row else set()
            # Dado histórico ou sensor inválido não encerra o episódio correspondente.
            next_active = set(active)
            if eligible:
                if sample["heart_rate_bpm"] <= 108:
                    next_active.discard("pulsos_simulados_acima_120_bpm")
                if sample["dht_valid"] and sample["temperature_c"] <= 28:
                    next_active.discard("temperatura_ambiente_acima_30_c")
                next_active.update(reasons)
            new_reasons = sorted(set(reasons) - active)
            mail_id = None
            if new_reasons:
                mail = EmailMessage(policy=SMTP)
                mail["From"] = "cardioia@example.invalid"
                mail["To"] = "grupo-aura@example.invalid"
                mail["Subject"] = "[SIMULACAO] CardioIA - alerta didatico"
                mail["Date"] = datetime.now(timezone.utc)
                mail.set_content("Simulamos um alerta acadêmico, sem envio externo ou diagnóstico.\n"
                                 f"Dispositivo/sessão/leitura: {identity}\n"
                                 f"Motivos: {', '.join(new_reasons)}\n"
                                 f"BPM artificial: {sample['heart_rate_bpm']}\n"
                                 f"Temperatura AMBIENTE: {sample['temperature_c']} °C\n")
                mail_id = self.db.execute("INSERT INTO outbox(content) VALUES (?)", (mail.as_bytes(),)).lastrowid
            result = {"sample": sample, "received_at": datetime.now(timezone.utc).isoformat(),
                      "duplicate": False, "evaluation": "didatica" if eligible else "historico_sem_alerta",
                      "reasons": reasons, "active_episodes": sorted(next_active), "email_id": mail_id,
                      "delivery": "arquivo_local_sem_envio" if mail_id else None}
            self.db.execute("INSERT OR REPLACE INTO episodes VALUES (?, ?, ?)", (*identity[:2], json.dumps(sorted(next_active))))
            self.db.execute("INSERT INTO readings VALUES (?, ?, ?, ?, ?)", (*identity, payload, json.dumps(result)))
        self.export_mail()
        return result

    def readings(self):
        return [json.loads(row[0]) for row in self.db.execute("SELECT result FROM readings ORDER BY rowid DESC LIMIT 100")]


def make_server(store, port=8765):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_):
            pass

        def respond(self, status, body):
            encoded = json.dumps(body, ensure_ascii=False, allow_nan=False).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        def do_GET(self):
            if self.path == "/leituras":
                self.respond(200, {"readings": store.readings()})
            elif self.path == "/saude":
                self.respond(200, {"status": "ok", "simulated": True})
            else:
                self.respond(404, {"error": "Rota inexistente"})

        def do_POST(self):
            if self.path != "/leituras":
                return self.respond(404, {"error": "Rota inexistente"})
            if self.headers.get_content_type() != "application/json":
                return self.respond(415, {"error": "Usar application/json"})
            try:
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= 2048:
                    return self.respond(413, {"error": "Corpo deve ter de 1 a 2048 bytes"})
                result = store.receive(self.rfile.read(size))
                self.respond(200 if result["duplicate"] else 201, result)
            except Conflict as error:
                self.respond(409, {"error": str(error)})
            except (InvalidTelemetry, ValueError) as error:
                self.respond(400, {"error": str(error)})
            except (sqlite3.Error, OSError):
                self.respond(503, {"error": "Armazenamento indisponível; repetir a mesma leitura"})

        def setup(self):
            super().setup()
            self.connection.settimeout(5)

    return HTTPServer(("127.0.0.1", port), Handler)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--porta", type=int, default=8765)
    parser.add_argument("--dados", type=Path, default=ROOT / ".tools/runtime/fase3/rest")
    args = parser.parse_args()
    store = RestStore(args.dados)
    server = make_server(store, args.porta)
    print(f"API local: http://127.0.0.1:{server.server_port} | E-mails simulados: {args.dados / 'emails'}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        store.close()


if __name__ == "__main__":
    main()

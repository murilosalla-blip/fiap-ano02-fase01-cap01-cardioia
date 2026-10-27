"""Enviamos e consultamos leituras na API local; não enviamos e-mails reais."""
import argparse
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import uuid

ROOT = Path(__file__).resolve().parents[3]


def request(base, method, path, sample=None):
    data = json.dumps(sample, allow_nan=False).encode() if sample is not None else None
    req = Request(base.rstrip("/") + path, data=data, method=method,
                  headers={"Content-Type": "application/json"})
    try:
        with urlopen(req, timeout=5) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f"HTTP {error.code}: {error.read().decode('utf-8', errors='replace')}") from error
    except (URLError, TimeoutError) as error:
        raise RuntimeError(f"API indisponível: {error}") from error


def demonstrate(base):
    template = json.loads((ROOT / "config/fase3/contratos/exemplo_telemetria.json").read_text(encoding="utf-8"))
    template["device_id"] = "cardioia-rest-demo"
    template["session_id"] = uuid.uuid4().hex[:16]
    results = []
    # Cenários sintéticos identificados; não representam novas medições do Wokwi.
    for sequence, (pulses, temperature) in enumerate([(6, 24), (11, 31), (12, 32), (6, 24), (11, 31)], 1):
        sample = dict(template, sequence=sequence, collected_uptime_ms=sequence * 5000,
                      pulse_count=pulses, heart_rate_bpm=pulses * 12, temperature_c=temperature)
        results.append(request(base, "POST", "/leituras", sample))
    duplicate = request(base, "POST", "/leituras", sample)
    received = request(base, "GET", "/leituras")
    return {"scenario": "sintetico_local", "session_id": template["session_id"],
            "sent": results, "repeated": duplicate,
            "received": [r for r in received["readings"] if r["sample"]["session_id"] == template["session_id"]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8765")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--demonstrar", action="store_true")
    mode.add_argument("--consultar", action="store_true")
    mode.add_argument("--enviar", type=Path, help="JSON no contrato de telemetria existente")
    parser.add_argument("--saida", type=Path)
    args = parser.parse_args()
    try:
        result = demonstrate(args.url) if args.demonstrar else (
            request(args.url, "GET", "/leituras") if args.consultar else
            request(args.url, "POST", "/leituras", json.loads(args.enviar.read_text(encoding="utf-8"))))
        text = json.dumps(result, ensure_ascii=False, indent=2)
        if args.saida:
            args.saida.parent.mkdir(parents=True, exist_ok=True)
            args.saida.write_text(text + "\n", encoding="utf-8")
        print(text)
    except (RuntimeError, OSError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

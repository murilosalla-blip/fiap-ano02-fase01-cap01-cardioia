"""Mantenho o comando utilizado na validação do consumidor MQTT."""
from pathlib import Path
import runpy
import sys

source = Path(__file__).resolve().parents[2] / "src/fase3/python"
sys.path.insert(0, str(source))
if __name__ == "__main__":
    runpy.run_path(str(source / "consumidor_mqtt.py"), run_name="__main__")

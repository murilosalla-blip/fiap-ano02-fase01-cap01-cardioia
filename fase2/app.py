"""Mantenho a entrada publicada; o aplicativo está em src/fase2/app.py."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().parents[1] / "src/fase2/app.py"), run_name="__main__")

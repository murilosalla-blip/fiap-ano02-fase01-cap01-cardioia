"""Verifica preservação da Fase 1 e proíbe remoções de arquivos anteriores."""
import json
import subprocess
from pathlib import Path

def verificar(raiz=None):
    raiz = Path(raiz or Path(__file__).resolve().parents[2])
    manifesto = json.loads((raiz / "fase2/auditoria/preservacao_pre_revisao.json").read_text())
    erros = []
    for item in manifesto["entries"]:
        caminho = raiz / item["path"]
        if not caminho.is_file():
            erros.append("Ausente: " + item["path"])
            continue
        if item["immutable"]:
            sha = subprocess.check_output(
                ["git", "hash-object", "--no-filters", str(caminho)],
                cwd=raiz, text=True
            ).strip()
            if sha != item["sha"]:
                erros.append("Alterado: " + item["path"])
    if erros:
        raise AssertionError("\n".join(erros))
    return len(manifesto["entries"])

if __name__ == "__main__":
    print(f"Preservação confirmada: {verificar()} arquivos anteriores conferidos.")

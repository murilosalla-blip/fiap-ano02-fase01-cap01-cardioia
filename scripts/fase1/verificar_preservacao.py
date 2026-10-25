"""Confiro o conteúdo original da Fase 1 nos destinos registrados na organização."""
import hashlib
import json
from pathlib import Path

def verificar(raiz=None):
    raiz = Path(raiz or Path(__file__).resolve().parents[2])
    manifesto = json.loads((raiz / "document/other/organizacao/preservacao_fase1.json").read_text(encoding="utf-8"))
    erros = []
    for item in manifesto["arquivos"]:
        caminho = raiz / item["preservado_em"]
        if not caminho.is_file():
            erros.append("Ausente: " + item["preservado_em"])
            continue
        if item["imutavel"]:
            conteudo = caminho.read_bytes()
            if caminho.suffix.lower() not in {".pdf", ".docx", ".png", ".jpg", ".jpeg", ".xlsx"}:
                conteudo = conteudo.replace(b"\r\n", b"\n")
            sha = hashlib.sha1(b"blob " + str(len(conteudo)).encode() + b"\0" + conteudo).hexdigest()
            if sha != item["sha_git"]:
                erros.append("Alterado: " + item["preservado_em"])
    if erros:
        raise AssertionError("\n".join(erros))
    return len(manifesto["arquivos"])

if __name__ == "__main__":
    print(f"Preservação confirmada: {verificar()} arquivos anteriores conferidos.")

"""Conferimos os arquivos anteriores e identificamos as aulas preservadas no histórico."""
import hashlib
import json
from pathlib import Path

def verificar(raiz=None):
    raiz = Path(raiz or Path(__file__).resolve().parents[2])
    manifesto = json.loads((raiz / "document/other/organizacao/preservacao_fase1.json").read_text(encoding="utf-8"))
    higienizacao = json.loads((raiz / "document/other/organizacao/higienizacao.json").read_text(encoding="utf-8"))
    retirados = {item["caminho"]: item for item in higienizacao["retirados"]}
    erros = []
    for item in manifesto["arquivos"]:
        caminho = raiz / item["preservado_em"]
        if item["preservado_em"] in retirados:
            arquivo = retirados[item["preservado_em"]]
            if (arquivo["categoria"] != "aulas_pdf" or caminho.suffix != ".pdf"
                    or not item["preservado_em"].startswith("document/other/referencias/fase1/aulas/")
                    or arquivo["sha_git"] != item["sha_git"] or caminho.exists()):
                erros.append("Retirada indevida de arquivo anterior: " + item["preservado_em"])
            continue
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
    total = verificar()
    registros = Path(__file__).resolve().parents[2] / "document/other/organizacao"
    inventario = json.loads((registros / "preservacao_fase1.json").read_text(encoding="utf-8"))
    retirados = {item["caminho"] for item in json.loads((registros / "higienizacao.json").read_text(encoding="utf-8"))["retirados"]}
    aulas = sum(item["preservado_em"] in retirados for item in inventario["arquivos"])
    print(f"Preservação conferida: {total} itens do inventário anterior; "
          f"{total - aulas} arquivos presentes, com conferência dos conteúdos protegidos; "
          f"{aulas} PDFs de aulas identificados no histórico Git.")

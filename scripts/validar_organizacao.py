"""Conferimos presença, integridade e navegação das entregas após a organização."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def carregar_retirados(raiz=ROOT):
    """Aceitamos somente retiradas individuais de apoio, nunca dados ou programas."""
    registro = json.loads((raiz / "document/other/organizacao/higienizacao.json").read_text(encoding="utf-8"))
    assert re.fullmatch(r"[0-9a-f]{40}", registro["commit_recuperacao"]), "Commit de recuperação inválido"
    consolidacoes = {"analise_template_fiap.md", "PADRONIZACAO_FASES.md", "REVISAO_DOCUMENTACAO.md", "VALIDACAO.md"}
    retirados = {}
    for item in registro["retirados"]:
        caminho, categoria = item["caminho"], item["categoria"]
        p = Path(caminho)
        assert not p.is_absolute() and ".." not in p.parts and "\\" not in caminho, "Caminho de retirada inválido"
        permitido = (
            categoria == "aulas_pdf" and p.suffix == ".pdf" and
            p.parent.as_posix() in {f"document/other/referencias/fase{i}/aulas" for i in (1, 2, 3)}
            or categoria == "entrada_transitoria" and caminho.startswith("document/other/historico/entradas_transitorias/")
            or categoria == "ensaio_substituido" and p.suffix == ".json" and
            p.parent.as_posix() == "document/other/fase3/evidencias/2026-10-24/dashboard/teste_rede"
            or categoria == "registro_consolidado" and p.parent.as_posix() == "document/other/organizacao" and p.name in consolidacoes
            or categoria == "workflow_inativo" and caminho == "src/fase2/portal-cardioia/.github/workflows/deploy-pages.yml"
        )
        assert permitido, "Retirada fora do escopo de apoio: " + caminho
        assert caminho not in retirados, "Retirada duplicada: " + caminho
        assert re.fullmatch(r"[0-9a-f]{64}", item["sha256"]), "SHA-256 inválido: " + caminho
        assert re.fullmatch(r"[0-9a-f]{64}", item["sha256_lf"]), "SHA-256 de texto inválido: " + caminho
        assert re.fullmatch(r"[0-9a-f]{40}", item["sha_git"]), "Blob Git inválido: " + caminho
        assert not (raiz / caminho).exists(), "Arquivo retirado ainda presente: " + caminho
        retirados[caminho] = item
    return retirados


def verificar():
    retirados = carregar_retirados()
    registro = json.loads((ROOT / "document/other/organizacao/mapa_arquivos.json").read_text(encoding="utf-8"))
    erros = []
    pastas_modelo = {".github", "assets", "config", "document", "scripts", "src"}
    for folder in ROOT.iterdir():
        if folder.is_dir() and not folder.name.startswith(".") and folder.name not in pastas_modelo:
            erros.append("Pasta fora do modelo na raiz: " + folder.name)
    for phase in ("fase1", "fase2", "fase3"):
        for category in ("src", "assets", "config", "document"):
            if not (ROOT / category / phase).is_dir():
                erros.append(f"Fase sem agrupamento: {category}/{phase}")
    links_externos = json.loads((ROOT / "document/other/organizacao/links_externos_preservados.json").read_text(encoding="utf-8"))
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    urls_atuais = set(re.findall(r"https?://[^\s<>\"')]+", readme))
    for url in links_externos["urls"]:
        if url not in urls_atuais:
            erros.append("Link externo removido do README: " + url)
    padronizacao = json.loads((ROOT / "document/other/organizacao/mudancas_padronizacao.json").read_text(encoding="utf-8"))
    for item in padronizacao["arquivos"]:
        if item["depois"] in retirados:
            arquivo = retirados[item["depois"]]
            chave = "sha256_lf" if "sha256_lf" in item else "sha256"
            assert arquivo[chave] == item.get("sha256_lf", item["sha256_antes"]), "Hash do apoio retirado divergente: " + item["depois"]
            continue
        path = ROOT / item["depois"]
        if not path.is_file():
            erros.append("Renomeação sem destino: " + item["depois"])
            continue
        if path.suffix in {".md", ".py"} and "/historico/" not in item["depois"]:
            continue
        raw = path.read_bytes()
        if "sha256_lf" in item:
            raw = raw.replace(b"\r\n", b"\n")
        if hashlib.sha256(raw).hexdigest() != item.get("sha256_lf", item["sha256_antes"]):
            erros.append("Renomeação com conteúdo alterado: " + item["depois"])
    integros = 0
    for item in registro["arquivos"]:
        if item["depois"] in retirados:
            arquivo = retirados[item["depois"]]
            chave = "sha256_lf" if "sha256_lf" in item else "sha256"
            assert arquivo[chave] == item.get("sha256_lf", item["sha256_antes"]), "Hash do apoio retirado divergente: " + item["depois"]
            continue
        p = ROOT / item["depois"]
        if not p.is_file():
            erros.append("Ausente: " + item["depois"])
            continue
        revisavel = p.suffix.lower() in {".md", ".py", ".yml", ".ipynb", ".js", ".cjs"} or item["antes"] in {".gitignore", ".gitattributes"} or item["antes"] in {
            "fase2/auditoria/inventario_visual_ampliado.json", "fase3/node-red/package.json",
        }
        if not revisavel:
            conteudo = p.read_bytes()
            esperado = item["sha256_antes"]
            if "sha256_lf" in item:
                conteudo = conteudo.replace(b"\r\n", b"\n")
                esperado = item["sha256_lf"]
            if item["antes"] == "fase3/node-red/flows.json":
                conteudo = json.dumps(json.loads(conteudo), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
                esperado = item["sha256_json"]
            if hashlib.sha256(conteudo).hexdigest() != esperado:
                erros.append("Conteúdo alterado: " + item["depois"])
            else:
                integros += 1
        if p.suffix == ".ipynb":
            atual = json.loads(p.read_text(encoding="utf-8"))
            saidas = json.dumps([c.get("outputs") for c in atual["cells"]], ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
            if hashlib.sha256(saidas).hexdigest() != item["sha256_saidas_notebook"]:
                erros.append("Saídas históricas alteradas: " + item["depois"])
    links = 0
    files = [ROOT / "README.md", *(ROOT / "document").rglob("*.md"), ROOT / "src/readme.md", ROOT / "src/fase1/README.md", ROOT / "scripts/fase1/README.md", ROOT / "config/readme.md", ROOT / "scripts/readme.md"]
    for p in files:
        if "historico" in p.relative_to(ROOT).parts:
            continue
        text = re.sub(r"```[\s\S]*?```", "", p.read_text(encoding="utf-8"))
        for match in re.finditer(r"!?\[[^\]\n]*\]\((<[^>]+>|[^)\n]+)\)", text):
            target = match[1].strip("<>")
            if target.startswith(("#", "http:", "https:", "mailto:", "app:", "codex:", "data:")):
                continue
            target = unquote(target.partition("#")[0])
            dest = (p.parent / target).resolve()
            if not dest.is_relative_to(ROOT) or not dest.exists():
                erros.append(f"Link inválido: {p.relative_to(ROOT).as_posix()} -> {target}")
            links += 1
    if erros:
        raise AssertionError("\n".join(erros))
    atuais = sum(item["depois"] not in retirados for item in registro["arquivos"])
    print(f"Conferimos {atuais} destinos atuais, {integros} conteúdos preservados e {links} links locais; "
          f"{len(retirados)} arquivos de apoio retirados com recuperação registrada.")


if __name__ == "__main__":
    verificar()

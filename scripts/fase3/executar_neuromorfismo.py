"""Executamos o experimento ou o notebook com o mesmo Python do comando."""
import argparse
from copy import deepcopy
import os
from pathlib import Path
import re
import sys
from urllib.parse import quote, unquote, urlsplit, urlunsplit

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src/fase3/neuromorfismo"))


def relocar_link(href, origem, destino):
    """Relocamos somente destinos locais existentes dentro deste projeto."""
    parts = urlsplit(href)
    if parts.scheme or parts.netloc or not parts.path:
        return href
    target = (origem / unquote(parts.path)).resolve()
    if target.is_relative_to(ROOT) and target.exists():
        relative = Path(os.path.relpath(target, destino)).as_posix()
        return urlunsplit(("", "", quote(relative, safe="/"), parts.query, parts.fragment))
    return href


def corrigir_links_notebook(nb, origem, destino):
    """Preservamos a origem; ajustamos links Markdown somente na cópia exportada."""
    exported = deepcopy(nb)
    for cell in exported["cells"]:
        if cell["cell_type"] != "markdown":
            continue
        cell["source"] = re.sub(
            r"(!?\[[^\]\n]*\]\()([^\s)]+)(\))",
            lambda m: m[1] + relocar_link(m[2], origem, destino) + m[3],
            cell["source"],
        )
    return exported


def corrigir_links_html(html, origem, destino):
    """Mantemos links locais válidos ao exportar para outra pasta."""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    for anchor in soup.find_all("a", href=True):
        anchor["href"] = relocar_link(anchor["href"], origem, destino)
    return str(soup)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--saida", type=Path, default=Path(".tools/runtime/fase3/neuromorfismo"))
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--notebook", action="store_true", help="Executar notebook completo; usa protocolo fixo, seed=42.")
    args = parser.parse_args()
    out = (ROOT / args.saida).resolve()
    if args.notebook:
        if args.seed != 42 or args.saida != parser.get_default("saida"):
            parser.error("O notebook usa seed=42 e saída padrão; omitir --seed e --saida.")
        import nbformat
        from nbclient import NotebookClient
        from jupyter_client import KernelManager

        source = ROOT / "src/fase3/notebooks/comparacao_temporal_lif.ipynb"
        nb = nbformat.read(source, as_version=4)
        # Não dependemos do Python registrado globalmente como kernel python3.
        km = KernelManager(kernel_name="python3")
        km.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
        try:
            NotebookClient(nb, km=km, timeout=300, resources={"metadata": {"path": str(ROOT)}}).execute()
        finally:
            if km.has_kernel:
                km.shutdown_kernel(now=True)
        out.mkdir(parents=True, exist_ok=True)
        target = out / "comparacao_temporal_lif.executado.ipynb"
        nbformat.write(corrigir_links_notebook(nb, source.parent, out), target)
        from nbconvert import HTMLExporter
        html, _ = HTMLExporter().from_notebook_node(nb)
        html = corrigir_links_html(html, source.parent, out)
        (out / "comparacao_temporal_lif.html").write_text(html, encoding="utf-8")
        print(f"Notebook executado sem erro: {target}")
        print(f"Visualização: {out / 'comparacao_temporal_lif.html'}")
    else:
        from experimento import executar
        summary = executar(out, args.seed)
        for name, result in summary["modelos"].items():
            m = result["sessoes"]
            print(f"{name}: F1 macro={m['f1_macro']:.4f}; acurácia balanceada={m['acuracia_balanceada']:.4f}; C={result['C_escolhido']}")
        print(f"Resultados: {out}")


if __name__ == "__main__":
    main()

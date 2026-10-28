"""Conferimos os links das cópias exportadas sem alterar a origem ou a rede."""
import importlib.util
from pathlib import Path
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location("inicializador_lif", ROOT / "scripts/fase3/executar_neuromorfismo.py")
EXPORT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EXPORT)


class TestExportacao(unittest.TestCase):
    def setUp(self):
        self.origem = ROOT / "src/fase3/notebooks"
        self.destino = ROOT / ".tools/runtime/fase3/neuromorfismo"
        self.guia = "../../../document/fase3/neuromorfismo/README.md"

    def test_html_relocaliza_guia_e_preserva_imagem_incorporada(self):
        from bs4 import BeautifulSoup
        html = f'<a href="{self.guia}#passo-1">Guia</a><img src="data:image/png;base64,abc"/>'
        result = BeautifulSoup(EXPORT.corrigir_links_html(html, self.origem, self.destino), "html.parser")
        href = urlsplit(result.a["href"])
        self.assertEqual((self.destino / unquote(href.path)).resolve(), ROOT / "document/fase3/neuromorfismo/README.md")
        self.assertEqual(href.fragment, "passo-1")
        self.assertEqual(result.img["src"], "data:image/png;base64,abc")

    def test_notebook_exportado_nao_muda_origem_ou_codigo(self):
        original = {"cells": [{"cell_type": "markdown", "source": f"[Guia]({self.guia})"},
                              {"cell_type": "code", "source": f"texto = '[Guia]({self.guia})'", "outputs": []}]}
        exported = EXPORT.corrigir_links_notebook(original, self.origem, self.destino)
        self.assertNotEqual(exported["cells"][0]["source"], original["cells"][0]["source"])
        self.assertEqual(original["cells"][0]["source"], f"[Guia]({self.guia})")
        self.assertEqual(original["cells"][1], exported["cells"][1])

    def test_ancoras_urls_externas_e_destinos_inexistentes_permanecem(self):
        for href in ["#secao", "https://example.org/a?q=1#b", "mailto:teste@example.invalid", "ausente.md"]:
            self.assertEqual(EXPORT.relocar_link(href, self.origem, self.destino), href)


if __name__ == "__main__":
    unittest.main()

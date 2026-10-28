"""Verificamos isolamento, dinâmica LIF e avaliação, não apenas presença de arquivos."""
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from experimento import (RedeLIF, agregar_sessoes, atributos_tradicionais, criar_janelas,
                         dividir_sessoes, gerar_sessoes, metricas)


class TestExperimento(unittest.TestCase):
    def test_sessoes_independentes_e_reproduziveis(self):
        a, y = gerar_sessoes(42)
        b, z = gerar_sessoes(42)
        np.testing.assert_array_equal(a, b)
        np.testing.assert_array_equal(y, z)
        self.assertFalse(np.array_equal(a, gerar_sessoes(43)[0]))
        self.assertEqual(np.bincount(y).tolist(), [120, 120])
        self.assertEqual(a.shape, (240, 120))

    def test_sem_sessao_ou_janela_cruzando_particoes(self):
        a, y = gerar_sessoes()
        splits = dividir_sessoes(y)
        sets = [set(v) for v in splits.values()]
        self.assertFalse(sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2])
        self.assertEqual(set.union(*sets), set(range(240)))
        self.assertEqual([len(s) for s in sets], [144, 48, 48])
        for name, ids in splits.items():
            x, labels, groups, starts = criar_janelas(a, y, ids)
            self.assertEqual(x.shape, (len(ids) * 9, 24))
            self.assertEqual(set(groups), set(ids))
            for i in [0, len(x) - 1]:
                np.testing.assert_array_equal(x[i], a[groups[i], starts[i]:starts[i] + 24])
                self.assertEqual(labels[i], y[groups[i]])

    def test_dinamica_tem_limiar_reset_e_refratario(self):
        x = np.zeros((1, 24))
        lif = RedeLIF().fit(x)
        lif.win[:] = 0
        lif.wrec[:] = 0
        lif.bias[:] = 0
        _, _, quiet = lif.transform(x, trace=True)
        self.assertEqual(quiet.sum(), 0)
        lif.bias[:] = 3
        features, potential, spikes = lif.transform(x, trace=True)
        self.assertGreater(spikes.sum(), 0)
        self.assertTrue((potential[spikes == 1] >= 1).all())
        self.assertTrue((np.diff(np.flatnonzero(spikes[:, 0])) > 2).all())
        np.testing.assert_allclose(features, lif.transform(x))  # Estado reiniciado por janela.

    def test_teste_nao_reajusta_normalizacao(self):
        a, _ = gerar_sessoes()
        lif = RedeLIF().fit(a[:10, :24])
        params = (lif.mean, lif.scale, lif.diff_scale)
        lif.transform(np.full((2, 24), 10000))
        self.assertEqual(params, (lif.mean, lif.scale, lif.diff_scale))

    def test_agregacao_por_sessao_e_metricas(self):
        ids, y, p = agregar_sessoes(np.array([0, 0, 1, 1]), np.array([0.2, 0.4, 0.7, 0.9]), np.array([3, 3, 8, 8]))
        self.assertEqual(ids.tolist(), [3, 8])
        np.testing.assert_allclose(p, [0.3, 0.8])
        self.assertEqual(metricas(y, p)["matriz_confusao"], [[1, 0], [0, 1]])
        self.assertEqual(metricas(y, 1 - p)["f1_macro"], 0)

    def test_atributos_temporais_e_estabilidade_em_sinal_constante(self):
        a = np.full((2, 24), 80.0)
        f = atributos_tradicionais(a)
        self.assertTrue(np.isfinite(f).all())
        self.assertEqual(f.shape, (2, 8))
        self.assertEqual(f[0, 4], 0)
        a[0, ::2] = 100
        self.assertGreater(atributos_tradicionais(a)[0, 4], 0)


if __name__ == "__main__":
    unittest.main()

import math
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Algoritmos import etapa2

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True, errors="replace")

etapa2.logLigado = False


class TesteParMaisProximo(unittest.TestCase):

    def _validar_resultado(self, resultado):
        distancia, ponto1, ponto2 = resultado
        self.assertIsNotNone(ponto1)
        self.assertIsNotNone(ponto2)
        self.assertAlmostEqual(distancia, math.dist(ponto1, ponto2), places=9)

    def test_caso_conhecido(self):
        pontos = [(0, 0), (5, 5), (1, 1), (10, 10)]

        resultado_forca_bruta = etapa2.ParMaisProximoForcaBruta(pontos)
        resultado_divisao_conquista = etapa2.ParMaisProximoDivisaoConquista(pontos)

        self._validar_resultado(resultado_forca_bruta)
        self._validar_resultado(resultado_divisao_conquista)
        self.assertAlmostEqual(resultado_forca_bruta[0], math.sqrt(2), places=9)
        self.assertAlmostEqual(resultado_divisao_conquista[0], math.sqrt(2), places=9)

    def test_pontos_duplicados(self):
        pontos = [(2, 2), (2, 2), (9, 9)]

        resultado_forca_bruta = etapa2.ParMaisProximoForcaBruta(pontos)
        resultado_divisao_conquista = etapa2.ParMaisProximoDivisaoConquista(pontos)

        self._validar_resultado(resultado_forca_bruta)
        self._validar_resultado(resultado_divisao_conquista)
        self.assertEqual(resultado_forca_bruta[0], 0)
        self.assertEqual(resultado_divisao_conquista[0], 0)

    def test_empate_entre_dois_pares(self):
        pontos = [(0, 0), (0, 3), (10, 0), (10, 3)]

        resultado_forca_bruta = etapa2.ParMaisProximoForcaBruta(pontos)
        resultado_divisao_conquista = etapa2.ParMaisProximoDivisaoConquista(pontos)

        self._validar_resultado(resultado_forca_bruta)
        self._validar_resultado(resultado_divisao_conquista)
        self.assertAlmostEqual(resultado_forca_bruta[0], 3, places=9)
        self.assertAlmostEqual(resultado_divisao_conquista[0], 3, places=9)

    def test_coordenadas_negativas(self):
        pontos = [(-5, -5), (-1, -2), (10, 10), (4, 4), (20, -3)]

        resultado_forca_bruta = etapa2.ParMaisProximoForcaBruta(pontos)
        resultado_divisao_conquista = etapa2.ParMaisProximoDivisaoConquista(pontos)

        self._validar_resultado(resultado_forca_bruta)
        self._validar_resultado(resultado_divisao_conquista)
        self.assertAlmostEqual(resultado_forca_bruta[0], 5, places=9)
        self.assertAlmostEqual(resultado_divisao_conquista[0], 5, places=9)

    def test_muitos_pontos_na_mesma_linha(self):
        pontos = [(indice, 0) for indice in range(50)]

        resultado_forca_bruta = etapa2.ParMaisProximoForcaBruta(pontos)
        resultado_divisao_conquista = etapa2.ParMaisProximoDivisaoConquista(pontos)

        self._validar_resultado(resultado_forca_bruta)
        self._validar_resultado(resultado_divisao_conquista)
        self.assertAlmostEqual(resultado_forca_bruta[0], 1, places=9)
        self.assertAlmostEqual(resultado_divisao_conquista[0], 1, places=9)

    def test_poucos_pontos(self):
        resultado_forca_bruta = etapa2.ParMaisProximoForcaBruta([])
        resultado_divisao_conquista = etapa2.ParMaisProximoDivisaoConquista([])
        self.assertEqual(resultado_forca_bruta, (float("inf"), None, None))
        self.assertEqual(resultado_divisao_conquista, (float("inf"), None, None))

        resultado_forca_bruta = etapa2.ParMaisProximoForcaBruta([(1, 2)])
        resultado_divisao_conquista = etapa2.ParMaisProximoDivisaoConquista([(1, 2)])
        self.assertEqual(resultado_forca_bruta, (float("inf"), None, None))
        self.assertEqual(resultado_divisao_conquista, (float("inf"), None, None))

    def test_forca_bruta_e_divisao_conquista_concordam(self):
        random.seed(2026)

        for _ in range(50):
            quantidade = random.randint(2, 80)
            pontos = [
                (random.uniform(-1000, 1000), random.uniform(-1000, 1000))
                for _ in range(quantidade)
            ]

            resultado_forca_bruta = etapa2.ParMaisProximoForcaBruta(pontos)
            resultado_divisao_conquista = etapa2.ParMaisProximoDivisaoConquista(pontos)

            self.assertAlmostEqual(
                resultado_forca_bruta[0], resultado_divisao_conquista[0], places=9
            )


if __name__ == "__main__":
    conjunto_testes = unittest.TestLoader().loadTestsFromTestCase(TesteParMaisProximo)
    executor = unittest.TextTestRunner(verbosity=2)
    executor.run(conjunto_testes)

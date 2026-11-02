import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Algoritmos import etapa1
from Algoritmos.etapa1 import SomaMaximaForcaBruta, SomaMaximaDivisaoConquista

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True, errors="replace")

etapa1.logLigado = False


class TesteSomaMaxima(unittest.TestCase):

    def _validar_resultado(self, vetor, resultado, soma_esperada):
        soma, inicio, fim = resultado
        self.assertEqual(soma, soma_esperada)
        self.assertGreaterEqual(inicio, 0)
        self.assertLess(inicio, len(vetor))
        self.assertGreaterEqual(fim, inicio)
        self.assertLess(fim, len(vetor))
        self.assertEqual(sum(vetor[inicio:fim + 1]), soma_esperada)

    def test_vetores_apenas_com_negativos(self):
        vetor = [-2, -1, -3, -5]
        esperado = -1

        resultado_forca_bruta = SomaMaximaForcaBruta(vetor)
        resultado_divisao_conquista = SomaMaximaDivisaoConquista(vetor)

        self._validar_resultado(vetor, resultado_forca_bruta, esperado)
        self._validar_resultado(vetor, resultado_divisao_conquista, esperado)
        self.assertEqual(resultado_forca_bruta, resultado_divisao_conquista)

    def test_vetor_de_tamanho_um(self):
        vetor = [5]
        esperado = 5

        resultado_forca_bruta = SomaMaximaForcaBruta(vetor)
        resultado_divisao_conquista = SomaMaximaDivisaoConquista(vetor)

        self._validar_resultado(vetor, resultado_forca_bruta, esperado)
        self._validar_resultado(vetor, resultado_divisao_conquista, esperado)
        self.assertEqual(resultado_forca_bruta, resultado_divisao_conquista)

    def test_empates(self):
        casos = [
            ([3, -10, 3], 3),
            ([4, 4, -20, 4, 4], 8),
            ([2, -5, 2], 2),
        ]

        for vetor, soma_esperada in casos:
            resultado_forca_bruta = SomaMaximaForcaBruta(vetor)
            resultado_divisao_conquista = SomaMaximaDivisaoConquista(vetor)

            self._validar_resultado(vetor, resultado_forca_bruta, soma_esperada)
            self._validar_resultado(vetor, resultado_divisao_conquista, soma_esperada)
            self.assertEqual(resultado_forca_bruta[0], resultado_divisao_conquista[0])

    def test_vetor_vazio(self):
        vetor = []
        esperado = (0, -1, -1)

        resultado_forca_bruta = SomaMaximaForcaBruta(vetor)
        resultado_divisao_conquista = SomaMaximaDivisaoConquista(vetor)

        self.assertEqual(resultado_forca_bruta, esperado)
        self.assertEqual(resultado_divisao_conquista, esperado)

    def test_algoritmos_concordam(self):
        vetores = [
            [1, -2, 3, 4, -1],
            [-5, -2, -8, -1],
            [2, 2, -1, 2, 2],
            [-1, 4, -2, 4, -1],
            [0, 0, 0],
            [7],
        ]

        for vetor in vetores:
            resultado_forca_bruta = SomaMaximaForcaBruta(vetor)
            resultado_divisao_conquista = SomaMaximaDivisaoConquista(vetor)
            self.assertEqual(resultado_forca_bruta[0], resultado_divisao_conquista[0])
            self._validar_resultado(vetor, resultado_forca_bruta, resultado_forca_bruta[0])
            self._validar_resultado(vetor, resultado_divisao_conquista, resultado_divisao_conquista[0])


if __name__ == "__main__":
    conjunto_testes = unittest.TestLoader().loadTestsFromTestCase(TesteSomaMaxima)
    executor = unittest.TextTestRunner(verbosity=2)
    executor.run(conjunto_testes)

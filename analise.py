import contextlib
import csv
import ctypes
import io
import os
import platform
import random
import sys
import time
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8", line_buffering=True, errors="replace")

from Algoritmos import etapa1
from Algoritmos import etapa2

# Desliga os logs  para nao interferir na medicao
etapa1.logLigado = False
etapa2.logLigado = False

tamanhos = [100, 200, 400, 800, 1600, 3200, 6400]
execucaoPorTamanho = 5
pastaResultados = "resultados"


def _memoria_total():
    if os.name != "nt":
        return "nao informado"

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", ctypes.c_ulong),
            ("dwMemoryLoad", ctypes.c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    memoria = MEMORYSTATUSEX()
    memoria.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memoria)):
        return f"{memoria.ullTotalPhys / (1024 ** 3):.1f} GB"
    return "nao informado"


def obter_configuracao_maquina():
    return {
        "Sistema operacional": platform.system(),
        "Versao": platform.release(),
        "Plataforma": platform.platform(),
        "Maquina": platform.machine(),
        "Processador": platform.processor() or "nao informado",
        "Nucleos logicos": os.cpu_count() or "nao informado",
        "Memoria RAM": _memoria_total(),
        "Python": f"{platform.python_implementation()} {platform.python_version()}",
        "Data/hora da medicao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
    }


def salvar_configuracao(configuracao, nome_arquivo=None):
    if nome_arquivo is None:
        nome_arquivo = os.path.join(pastaResultados, "configuracao_maquina.txt")
    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("CONFIGURACAO DA MAQUINA UTILIZADA\n")
        arquivo.write("=" * 40 + "\n")
        for chave, valor in configuracao.items():
            arquivo.write(f"{chave}: {valor}\n")


def gerar_vetor(tamanho):
    return [random.randint(-1000, 1000) for _ in range(tamanho)]


def gerar_pontos_aleatorios(tamanho, faixa_x=(0, 1000), faixa_y=(0, 1000)):
    pontos = []
    for _ in range(tamanho):
        coordenada_x = random.uniform(faixa_x[0], faixa_x[1])
        coordenada_y = random.uniform(faixa_y[0], faixa_y[1])
        pontos.append((coordenada_x, coordenada_y))
    return pontos


def medir_tempo(funcao, argumento):
    inicio = time.perf_counter()
    with contextlib.redirect_stdout(io.StringIO()):
        funcao(argumento)
    return time.perf_counter() - inicio


def validar_algoritmos():
    random.seed(123)
    for _ in range(20):
        quantidade = random.randint(1, 100)
        vetor = gerar_vetor(quantidade)
        soma_forca_bruta = etapa1.SomaMaximaForcaBruta(vetor)[0]
        soma_divisao_conquista = etapa1.SomaMaximaDivisaoConquista(vetor)[0]
        if soma_forca_bruta != soma_divisao_conquista:
            raise RuntimeError("Etapa 1: algoritmos divergiram na validacao inicial")

        pontos = gerar_pontos_aleatorios(quantidade)
        distancia_forca_bruta = etapa2.ParMaisProximoForcaBruta(pontos)[0]
        distancia_divisao_conquista = etapa2.ParMaisProximoDivisaoConquista(pontos)[0]
        if abs(distancia_forca_bruta - distancia_divisao_conquista) > 1e-9:
            raise RuntimeError("Etapa 2: algoritmos divergiram na validacao inicial")

    print("Validacao inicial concluida: forca bruta e divisao e conquista concordam.")


def executar_medicoes_etapa1():
    resultados = []

    print("\nEtapa 1 - Subarranjo de Soma Maxima")
    print("-" * 58)
    print(f"{'Tamanho N':<12} | {'Tempo BF (s)':<18} | {'Tempo DC (s)':<18}")
    print("-" * 58)

    for tamanho in tamanhos:
        tempos_forca_bruta = []
        tempos_divisao_conquista = []

        for execucao in range(1, execucaoPorTamanho + 1):
            vetor = gerar_vetor(tamanho)

            tempo_forca_bruta = medir_tempo(etapa1.SomaMaximaForcaBruta, vetor)
            tempo_divisao_conquista = medir_tempo(etapa1.SomaMaximaDivisaoConquista, vetor)

            tempos_forca_bruta.append(tempo_forca_bruta)
            tempos_divisao_conquista.append(tempo_divisao_conquista)
            resultados.append((tamanho, execucao, tempo_forca_bruta, tempo_divisao_conquista))

        media_forca_bruta = sum(tempos_forca_bruta) / len(tempos_forca_bruta)
        media_divisao_conquista = sum(tempos_divisao_conquista) / len(tempos_divisao_conquista)
        print(f"{tamanho:<12} | {media_forca_bruta:<18.6f} | {media_divisao_conquista:<18.6f}")

    print("-" * 58)
    return resultados


def executar_medicoes_etapa2():
    resultados = []

    print("\nEtapa 2 - Par de Pontos Mais Proximos")
    print("-" * 58)
    print(f"{'Tamanho N':<12} | {'Tempo BF (s)':<18} | {'Tempo DC (s)':<18}")
    print("-" * 58)

    for tamanho in tamanhos:
        tempos_forca_bruta = []
        tempos_divisao_conquista = []

        for execucao in range(1, execucaoPorTamanho + 1):
            pontos = gerar_pontos_aleatorios(tamanho)

            tempo_forca_bruta = medir_tempo(etapa2.ParMaisProximoForcaBruta, pontos)
            tempo_divisao_conquista = medir_tempo(etapa2.ParMaisProximoDivisaoConquista, pontos)

            tempos_forca_bruta.append(tempo_forca_bruta)
            tempos_divisao_conquista.append(tempo_divisao_conquista)
            resultados.append((tamanho, execucao, tempo_forca_bruta, tempo_divisao_conquista))

        media_forca_bruta = sum(tempos_forca_bruta) / len(tempos_forca_bruta)
        media_divisao_conquista = sum(tempos_divisao_conquista) / len(tempos_divisao_conquista)
        print(f"{tamanho:<12} | {media_forca_bruta:<18.6f} | {media_divisao_conquista:<18.6f}")

    print("-" * 58)
    return resultados


def salvar_csv(nome_arquivo, resultados):
    with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(
            ["N", "Execucao", "Tempo_Forca_Bruta", "Tempo_Divisao_Conquista"]
        )
        for tamanho, execucao, tempo_forca_bruta, tempo_divisao_conquista in resultados:
            texto_forca_bruta = "" if tempo_forca_bruta is None else f"{tempo_forca_bruta:.9f}"
            escritor.writerow(
                [tamanho, execucao, texto_forca_bruta, f"{tempo_divisao_conquista:.9f}"]
            )


def principal():
    print("Analise experimental - Divisao e Conquista")
    print("=" * 58)

    os.makedirs(pastaResultados, exist_ok=True)

    configuracao = obter_configuracao_maquina()
    print("Configuracao da maquina:")
    for chave, valor in configuracao.items():
        print(f"  {chave}: {valor}")
    salvar_configuracao(configuracao)

    validar_algoritmos()

    random.seed(2026)
    resultados_etapa1 = executar_medicoes_etapa1()
    salvar_csv(os.path.join(pastaResultados, "resultados_etapa1.csv"), resultados_etapa1)

    random.seed(2027)
    resultados_etapa2 = executar_medicoes_etapa2()
    salvar_csv(os.path.join(pastaResultados, "resultados_etapa2.csv"), resultados_etapa2)



if __name__ == "__main__":
    principal()

import csv
import os
from html import escape

LARGURA = 960
ALTURA = 560
MARGEM_ESQUERDA = 100
MARGEM_DIREITA = 40
MARGEM_TOPO = 65
MARGEM_BASE = 80

COR_FUNDO = "#ffffff"
COR_AREA = "#f7f9fc"
COR_EIXO = "#333333"
COR_GRADE = "#d9dee7"
COR_FORCA_BRUTA = "#c0392b"
COR_DIVISAO_CONQUISTA = "#1f4e79"


def ler_medias(caminho):
    grupos = {"forca_bruta": {}, "divisao_conquista": {}}

    with open(caminho, newline="", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            tamanho = int(linha["N"])
            for chave, coluna in (
                ("forca_bruta", "Tempo_Forca_Bruta"),
                ("divisao_conquista", "Tempo_Divisao_Conquista"),
            ):
                texto = (linha.get(coluna) or "").strip()
                if not texto or texto.lower() == "nan":
                    continue
                grupos[chave].setdefault(tamanho, []).append(float(texto))

    medias = {}
    for chave, por_tamanho in grupos.items():
        medias[chave] = sorted(
            (tamanho, sum(valores) / len(valores))
            for tamanho, valores in por_tamanho.items()
        )
    return medias


def formatar_tempo(valor):
    if valor == 0:
        return "0"
    if valor >= 1:
        return f"{valor:.2f}"
    if valor >= 0.01:
        return f"{valor:.3f}"
    return f"{valor:.1e}"


def gerar_svg(medias, titulo, nome_arquivo, nota=""):
    series = [
        ("Forca bruta", COR_FORCA_BRUTA, medias.get("forca_bruta", [])),
        ("Divisao e conquista", COR_DIVISAO_CONQUISTA, medias.get("divisao_conquista", [])),
    ]

    pontos_validos = [
        (rotulo, cor, pontos) for rotulo, cor, pontos in series if pontos
    ]

    if not pontos_validos:
        print(f"Sem dados suficientes para gerar {nome_arquivo}.")
        return

    todos_x = [tamanho for _, _, pontos in pontos_validos for tamanho, _ in pontos]
    todos_y = [tempo for _, _, pontos in pontos_validos for _, tempo in pontos]

    minimo_x, maximo_x = min(todos_x), max(todos_x)
    if minimo_x == maximo_x:
        minimo_x -= 1
        maximo_x += 1
    margem_x = (maximo_x - minimo_x) * 0.05
    minimo_x -= margem_x
    maximo_x += margem_x

    minimo_y = 0
    maximo_y = max(todos_y)
    maximo_y = maximo_y * 1.08 if maximo_y > 0 else 1

    area_x0 = MARGEM_ESQUERDA
    area_x1 = LARGURA - MARGEM_DIREITA
    area_y0 = MARGEM_TOPO
    area_y1 = ALTURA - MARGEM_BASE

    def posicao_x(tamanho):
        return area_x0 + (tamanho - minimo_x) / (maximo_x - minimo_x) * (area_x1 - area_x0)

    def posicao_y(tempo):
        return area_y1 - (tempo - minimo_y) / (maximo_y - minimo_y) * (area_y1 - area_y0)

    partes = []
    partes.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{LARGURA}" height="{ALTURA}" '
        f'viewBox="0 0 {LARGURA} {ALTURA}" role="img" aria-label="{escape(titulo)}">'
    )
    partes.append(f'<rect width="100%" height="100%" fill="{COR_FUNDO}"/>')
    partes.append(
        f'<text x="{LARGURA / 2:.1f}" y="32" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="20" font-weight="bold" fill="#1a1a1a">'
        f"{escape(titulo)}</text>"
    )
    partes.append(
        f'<rect x="{area_x0}" y="{area_y0}" width="{area_x1 - area_x0}" '
        f'height="{area_y1 - area_y0}" fill="{COR_AREA}" stroke="{COR_GRADE}"/>'
    )

    for indice in range(6):
        valor_y = minimo_y + (maximo_y - minimo_y) * indice / 5
        y = area_y1 - (valor_y - minimo_y) / (maximo_y - minimo_y) * (area_y1 - area_y0)
        partes.append(
            f'<line x1="{area_x0}" y1="{y:.2f}" x2="{area_x1}" y2="{y:.2f}" '
            f'stroke="{COR_GRADE}" stroke-width="1"/>'
        )
        partes.append(
            f'<text x="{area_x0 - 12}" y="{y + 4:.2f}" text-anchor="end" '
            f'font-family="Arial, sans-serif" font-size="12" fill="{COR_EIXO}">'
            f"{formatar_tempo(valor_y)}</text>"
        )

    tamanhos = sorted(set(todos_x))
    for tamanho in tamanhos:
        x = posicao_x(tamanho)
        partes.append(
            f'<line x1="{x:.2f}" y1="{area_y0}" x2="{x:.2f}" y2="{area_y1}" '
            f'stroke="{COR_GRADE}" stroke-width="1" stroke-dasharray="4 3"/>'
        )
        partes.append(
            f'<text x="{x:.2f}" y="{area_y1 + 22}" text-anchor="middle" '
            f'font-family="Arial, sans-serif" font-size="12" fill="{COR_EIXO}">{tamanho}</text>'
        )

    partes.append(
        f'<line x1="{area_x0}" y1="{area_y1}" x2="{area_x1}" y2="{area_y1}" '
        f'stroke="{COR_EIXO}" stroke-width="1.5"/>'
    )
    partes.append(
        f'<line x1="{area_x0}" y1="{area_y0}" x2="{area_x0}" y2="{area_y1}" '
        f'stroke="{COR_EIXO}" stroke-width="1.5"/>'
    )
    partes.append(
        f'<text x="{(area_x0 + area_x1) / 2:.1f}" y="{ALTURA - 30}" text-anchor="middle" '
        f'font-family="Arial, sans-serif" font-size="14" fill="{COR_EIXO}">'
        "Tamanho da entrada (N)</text>"
    )
    partes.append(
        f'<text x="28" y="{(area_y0 + area_y1) / 2:.1f}" text-anchor="middle" '
        f'transform="rotate(-90 28 {(area_y0 + area_y1) / 2:.1f})" '
        f'font-family="Arial, sans-serif" font-size="14" fill="{COR_EIXO}">'
        "Tempo medio (s)</text>"
    )

    for rotulo, cor, pontos in pontos_validos:
        coordenadas = [(posicao_x(tamanho), posicao_y(tempo)) for tamanho, tempo in pontos]
        if len(coordenadas) > 1:
            texto_pontos = " ".join(f"{x:.2f},{y:.2f}" for x, y in coordenadas)
            partes.append(
                f'<polyline points="{texto_pontos}" fill="none" stroke="{cor}" stroke-width="2.5"/>'
            )
        for x, y in coordenadas:
            partes.append(
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4.5" fill="{cor}" '
                f'stroke="#ffffff" stroke-width="1.2"/>'
            )

    for indice, (rotulo, cor, _) in enumerate(series):
        y = 88 + indice * 24
        partes.append(
            f'<line x1="{area_x1 - 250}" y1="{y}" x2="{area_x1 - 220}" y2="{y}" '
            f'stroke="{cor}" stroke-width="3"/>'
        )
        partes.append(f'<circle cx="{area_x1 - 235}" cy="{y}" r="4" fill="{cor}"/>')
        partes.append(
            f'<text x="{area_x1 - 212}" y="{y + 4}" font-family="Arial, sans-serif" '
            f'font-size="12" fill="{COR_EIXO}">{escape(rotulo)}</text>'
        )

    if nota:
        partes.append(
            f'<text x="{area_x0}" y="{ALTURA - 10}" font-family="Arial, sans-serif" '
            f'font-size="11" fill="#555555">{escape(nota)}</text>'
        )

    partes.append("</svg>")

    with open(nome_arquivo, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(partes))

    print(f"Grafico gerado: {nome_arquivo}")


def principal():
    pasta_resultados = "resultados"
    arquivos = [
        (1, "Subarranjo de Soma Maxima", os.path.join(pasta_resultados, "resultados_etapa1.csv")),
        (2, "Par de Pontos Mais Proximos", os.path.join(pasta_resultados, "resultados_etapa2.csv")),
    ]

    for etapa, titulo, arquivo in arquivos:
        if not os.path.exists(arquivo):
            print(f"Arquivo {arquivo} nao encontrado. Execute 'python analise.py' primeiro.")
            continue

        medias = ler_medias(arquivo)
        gerar_svg(
            medias,
            f"Etapa {etapa} - {titulo}",
            os.path.join(pasta_resultados, f"grafico_etapa{etapa}.svg"),
            nota="",
        )


if __name__ == "__main__":
    principal()

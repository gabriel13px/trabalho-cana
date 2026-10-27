import math

logLigado = True

def log(mensagem):
    if logLigado:
        print(mensagem)

def FormatarPonto(ponto):
    if ponto is None:
        return "(nenhum)"
    return f"({ponto[0]:g}, {ponto[1]:g})"

def FormatarPontos(pontos):
    if not pontos:
        return "(vazio)"
    return " | ".join(FormatarPonto(ponto) for ponto in pontos)

def FormatarPar(ponto1, ponto2):
    if ponto1 is None or ponto2 is None:
        return "[ (nenhum) <-> (nenhum) ]"
    return f"[ {FormatarPonto(ponto1)} <-> {FormatarPonto(ponto2)} ]"

def FormatarDistancia(distancia):
    if distancia == float('inf'):
        return "inf"
    return f"{distancia:.6g}"

def Distancia(ponto1, ponto2):
    return math.sqrt((ponto1[0] - ponto2[0])**2 + (ponto1[1] - ponto2[1])**2)

def ParMaisProximoForcaBruta(pontos, prefixo=""):
    tamanho = len(pontos)
    log(f"{prefixo}Iniciando forca bruta | N={tamanho} | pontos=[ {FormatarPontos(pontos)} ]")
    if tamanho < 2:
        log(f"{prefixo}Forca bruta concluida | pontos=[ {FormatarPontos(pontos)} ] | distancia=inf")
        return float('inf'), None, None

    distancia_minima = float('inf')
    ponto1_mais_proximo = None
    ponto2_mais_proximo = None

    for indice in range(tamanho):
        if logLigado:
            log(f"{prefixo}i={indice} | ponto={FormatarPonto(pontos[indice])}")
        for outro_indice in range(indice + 1, tamanho):
            distancia = Distancia(pontos[indice], pontos[outro_indice])
            atualizou = False
            if distancia < distancia_minima:
                distancia_minima = distancia
                ponto1_mais_proximo = pontos[indice]
                ponto2_mais_proximo = pontos[outro_indice]
                atualizou = True
            if logLigado:
                marcador = " (novo melhor)" if atualizou else ""
                log(
                    f"{prefixo}  j={outro_indice} | "
                    f"par={FormatarPar(pontos[indice], pontos[outro_indice])} "
                    f"dist={FormatarDistancia(distancia)} | "
                    f"melhor={FormatarPar(ponto1_mais_proximo, ponto2_mais_proximo)} "
                    f"dist={FormatarDistancia(distancia_minima)}{marcador}"
                )
    log(
        f"{prefixo}Forca bruta concluida | "
        f"melhor={FormatarPar(ponto1_mais_proximo, ponto2_mais_proximo)} | "
        f"dist={FormatarDistancia(distancia_minima)}"
    )
    return distancia_minima, ponto1_mais_proximo, ponto2_mais_proximo

def ParMaisProximoRecursivo(pontos_x, pontos_y, nivel=0):
    prefixo = "  " * nivel
    tamanho = len(pontos_x)
    if tamanho <= 3:
        if logLigado:
            log(f"{prefixo}base | N={tamanho} (forca bruta)")
        distancia_minima, ponto1, ponto2 = ParMaisProximoForcaBruta(
            pontos_x, prefixo + "  "
        )
        if logLigado:
            log(
                f"{prefixo}base concluida | "
                f"melhor={FormatarPar(ponto1, ponto2)} | "
                f"dist={FormatarDistancia(distancia_minima)}"
            )
        return distancia_minima, ponto1, ponto2

    meio = tamanho // 2
    mediana_x = pontos_x[meio][0]

    pontos_x_esquerda = pontos_x[:meio]
    pontos_x_direita = pontos_x[meio:]

    pontos_y_esquerda = []
    pontos_y_direita = []
    for ponto in pontos_y:
        if ponto[0] <= mediana_x:
            pontos_y_esquerda.append(ponto)
        else:
            pontos_y_direita.append(ponto)

    if logLigado:
        log(
            f"{prefixo}dividindo | N={tamanho} | eixo_x={mediana_x:g} | "
            f"esquerda=[ {FormatarPontos(pontos_x_esquerda)} ] | "
            f"direita=[ {FormatarPontos(pontos_x_direita)} ]"
        )

    (distancia_esquerda, ponto1_esquerda, ponto2_esquerda) = ParMaisProximoRecursivo(
        pontos_x_esquerda, pontos_y_esquerda, nivel + 1
    )
    (distancia_direita, ponto1_direita, ponto2_direita) = ParMaisProximoRecursivo(
        pontos_x_direita, pontos_y_direita, nivel + 1
    )

    if logLigado:
        log(
            f"{prefixo}esquerda -> melhor={FormatarPar(ponto1_esquerda, ponto2_esquerda)} | "
            f"dist={FormatarDistancia(distancia_esquerda)}"
        )
        log(
            f"{prefixo}direita  -> melhor={FormatarPar(ponto1_direita, ponto2_direita)} | "
            f"dist={FormatarDistancia(distancia_direita)}"
        )

    distancia_minima = distancia_esquerda
    par_mais_proximo = (ponto1_esquerda, ponto2_esquerda)

    if distancia_direita < distancia_minima:
        distancia_minima = distancia_direita
        par_mais_proximo = (ponto1_direita, ponto2_direita)

   
    faixa_pontos = [ponto for ponto in pontos_y if abs(ponto[0] - mediana_x) < distancia_minima]
    if logLigado:
        log(
            f"{prefixo}faixa central | faixa=[ {FormatarPontos(faixa_pontos)} ] | "
            f"delta={FormatarDistancia(distancia_minima)} | "
            f"melhor={FormatarPar(par_mais_proximo[0], par_mais_proximo[1])}"
        )

    for indice in range(len(faixa_pontos)):
        for vizinho in range(indice + 1, min(indice + 8, len(faixa_pontos))):
            distancia = Distancia(faixa_pontos[indice], faixa_pontos[vizinho])
            atualizou = False
            if distancia < distancia_minima:
                distancia_minima = distancia
                par_mais_proximo = (faixa_pontos[indice], faixa_pontos[vizinho])
                atualizou = True
            if logLigado:
                marcador = " (novo melhor)" if atualizou else ""
                log(
                    f"{prefixo}  faixa i={indice} j={vizinho} | "
                    f"par={FormatarPar(faixa_pontos[indice], faixa_pontos[vizinho])} | "
                    f"dist={FormatarDistancia(distancia)} | "
                    f"melhor={FormatarPar(par_mais_proximo[0], par_mais_proximo[1])} "
                    f"dist={FormatarDistancia(distancia_minima)}{marcador}"
                )

    if logLigado:
        log(
            f"{prefixo}retorno | N={tamanho} | "
            f"melhor={FormatarPar(par_mais_proximo[0], par_mais_proximo[1])} | "
            f"dist={FormatarDistancia(distancia_minima)}"
        )
    return distancia_minima, par_mais_proximo[0], par_mais_proximo[1]

def ParMaisProximoDivisaoConquista(pontos):
    tamanho = len(pontos)
    log(f"Iniciando divisao e conquista | N={tamanho} | pontos=[ {FormatarPontos(pontos)} ]")
    if tamanho < 2:
        log(f"Divisao e conquista concluida | pontos=[ {FormatarPontos(pontos)} ] | distancia=inf")
        return float('inf'), None, None


    pontos_x = sorted(pontos, key=lambda ponto: ponto[0])
    pontos_y = sorted(pontos, key=lambda ponto: ponto[1])

    return ParMaisProximoRecursivo(pontos_x, pontos_y)


def ExemploEtapa2():
    pontos = [(0.0, 0.0), (5.0, 5.0), (1.0, 1.0), (10.0, 10.0)]
    print("Cenario: estacoes de monitoramento com risco de interferencia.")
    print(f"Entrada: N={len(pontos)} | pontos={pontos}")

    distancia, ponto1, ponto2 = ParMaisProximoForcaBruta(pontos)
    print(f"Forca bruta: distancia={distancia:.10g} | estacoes={ponto1} e {ponto2}\n \n")

    distancia, ponto1, ponto2 = ParMaisProximoDivisaoConquista(pontos)
    print(f"Divisao e conquista: distancia={distancia:.10g} | estacoes={ponto1} e {ponto2}")


if __name__ == "__main__":
    ExemploEtapa2()

import math

logLigado = True

def log(mensagem):
    if logLigado:
        print(mensagem)

def FormatarValores(valores):
    if not valores:
        return "(vazio)"
    largura = max(len(str(valor)) for valor in valores)
    return " | ".join(f"{valor:>{largura}}" for valor in valores)

def FormatarTrecho(vetor, inicio, fim):
    if (inicio < 0 or fim < 0 or inicio > fim):
        return "(vazio)"
    return FormatarValores(vetor[inicio:fim + 1])

def FormatarIntervalo(inicio, fim):
    if (inicio < 0 or fim < 0 or inicio > fim):
        return "[-]"
    return f"[{inicio}..{fim}]"

def SomaMaximaForcaBruta(vetor):
    log(f"Iniciando forca bruta | N={len(vetor)} | vetor=[ {FormatarValores(vetor)} ]")
    soma_maxima = -math.inf
    indice_inicio = -1
    indice_fim = -1

    if not vetor:
        log("Forca bruta concluida | vetor=[ (vazio) ] | soma_maxima=0")
        return 0, -1, -1

    for indice in range(len(vetor)):
        if logLigado:
            log(f"i={indice} | valor={vetor[indice]}")
        soma_atual = 0
        for fim in range(indice, len(vetor)):
            soma_atual += vetor[fim]
            atualizou = False
            if soma_atual > soma_maxima:
                soma_maxima = soma_atual
                indice_inicio = indice
                indice_fim = fim
                atualizou = True
            if logLigado:
                marcador = " (novo melhor)" if atualizou else ""
                log(
                    f"  j={fim} | atual=[ {FormatarTrecho(vetor, indice, fim)} ] "
                    f"{FormatarIntervalo(indice, fim)} soma={soma_atual} | "
                    f"melhor=[ {FormatarTrecho(vetor, indice_inicio, indice_fim)} ] "
                    f"{FormatarIntervalo(indice_inicio, indice_fim)} "
                    f"soma={soma_maxima}{marcador}"
                )
    log(
        f"Forca bruta concluida | melhor=[ {FormatarTrecho(vetor, indice_inicio, indice_fim)} ] "
        f"{FormatarIntervalo(indice_inicio, indice_fim)} soma={soma_maxima}"
    )
    return (soma_maxima, indice_inicio, indice_fim)

def SomaMaximaCruzandoMeio(vetor, inicio, meio, fim, nivel=0):
    prefixo = "  " * nivel
    if logLigado:
        log(
            f"{prefixo}cruzando {FormatarIntervalo(inicio, fim)} | "
            f"esquerda=[ {FormatarTrecho(vetor, inicio, meio)} ] | "
            f"direita=[ {FormatarTrecho(vetor, meio + 1, fim)} ]"
        )
    soma_esquerda = -math.inf
    soma_atual = 0
    indice_esquerda = meio

    for indice in range(meio, inicio - 1, -1):
        soma_atual += vetor[indice]
        if soma_atual > soma_esquerda:
            soma_esquerda = soma_atual
            indice_esquerda = indice
        if logLigado:
            log(
                f"{prefixo}  esquerda i={indice} | "
                f"atual=[ {FormatarTrecho(vetor, indice, meio)} ] "
                f"soma={soma_atual} | melhor_esq={soma_esquerda} "
                f"{FormatarIntervalo(indice_esquerda, meio)}"
            )

    soma_direita = -math.inf
    soma_atual = 0
    indice_direita = meio

    for indice in range(meio + 1, fim + 1):
        soma_atual += vetor[indice]
        if soma_atual > soma_direita:
            soma_direita = soma_atual
            indice_direita = indice
        if logLigado:
            log(
                f"{prefixo}  direita i={indice} | "
                f"atual=[ {FormatarTrecho(vetor, meio + 1, indice)} ] "
                f"soma={soma_atual} | melhor_dir={soma_direita} "
                f"{FormatarIntervalo(meio + 1, indice_direita)}"
            )

    soma_cruzada = soma_esquerda + soma_direita
    if logLigado:
        log(
            f"{prefixo}  cruzado | atual=[ {FormatarTrecho(vetor, indice_esquerda, indice_direita)} ] "
            f"{FormatarIntervalo(indice_esquerda, indice_direita)} soma={soma_cruzada}"
        )
    return (soma_cruzada, indice_esquerda, indice_direita)

def SomaMaximaRecursiva(vetor, inicio, fim, nivel=0):
    prefixo = "  " * nivel
    if logLigado:
        log(
            f"{prefixo}dividindo {FormatarIntervalo(inicio, fim)} | "
            f"trecho=[ {FormatarTrecho(vetor, inicio, fim)} ]"
        )

    if inicio == fim:
        if logLigado:
            log(
                f"{prefixo}base {FormatarIntervalo(inicio, fim)} | "
                f"trecho=[ {FormatarTrecho(vetor, inicio, fim)} ]"
            )
        return (vetor[inicio], inicio, fim)
    meio = (inicio + fim) // 2
    soma_esq, inicio_esq, fim_esq = SomaMaximaRecursiva(vetor, inicio, meio, nivel + 1)
    soma_dir, inicio_dir, fim_dir = SomaMaximaRecursiva(vetor, meio + 1, fim, nivel + 1)
    soma_cruzada, inicio_cruz, fim_cruz = SomaMaximaCruzandoMeio(
        vetor, inicio, meio, fim, nivel + 1
    )

    if logLigado:
        log(
            f"{prefixo}candidatos {FormatarIntervalo(inicio, fim)} | "
            f"esq=[ {FormatarTrecho(vetor, inicio_esq, fim_esq)} ] soma={soma_esq} | "
            f"dir=[ {FormatarTrecho(vetor, inicio_dir, fim_dir)} ] soma={soma_dir} | "
            f"cruz=[ {FormatarTrecho(vetor, inicio_cruz, fim_cruz)} ] soma={soma_cruzada}"
        )

    if soma_esq >= soma_dir and soma_esq >= soma_cruzada:
        resultado = (soma_esq, inicio_esq, fim_esq)
    elif soma_dir >= soma_esq and soma_dir >= soma_cruzada:
        resultado = (soma_dir, inicio_dir, fim_dir)
    else:
        resultado = (soma_cruzada, inicio_cruz, fim_cruz)

    if logLigado:
        log(
            f"{prefixo}retorno {FormatarIntervalo(inicio, fim)} | "
            f"melhor=[ {FormatarTrecho(vetor, resultado[1], resultado[2])} ] "
            f"{FormatarIntervalo(resultado[1], resultado[2])} soma={resultado[0]}"
        )
    return resultado

def SomaMaximaDivisaoConquista(vetor):
    log(f"Iniciando divisao e conquista | N={len(vetor)} | vetor=[ {FormatarValores(vetor)} ]")
    if not vetor:
        log("Divisao e conquista concluida | vetor=[ (vazio) ] | soma_maxima=0")
        return 0, -1, -1
    return SomaMaximaRecursiva(vetor, 0, len(vetor) - 1)


def DemonstracaoEtapa1():
    vetor = [1, -2, 3, 4, -1]
    print("Cenario: corretora registrando a variacao diaria do preco de uma acao.")
    print(f"Entrada: N={len(vetor)} | variacoes={vetor}")

    soma, inicio, fim = SomaMaximaForcaBruta(vetor)
    print(f"Forca bruta: soma_maxima={soma}, inicio={inicio}, fim={fim}")
    print()

    soma, inicio, fim = SomaMaximaDivisaoConquista(vetor)
    print(f"Divisao e conquista: soma_maxima={soma}, inicio={inicio}, fim={fim}")


if __name__ == "__main__":
    DemonstracaoEtapa1()

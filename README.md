# Trabalho Prático — Divisão e Conquista

Trabalho desenvolvido para a disciplina de Análise de Algoritmos, com o objetivo de implementar e comparar algoritmos baseados nas técnicas de força bruta e divisão e conquista.

O projeto aborda dois problemas: **Subarranjo de Soma Máxima** e **Par de Pontos Mais Próximos**, incluindo testes automatizados e análise experimental de desempenho.

## 1. Algoritmos implementados

### Subarranjo de Soma Máxima

O objetivo é encontrar o intervalo contínuo de um vetor que possui a maior soma possível.

- **Força bruta:** testa todos os intervalos possíveis. Complexidade O(n²).
- **Divisão e conquista:** divide o vetor recursivamente e compara os melhores resultados de cada metade com o intervalo que atravessa o meio. Complexidade O(n log n).

### Par de Pontos Mais Próximos

O objetivo é encontrar a menor distância entre dois pontos em um plano cartesiano.

- **Força bruta:** compara todos os pares de pontos. Complexidade O(n²).
- **Divisão e conquista:** divide os pontos em duas regiões e verifica os possíveis pares mais próximos, incluindo os que atravessam a divisão. Complexidade O(n log n).

## 2. Estrutura do projeto

```text
Trabalho-Cana-Divisao-e-Conquista/
├── Algoritmos/
│   ├── etapa1.py             # Subarranjo de soma máxima e demonstração via logs
│   └── etapa2.py             # Par de pontos mais próximos e demonstração via logs
├── testes/
│   ├── test_etapa1.py        # Testes da Etapa 1 (unittest)
│   └── test_etapa2.py        # Testes da Etapa 2 (unittest)
├── resultados/
│   ├── resultados_etapa1.csv
│   ├── resultados_etapa2.csv
│   ├── configuracao_maquina.txt
│   ├── grafico_etapa1.svg
│   └── grafico_etapa2.svg
├── casos_teste.txt           # Casos de teste com entradas e saídas esperadas
├── analise.py                # Medições de tempo e configuração da máquina
├── graficos.py               # Gera os gráficos SVG a partir dos CSVs
└── README.md
```

## 3. Tecnologias utilizadas

- Python 3.12 — implementação dos algoritmos, testes, análise e geração dos gráficos, usando apenas a biblioteca padrão.
- Git e GitHub — versionamento do projeto.

## 4. Como executar

Não é necessário instalar pacotes Python externos.

### Demonstrações

Cada módulo usa um exemplo fixo e registra no console os passos dos algoritmos:

```bash
python -m Algoritmos.etapa1
python -m Algoritmos.etapa2
```

- `etapa1.py` — variações diárias `[1, -2, 3, 4, -1]`; saída esperada `soma_maxima=7, inicio=2, fim=3`.
- `etapa2.py` — estações `[(0, 0), (5, 5), (1, 1), (10, 10)]`; saída esperada `distancia=1.414213562` entre `(0, 0)` e `(1, 1)`.

Para testar outras entradas, importe as funções e chame-as diretamente:

```python
from Algoritmos import etapa1, etapa2

etapa1.SomaMaximaForcaBruta([1, -2, 3, 4, -1])
etapa1.SomaMaximaDivisaoConquista([1, -2, 3, 4, -1])

etapa2.ParMaisProximoForcaBruta([(0, 0), (5, 5), (1, 1), (10, 10)])
etapa2.ParMaisProximoDivisaoConquista([(0, 0), (5, 5), (1, 1), (10, 10)])
```

As funções devolvem:

```text
Etapa 1: (soma_maxima, indice_inicio, indice_fim)
Etapa 2: (distancia, (x1, y1), (x2, y2))
```

### Testes automatizados

```bash
python -m testes.test_etapa1
python -m testes.test_etapa2
```

### Análise experimental

```bash
python analise.py
```

### Gráficos

```bash
python graficos.py
```

## 5. Testes automatizados

O projeto contém testes para verificar a correção dos algoritmos, incluindo situações como:

- vetores apenas com valores negativos;
- vetor de tamanho 1;
- empates entre intervalos com a mesma soma;
- vetor vazio;
- comparação cruzada entre força bruta e divisão e conquista;
- pontos duplicados, coordenadas negativas e pontos alinhados;
- empates no par mais próximo;
- 50 conjuntos aleatórios de pontos comparando as duas implementações.

Os casos de teste e suas justificativas estão documentados no arquivo `casos_teste.txt`.

## 6. Análise experimental

Foram utilizados tamanhos de entrada de 100, 200, 400, 800, 1.600, 3.200 e 6.400 elementos.

Cada algoritmo foi executado cinco vezes por tamanho de entrada, utilizando a média dos tempos, medida com `time.perf_counter()`.

**Arquivos gerados:**

- `resultados/resultados_etapa1.csv` e `resultados/resultados_etapa2.csv` — medições brutas;
- `resultados/configuracao_maquina.txt` — ambiente usado nas medições;
- `resultados/grafico_etapa1.svg` e `resultados/grafico_etapa2.svg` — gráficos de tempos.

## 7. Resultados

Os experimentos permitem observar que, em entradas pequenas, a força bruta pode apresentar menor tempo de execução devido à simplicidade da implementação.

Conforme o tamanho da entrada aumenta, os algoritmos de divisão e conquista tendem a apresentar melhor desempenho, de acordo com suas complexidades assintóticas.

Os dados detalhados estão nos arquivos CSV e nos gráficos da pasta `resultados/`.

## 8. Integrantes

- Gabriel Oliveira da Silva
- Carlyle José de Figueiredo Martins

# Técnicas de Algoritmos — Subset Sum

Projeto  que implementa e compara duas técnicas clássicas de resolução do problema **Soma de Subconjunto (Subset Sum)**: Backtracking e Branch and Bound. O objetivo é analisar o comportamento de cada método por meio de métricas de desempenho coletadas em tempo de execução.

---

## Índice

- [O Problema — Subset Sum](#o-problema--subset-sum)
- [Algoritmos de Solução](#algoritmos-de-solução)
  - [Backtracking](#backtracking)
  - [Branch and Bound](#branch-and-bound)
  - [Comparativo](#comparativo)
- [Como Usar](#como-usar)
  - [Requisitos](#requisitos)
  - [Executando o Projeto](#executando-o-projeto)
  - [Formato de Entrada](#formato-de-entrada)
  - [Usando os Exemplos](#usando-os-exemplos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Métricas Geradas](#métricas-geradas)

---

## O Problema — Subset Sum

Dado um conjunto de **n inteiros positivos** e um valor alvo **T**, o problema pergunta:

> Existe algum subconjunto cujos elementos somam exatamente **T**?

**Exemplo:**

```
Conjunto : {3, 5, 7, 2, 8}
Alvo (T) : 15

Solução  : {3, 5, 7}  →  3 + 5 + 7 = 15  ✓
```

O Subset Sum é um problema **NP-completo**, o que significa que não existe algoritmo de tempo polinomial conhecido para resolvê-lo no caso geral. No pior caso, é preciso explorar todos os 2ⁿ subconjuntos possíveis.

---

## Algoritmos de Solução

### Backtracking

O Backtracking percorre uma **árvore binária de decisão** em profundidade (DFS). Em cada nível, há duas escolhas para o elemento atual: **incluir** ou **excluir**.

```
                     []
                /          \
            [3]              []
           /    \           /    \
        [3,5]  [3]        [5]    []
        ...    ...        ...    ...
```

**Poda aplicada:**

- Se o elemento atual **excede o valor restante** → ramo descartado.
- Se a **soma dos elementos restantes é menor que o alvo restante** → ramo descartado.

| | |
|---|---|
| **Complexidade** | O(2ⁿ) no pior caso |
| **Estrutura** | Recursão em profundidade (DFS) |
| **Melhor caso** | Solução nos primeiros elementos da lista |
| **Pior caso** | Sem solução ou solução apenas no último ramo |

---

### Branch and Bound

O Branch and Bound explora a árvore em largura (BFS) usando uma **fila explícita de estados**. Para cada estado, calcula um **limite superior** antes de expandir.

**Estado:** `(índice, soma_atual, índices_selecionados)`

**Limite superior:**
```
limite_superior = soma_atual + soma(elementos_restantes)
```

**Condições de poda:**

- `soma_atual > alvo` → excedeu, descartar.
- `limite_superior < alvo` → impossível atingir o alvo, descartar.

| | |
|---|---|
| **Complexidade** | O(2ⁿ) no pior caso |
| **Estrutura** | Fila BFS com estados explícitos |
| **Melhor caso** | Poda elimina grandes subárvores cedo |
| **Pior caso** | Muitos caminhos viáveis simultaneamente → fila cresce muito |

---

### Comparativo

| Critério | Backtracking | Branch and Bound |
|---|---|---|
| Estratégia | DFS recursivo | BFS com fila |
| Uso de memória | Baixo (pilha de chamadas) | Mais alto (fila de estados) |
| Velocidade — solução cedo | Rápido | Mais lento (explora por nível) |
| Velocidade — poda eficiente | Bom | Excelente (limite superior preciso) |
| Facilidade de implementação | Alta | Média |

---

## Como Usar

### Requisitos

- Python 3.10 ou superior
- Nenhuma dependência externa

### Executando o Projeto

```bash
python main.py
```

O programa exibirá um menu interativo com três etapas:

```
==================================================
  PROJETO EXPERIMENTAL — TÉCNICAS DE ALGORITMOS
==================================================

Algoritmo:
  1. Subset Sum
Escolha: 1

Método de resolução:
  1. Backtracking
  2. Branch and Bound
Escolha: 1

Tipo de entrada:
  1. Arquivo
  2. Manual
Escolha: 1
```

---

### Formato de Entrada

A entrada segue um formato fixo de **duas linhas**:

```
n T
a1 a2 a3 ... an
```

| Campo | Descrição |
|---|---|
| `n` | Quantidade de elementos no conjunto |
| `T` | Valor alvo (inteiro positivo) |
| `a1 ... an` | Elementos do conjunto (n inteiros positivos) |

**Exemplo:**

```
5 9
3 4 5 8 1
```

> Todos os valores devem ser **inteiros positivos**. O número de elementos na segunda linha deve ser exatamente `n`.

---

### Arquivos Suportados

O projeto aceita apenas arquivos **`.txt`** com o formato de duas linhas descrito acima.

---

### Usando os Exemplos

A pasta `examples/` contém entradas prontas para análise:

```bash
# Ao executar o programa, escolha "Arquivo" e informe o caminho:
Caminho do arquivo: examples/padrao.txt
```

#### Descrição dos exemplos

| Arquivo | n | T | O que demonstra |
|---|---|---|---|
| `padrao.txt` | 8 | 15 | Caso equilibrado para comparação base |
| `solucao_imediata.txt` | 10 | 12 | Solução nos 2 primeiros elementos — **ponto forte do Backtracking** |
| `sem_solucao.txt` | 12 | 79 | Alvo impossível (soma total = 78) — **pior caso para ambos** |
| `poda_maxima.txt` | 10 | 5 | Elementos grandes, alvo pequeno — **máxima poda em ambos** |
| `solucao_no_final.txt` | 10 | 9 | Solução apenas no último elemento — **ponto fraco do Backtracking** |
| `fila_grande_bb.txt` | 15 | 30 | Muitos caminhos viáveis — **ponto fraco do Branch and Bound** |

---

## Estrutura do Projeto

```
.
├── main.py                     # Ponto de entrada e menu interativo
├── io_handler.py               # Leitura e parsing de entrada (manual e arquivo)
├── metrics.py                  # Exibição de resultados e métricas
├── algorithms/
│   ├── __init__.py             # Marca o diretório como pacote Python
│   ├── backtracking.py         # Implementação do Backtracking
│   └── branch_bound.py         # Implementação do Branch and Bound
└── examples/
    ├── padrao.txt
    ├── solucao_imediata.txt
    ├── sem_solucao.txt
    ├── poda_maxima.txt
    ├── solucao_no_final.txt
    └── fila_grande_bb.txt
```

---

## Métricas Geradas

Após a execução, o programa exibe três blocos de análise:

**Análise Comportamental**
- Estados explorados — total de nós visitados na árvore
- Estados podados — ramos descartados antes de expandir
- Eficiência de poda — porcentagem de ramos eliminados
- Profundidade máxima *(Backtracking)* ou Tamanho máximo da fila *(Branch and Bound)*

**Métricas de Qualidade**
- Qualidade da solução — ótima (exata) ou sem solução
- Tempo de execução em milissegundos
- Pico de memória em KB

**Análise de Complexidade**
- Complexidade teórica
- Justificativa detalhada do comportamento do algoritmo

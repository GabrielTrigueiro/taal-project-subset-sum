# Técnicas de Algoritmos — Subset Sum

Projeto que implementa e compara quatro técnicas clássicas de resolução do problema **Soma de Subconjunto (Subset Sum)**: Backtracking, Branch and Bound, Programação Dinâmica e Estratégia Gulosa. O objetivo é analisar o comportamento de cada método por meio de métricas de desempenho coletadas em tempo de execução.

---

## Índice

- [O Problema — Subset Sum](#o-problema--subset-sum)
- [Algoritmos de Solução](#algoritmos-de-solução)
  - [Backtracking](#backtracking)
  - [Branch and Bound](#branch-and-bound)
  - [Programação Dinâmica](#programação-dinâmica)
  - [Estratégia Gulosa](#estratégia-gulosa)
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

### Programação Dinâmica

A Programação Dinâmica constrói uma **tabela booleana `dp[i][s]`** onde cada célula indica se é possível atingir a soma `s` usando os primeiros `i` elementos.

**Transição:**
```
dp[i][s] = dp[i-1][s]                            # não incluir elemento i
           OR dp[i-1][s - nums[i-1]]  (se s ≥ nums[i-1])  # incluir elemento i
```

**Caso base:** `dp[i][0] = True` para todo `i` (subconjunto vazio tem soma 0).

A solução é **reconstruída** percorrendo a tabela de trás para frente após o preenchimento.

| | |
|---|---|
| **Complexidade de tempo** | O(n × T) — pseudopolinomial |
| **Complexidade de espaço** | O(n × T) para reconstrução |
| **Estrutura** | Tabela 2D preenchida de forma bottom-up |
| **Garante solução ótima** | Sim — sempre encontra se existir |
| **Observação** | Eficiente para T pequeno; cresce linearmente com o alvo |

---

### Estratégia Gulosa

A Estratégia Gulosa ordena os elementos em **ordem decrescente** e, a cada passo, inclui o maior elemento que ainda cabe no valor restante.

**Critério guloso:** "escolha sempre o maior elemento que não ultrapassa o restante".

> ⚠️ **Atenção:** A Estratégia Gulosa **não garante** encontrar uma solução mesmo quando ela existe. É uma heurística que pode falhar em casos onde a solução exige priorizar elementos menores.

**Exemplo de falha:**
```
Conjunto = {10, 7, 6, 5, 3},  Alvo = 11
Guloso escolhe 10 (restante = 1) → nenhum elemento cabe → falha.
Solução real: {6, 5} → 6 + 5 = 11  ✓
```

| | |
|---|---|
| **Complexidade** | O(n log n) — dominada pela ordenação |
| **Estrutura** | Varredura linear após ordenação |
| **Garante solução ótima** | Não — heurística sem garantia de completude |
| **Melhor caso** | Elementos grandes encaixam diretamente no alvo |
| **Pior caso** | Escolha gulosa bloqueia todos os caminhos válidos |

---

### Comparativo

| Critério | Backtracking | Branch and Bound | Prog. Dinâmica | Est. Gulosa |
|---|---|---|---|---|
| Estratégia | DFS recursivo | BFS com fila | Tabela bottom-up | Ordenação + varredura |
| Complexidade | O(2ⁿ) | O(2ⁿ) pior caso | O(n × T) | O(n log n) |
| Uso de memória | Baixo (pilha) | Mais alto (fila) | O(n × T) — tabela | O(n) — ordenação |
| Solução ótima garantida | Sim | Sim | Sim | Não |
| Velocidade — instâncias pequenas | Rápido | Rápido | Médio | Muito rápido |
| Velocidade — T grande | Pior caso exponencial | Pior caso exponencial | Cresce com T | Insensível a T |

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
  3. Programação Dinâmica
  4. Estratégia Gulosa
Escolha: 3

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
| `padrao.txt` | 8 | 15 | Caso equilibrado para comparação base entre todos os algoritmos |
| `solucao_imediata.txt` | 10 | 12 | Solução nos 2 primeiros elementos — **ponto forte do Backtracking** |
| `sem_solucao.txt` | 12 | 79 | Alvo impossível (soma total = 78) — **pior caso para Backtracking e B&B; DP confirma ausência; Greedy aceita tudo mas não fecha** |
| `poda_maxima.txt` | 10 | 5 | Elementos grandes, alvo pequeno — **máxima poda em Backtracking e B&B; DP leve; Greedy rejeita tudo** |
| `solucao_no_final.txt` | 10 | 9 | Solução apenas no último elemento — **ponto fraco do Backtracking** |
| `fila_grande_bb.txt` | 15 | 30 | Muitos caminhos viáveis — **ponto fraco do Branch and Bound** |
| `greedy_falha.txt` | 5 | 11 | Solução existe ({6,5}=11) mas **Greedy falha** ao escolher 10 primeiro — **demonstra limitação da heurística** |

---

## Estrutura do Projeto

```
.
├── main.py                          # Ponto de entrada e menu interativo
├── io_handler.py                    # Leitura e parsing de entrada (manual e arquivo)
├── metrics.py                       # Exibição de resultados e métricas
├── algorithms/
│   ├── __init__.py                  # Marca o diretório como pacote Python
│   ├── backtracking.py              # Implementação do Backtracking
│   ├── branch_bound.py              # Implementação do Branch and Bound
│   ├── dynamic_programming.py       # Implementação da Programação Dinâmica
│   └── greedy.py                    # Implementação da Estratégia Gulosa
└── examples/
    ├── padrao.txt
    ├── solucao_imediata.txt
    ├── sem_solucao.txt
    ├── poda_maxima.txt
    ├── solucao_no_final.txt
    ├── fila_grande_bb.txt
    └── greedy_falha.txt             # Caso onde o Greedy falha mas solução existe
```

---

## Métricas Geradas

Após a execução, o programa exibe três blocos de análise. O conteúdo varia conforme o algoritmo escolhido:

**Análise Comportamental**

| Métrica | Backtracking | Branch and Bound | Prog. Dinâmica | Est. Gulosa |
|---|---|---|---|---|
| Estados / células exploradas | ✓ nós visitados | ✓ estados processados | ✓ células computadas | ✓ elementos analisados |
| Podas / rejeições | ✓ ramos eliminados | ✓ estados descartados | N/A | ✓ elementos rejeitados |
| Eficiência de poda (%) | ✓ | ✓ | N/A | — |
| Profundidade máxima | ✓ | — | — | — |
| Tamanho máximo da fila | — | ✓ | — | — |
| Tamanho da tabela DP | — | — | ✓ | — |
| Elementos aceitos | — | — | — | ✓ |

**Métricas de Qualidade**
- Qualidade da solução — ótima/exata (Backtracking, B&B, DP) ou aproximada/heurística (Greedy)
- Tempo de execução em milissegundos
- Pico de memória em KB

**Análise de Complexidade**
- Complexidade teórica
- Observações específicas de cada método (pseudopolinomial para DP; sem garantia de completude para Greedy)

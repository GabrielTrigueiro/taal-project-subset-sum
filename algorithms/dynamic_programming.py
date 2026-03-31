from __future__ import annotations  # Permite usar tipos como list[int] em versões antigas do Python

import time          # Para medir o tempo de execução
import tracemalloc   # Para medir o uso de memória


def dynamic_programming(nums: list[int], target: int) -> tuple[list[int] | None, dict]:
    """
    Soma de Subconjunto via Programação Dinâmica (DP).

    Constrói uma tabela booleana dp[i][s] onde dp[i][s] = True significa que
    é possível atingir a soma s usando apenas os primeiros i elementos de nums.

    Transição:
        dp[i][s] = dp[i-1][s]                           # não incluir nums[i-1]
                   OR dp[i-1][s - nums[i-1]]  (se s >= nums[i-1])  # incluir nums[i-1]

    Caso base:
        dp[i][0] = True para todo i  (subconjunto vazio tem soma 0)

    Reconstrução da solução: percorre a tabela de trás para frente para
    identificar quais elementos foram incluídos no subconjunto.

    Parâmetros:
        nums   : lista de inteiros positivos
        target : valor alvo da soma

    Retorna:
        (índices_solução, métricas)
        - índices_solução : índices base-1 do subconjunto encontrado, ou None se não houver solução
        - métricas        : dict com dados de desempenho e comportamento do algoritmo
    """

    n = len(nums)

    # --------------------------------------------------------------------------
    # Inicialização das métricas de desempenho
    # --------------------------------------------------------------------------
    metrics = {
        "nodes_visited"   : 0,              # Células da tabela DP computadas (preenchidas)
        "nodes_pruned"    : 0,              # Não aplicável — DP preenche toda a tabela (sempre 0)
        "dp_table_size"   : (n + 1) * (target + 1),  # Dimensão total da tabela DP
        "time_ms"         : 0.0,            # Tempo total de execução em milissegundos
        "memory_kb"       : 0.0,            # Pico de memória utilizada em kilobytes
        "found"           : False,          # Indica se uma solução foi encontrada
        "method"          : "Programação Dinâmica",
        "complexity"      : "O(n × T)",
    }

    # Inicia o rastreamento de memória e o cronômetro antes do preenchimento da tabela
    tracemalloc.start()
    start = time.perf_counter()

    # --------------------------------------------------------------------------
    # Alocação da tabela DP 2D: dp[i][s]
    # - i varia de 0 a n (0 = nenhum elemento considerado)
    # - s varia de 0 a target
    # --------------------------------------------------------------------------
    dp = [[False] * (target + 1) for _ in range(n + 1)]

    # Caso base: a soma 0 é sempre atingível com o subconjunto vazio
    for i in range(n + 1):
        dp[i][0] = True
        metrics["nodes_visited"] += 1   # Conta inicialização da primeira coluna

    # --------------------------------------------------------------------------
    # Preenchimento da tabela DP (ordem crescente de i e s)
    # --------------------------------------------------------------------------
    for i in range(1, n + 1):
        for s in range(1, target + 1):
            metrics["nodes_visited"] += 1   # Conta esta célula como computada

            # Opção 1: não incluir o i-ésimo elemento — herda o estado anterior
            dp[i][s] = dp[i - 1][s]

            # Opção 2: incluir o i-ésimo elemento (nums[i-1]) — só possível se s >= nums[i-1]
            if s >= nums[i - 1] and dp[i - 1][s - nums[i - 1]]:
                dp[i][s] = True

    # Para o cronômetro e coleta o pico de memória após o preenchimento da tabela
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Registra as métricas finais
    metrics["time_ms"]   = (end - start) * 1000   # Converte segundos para milissegundos
    metrics["memory_kb"] = peak / 1024             # Converte bytes para kilobytes
    metrics["found"]     = dp[n][target]

    # Se não há solução, retorna imediatamente
    if not dp[n][target]:
        return None, metrics

    # --------------------------------------------------------------------------
    # Reconstrução da solução: percorre a tabela de trás para frente
    # Se dp[i][s] = True mas dp[i-1][s] = False, o elemento i foi necessário
    # --------------------------------------------------------------------------
    solution = []
    s = target
    for i in range(n, 0, -1):
        if dp[i][s] and not dp[i - 1][s]:
            # O elemento nums[i-1] foi incluído no subconjunto solução
            solution.append(i)    # Índice base-1
            s -= nums[i - 1]      # Reduz a soma restante a ser reconstruída

    solution.reverse()   # Reverte para ordem crescente de índices
    return solution, metrics

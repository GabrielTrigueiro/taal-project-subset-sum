from __future__ import annotations  # Permite usar tipos como list[int] em versões antigas do Python

import time          # Para medir o tempo de execução
import tracemalloc   # Para medir o uso de memória
from collections import deque   # Fila eficiente para BFS (O(1) no append e popleft)


def branch_and_bound(nums: list[int], target: int) -> tuple[list[int] | None, dict]:
    """
    Soma de Subconjunto via Branch and Bound.

    Usa BFS (busca em largura) com uma fila explícita de estados.
    Cada estado representa uma decisão parcial sobre quais elementos incluir.

    Estado na fila: (índice, soma_atual, índices_selecionados_base1)

    Função de limite superior:
        limite_superior = soma_atual + soma(nums[índice:])

    Condições de poda (descarta o estado sem expandir):
        1. soma_atual > alvo        → já ultrapassou o alvo
        2. limite_superior < alvo   → impossível atingir o alvo com os elementos restantes

    Parâmetros:
        nums   : lista de inteiros positivos
        target : valor alvo da soma

    Retorna:
        (índices_solução, métricas)
        - índices_solução : índices base-1 do subconjunto encontrado, ou None se não houver solução
        - métricas        : dict com dados de desempenho e comportamento do algoritmo
    """

    # --------------------------------------------------------------------------
    # Inicialização das métricas de desempenho
    # --------------------------------------------------------------------------
    metrics = {
        "nodes_visited"   : 0,       # Total de nós (estados) processados da fila
        "nodes_pruned"    : 0,       # Total de ramos descartados pela poda
        "max_queue_size"  : 0,       # Tamanho máximo que a fila atingiu durante a busca
        "time_ms"         : 0.0,     # Tempo total de execução em milissegundos
        "memory_kb"       : 0.0,     # Pico de memória utilizada em kilobytes
        "found"           : False,   # Indica se uma solução foi encontrada
        "method"          : "Branch and Bound",
        "complexity"      : "O(2^n) pior caso",
    }

    n = len(nums)   # Tamanho do array de entrada

    # --------------------------------------------------------------------------
    # Pré-cálculo das somas de sufixo (suffix_sum)
    # suffix_sum[i] = soma de nums[i], nums[i+1], ..., nums[n-1]
    # Permite calcular o limite superior em O(1) durante a busca
    # --------------------------------------------------------------------------
    suffix_sum = [0] * (n + 1)          # Uma posição extra para o índice n (soma vazia)
    for i in range(n - 1, -1, -1):      # Percorre o array de trás para frente
        suffix_sum[i] = suffix_sum[i + 1] + nums[i]   # Acumula a soma a partir de i

    # Inicia o rastreamento de memória e o cronômetro antes da busca
    tracemalloc.start()
    start = time.perf_counter()

    # --------------------------------------------------------------------------
    # Fila BFS — cada entrada representa um estado parcial da busca
    # Formato: (índice_atual, soma_acumulada, lista_de_índices_selecionados)
    # --------------------------------------------------------------------------
    queue: deque = deque()
    queue.append((0, 0, []))   # Estado inicial: começa no índice 0, soma 0, sem elementos

    solution = None   # Armazenará a solução ao ser encontrada

    # --------------------------------------------------------------------------
    # Loop principal de BFS
    # --------------------------------------------------------------------------
    while queue:

        # Atualiza o tamanho máximo registrado da fila
        if len(queue) > metrics["max_queue_size"]:
            metrics["max_queue_size"] = len(queue)

        # Retira o próximo estado da fila (ordem FIFO)
        index, current_sum, selected = queue.popleft()
        metrics["nodes_visited"] += 1   # Conta este estado como processado

        # --- Verificação de solução: soma exatamente igual ao alvo ---
        if current_sum == target:
            solution = selected   # Guarda os índices selecionados como solução
            break                 # Interrompe a busca imediatamente

        # --- Caso base: chegou ao fim do array ---
        if index == n:
            continue   # Não há mais elementos para processar neste estado

        # Calcula o limite superior: melhor soma possível a partir deste estado
        upper_bound = current_sum + suffix_sum[index]

        # --- Poda: mesmo somando tudo que resta, não chega ao alvo ---
        if upper_bound < target:
            metrics["nodes_pruned"] += 1
            continue   # Descarta este estado sem gerar filhos

        # --- Ramo 1: INCLUIR nums[index] ---
        new_sum = current_sum + nums[index]   # Calcula a nova soma ao incluir o elemento
        if new_sum <= target:                  # Só enfileira se não ultrapassar o alvo
            queue.append((index + 1, new_sum, selected + [index + 1]))   # índice base-1
        else:
            metrics["nodes_pruned"] += 1   # Ultrapassaria o alvo → poda este ramo

        # --- Ramo 2: EXCLUIR nums[index] ---
        # Verifica se, sem o elemento atual, os elementos restantes ainda permitem atingir o alvo
        if suffix_sum[index + 1] >= target - current_sum:
            queue.append((index + 1, current_sum, selected))   # Mantém a soma atual
        else:
            metrics["nodes_pruned"] += 1   # Impossível atingir o alvo sem este elemento → poda

    # Para o cronômetro e coleta o pico de memória após o término da busca
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Registra as métricas finais
    metrics["time_ms"]   = (end - start) * 1000   # Converte segundos para milissegundos
    metrics["memory_kb"] = peak / 1024             # Converte bytes para kilobytes
    metrics["found"]     = solution is not None

    # Retorna a solução encontrada (ou None) junto com as métricas
    return solution, metrics

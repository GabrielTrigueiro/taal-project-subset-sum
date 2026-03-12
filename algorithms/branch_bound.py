from __future__ import annotations

import time
import tracemalloc
from collections import deque


def branch_and_bound(nums: list[int], target: int) -> tuple[list[int] | None, dict]:
    """
    Soma de Subconjunto via Branch and Bound.

    Usa BFS com uma fila explícita de estados.
    Estado: (índice, soma_atual, índices_selecionados_base1)

    Função de limite (limite superior):
        limite_superior = soma_atual + soma(nums[índice:])
    Condições de poda:
        1. soma_atual > alvo  → excedeu, podar
        2. limite_superior < alvo  → não consegue atingir o alvo, podar

    Retorna:
        (índices_solução, métricas)
        índices_solução: índices base-1 do subconjunto, ou None se não houver solução.
        métricas: dict com dados comportamentais e de qualidade.
    """
    metrics = {
        "nodes_visited": 0,
        "nodes_pruned": 0,
        "max_queue_size": 0,
        "time_ms": 0.0,
        "memory_kb": 0.0,
        "found": False,
        "method": "Branch and Bound",
        "complexity": "O(2^n) pior caso",
        "complexity_note": (
            "Usa BFS com fila explícita de estados. O limite superior "
            "(soma_atual + soma_restante) permite podar ramos que não podem "
            "atingir o alvo. Na prática, a poda elimina grandes subárvores, "
            "tornando-o significativamente mais eficiente que força bruta."
        ),
    }

    # Pré-calcula somas de sufixo para cálculo eficiente do limite superior
    n = len(nums)
    suffix_sum = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_sum[i] = suffix_sum[i + 1] + nums[i]

    tracemalloc.start()
    start = time.perf_counter()

    # Entradas da fila: (índice, soma_atual, índices_selecionados)
    queue: deque = deque()
    queue.append((0, 0, []))

    solution = None

    while queue:
        if len(queue) > metrics["max_queue_size"]:
            metrics["max_queue_size"] = len(queue)

        index, current_sum, selected = queue.popleft()
        metrics["nodes_visited"] += 1

        # Verifica solução
        if current_sum == target:
            solution = selected
            break

        # Elementos esgotados
        if index == n:
            continue

        upper_bound = current_sum + suffix_sum[index]

        # Poda: mesmo incluindo todos os elementos restantes não atinge o alvo
        if upper_bound < target:
            metrics["nodes_pruned"] += 1
            continue

        # Ramo 1: incluir nums[index]
        new_sum = current_sum + nums[index]
        if new_sum <= target:
            queue.append((index + 1, new_sum, selected + [index + 1]))
        else:
            metrics["nodes_pruned"] += 1

        # Ramo 2: excluir nums[index]
        # Só enfileira se excluindo ainda for possível atingir o alvo
        if suffix_sum[index + 1] >= target - current_sum:
            queue.append((index + 1, current_sum, selected))
        else:
            metrics["nodes_pruned"] += 1

    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    metrics["time_ms"] = (end - start) * 1000
    metrics["memory_kb"] = peak / 1024
    metrics["found"] = solution is not None

    return solution, metrics

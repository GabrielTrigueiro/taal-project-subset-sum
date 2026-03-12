from __future__ import annotations

import time
import tracemalloc


def backtracking(nums: list[int], target: int) -> tuple[list[int] | None, dict]:
    """
    Soma de Subconjunto via Backtracking.

    Explora uma árvore binária de decisão (incluir/excluir cada elemento).
    Poda: ignora um ramo se o elemento atual excede o alvo restante.

    Retorna:
        (índices_solução, métricas)
        índices_solução: índices base-1 do subconjunto, ou None se não houver solução.
        métricas: dict com dados comportamentais e de qualidade.
    """
    metrics = {
        "nodes_visited": 0,
        "nodes_pruned": 0,
        "max_depth": 0,
        "time_ms": 0.0,
        "memory_kb": 0.0,
        "found": False,
        "method": "Backtracking",
        "complexity": "O(2^n)",
        "complexity_note": (
            "Explora uma árvore binária de decisão (incluir/excluir cada elemento). "
            "No pior caso, visita todos os 2^n subconjuntos. A poda elimina ramos "
            "onde o elemento atual excede a soma restante, reduzindo o espaço na prática."
        ),
    }

    solution: list[int] = []
    found_flag = [False]

    tracemalloc.start()
    start = time.perf_counter()

    def _backtrack(index: int, remaining: int, current: list[int], depth: int):
        if found_flag[0]:
            return

        metrics["nodes_visited"] += 1
        if depth > metrics["max_depth"]:
            metrics["max_depth"] = depth

        # Caso base: subconjunto válido encontrado
        if remaining == 0:
            solution.extend(current)
            found_flag[0] = True
            return

        # Caso base: todos os elementos foram percorridos
        if index == len(nums):
            return

        # Poda: os elementos restantes não conseguem atingir o alvo
        remaining_sum = sum(nums[index:])
        if remaining_sum < remaining:
            metrics["nodes_pruned"] += 1
            return

        # Ramo 1: incluir nums[index] (apenas se não exceder o restante)
        if nums[index] <= remaining:
            current.append(index + 1)  # índice base-1
            _backtrack(index + 1, remaining - nums[index], current, depth + 1)
            if not found_flag[0]:
                current.pop()
        else:
            metrics["nodes_pruned"] += 1

        # Ramo 2: excluir nums[index]
        if not found_flag[0]:
            _backtrack(index + 1, remaining, current, depth + 1)

    _backtrack(0, target, [], 0)

    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    metrics["time_ms"] = (end - start) * 1000
    metrics["memory_kb"] = peak / 1024
    metrics["found"] = found_flag[0]

    return (solution if found_flag[0] else None), metrics

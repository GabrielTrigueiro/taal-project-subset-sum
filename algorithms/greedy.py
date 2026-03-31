from __future__ import annotations  # Permite usar tipos como list[int] em versões antigas do Python

import time          # Para medir o tempo de execução
import tracemalloc   # Para medir o uso de memória


def greedy(nums: list[int], target: int) -> tuple[list[int] | None, dict]:
    """
    Soma de Subconjunto via Estratégia Gulosa.

    Ordena os elementos em ordem decrescente e, a cada passo, inclui o maior
    elemento possível que não ultrapasse o valor restante para atingir o alvo.

    Critério guloso: "escolha sempre o maior elemento que ainda cabe".

    AVISO: A Estratégia Gulosa NÃO garante encontrar uma solução mesmo
    quando ela existe. Por ser uma heurística, pode falhar em instâncias
    onde a solução exige priorizar elementos menores antes de maiores.

    Exemplo de falha:
        Conjunto = {10, 7, 6, 5, 3},  Alvo = 11
        Guloso escolhe 10 (restante = 1) → nenhum elemento cabe → falha.
        Solução real: {6, 5} → 6 + 5 = 11 ✓

    Parâmetros:
        nums   : lista de inteiros positivos
        target : valor alvo da soma

    Retorna:
        (índices_solução, métricas)
        - índices_solução : índices base-1 do subconjunto encontrado, ou None
                            (ausência de solução pode ser falso negativo da heurística)
        - métricas        : dict com dados de desempenho e comportamento do algoritmo
    """

    n = len(nums)

    # --------------------------------------------------------------------------
    # Inicialização das métricas de desempenho
    # --------------------------------------------------------------------------
    metrics = {
        "nodes_visited"     : 0,        # Total de elementos analisados (candidatos avaliados)
        "nodes_pruned"      : 0,        # Elementos rejeitados por exceder o alvo restante
        "elements_accepted" : 0,        # Elementos efetivamente incluídos no subconjunto
        "time_ms"           : 0.0,      # Tempo total de execução em milissegundos
        "memory_kb"         : 0.0,      # Pico de memória utilizada em kilobytes
        "found"             : False,    # Indica se o alvo foi atingido exatamente
        "method"            : "Estratégia Gulosa",
        "complexity"        : "O(n log n)",
    }

    # Inicia o rastreamento de memória e o cronômetro antes da execução
    tracemalloc.start()
    start = time.perf_counter()

    # --------------------------------------------------------------------------
    # Ordenação dos índices pelo valor do elemento, em ordem decrescente
    # (critério guloso: priorizar os maiores elementos primeiro)
    # --------------------------------------------------------------------------
    sorted_indices = sorted(range(n), key=lambda i: nums[i], reverse=True)

    remaining = target          # Quanto ainda falta para atingir o alvo
    selected: list[int] = []    # Índices base-1 dos elementos selecionados

    # --------------------------------------------------------------------------
    # Varredura gulosa: avalia cada elemento na ordem decrescente de valor
    # --------------------------------------------------------------------------
    for idx in sorted_indices:
        metrics["nodes_visited"] += 1   # Conta este elemento como avaliado

        if nums[idx] <= remaining:
            # Decisão gulosa: inclui o elemento pois ele não ultrapassa o restante
            selected.append(idx + 1)    # Armazena o índice base-1
            remaining -= nums[idx]      # Atualiza o valor restante
            metrics["elements_accepted"] += 1

            if remaining == 0:
                break   # Alvo atingido exatamente — encerra a busca
        else:
            # Elemento excede o valor restante — descartado sem explorar subproblemas
            metrics["nodes_pruned"] += 1

    # Para o cronômetro e coleta o pico de memória após a execução
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Registra as métricas finais
    metrics["time_ms"]   = (end - start) * 1000   # Converte segundos para milissegundos
    metrics["memory_kb"] = peak / 1024             # Converte bytes para kilobytes
    metrics["found"]     = remaining == 0          # True somente se o alvo foi atingido exatamente

    if remaining == 0:
        selected.sort()   # Ordena por índice para exibição consistente com os demais algoritmos
        return selected, metrics

    # Nenhuma solução encontrada pela heurística (pode ser falso negativo)
    return None, metrics

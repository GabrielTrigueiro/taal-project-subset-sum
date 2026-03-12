from __future__ import annotations  # Permite usar tipos como list[int] em versões antigas do Python

import time          # Para medir o tempo de execução
import tracemalloc   # Para medir o uso de memória


def backtracking(nums: list[int], target: int) -> tuple[list[int] | None, dict]:
    """
    Soma de Subconjunto via Backtracking.

    Explora uma árvore binária de decisão onde, para cada elemento,
    há dois caminhos possíveis: incluir ou excluir o elemento.

    Poda: ignora um ramo se o elemento atual excede o alvo restante,
    ou se a soma dos elementos restantes não é suficiente para atingir o alvo.

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
        "nodes_visited"   : 0,       # Total de nós visitados na árvore de decisão
        "nodes_pruned"    : 0,       # Total de ramos eliminados pela poda
        "max_depth"       : 0,       # Profundidade máxima atingida na árvore
        "time_ms"         : 0.0,     # Tempo total de execução em milissegundos
        "memory_kb"       : 0.0,     # Pico de memória utilizada em kilobytes
        "found"           : False,   # Indica se uma solução foi encontrada
        "method"          : "Backtracking",
        "complexity"      : "O(2^n)",
    }

    solution: list[int] = []   # Armazenará os índices (base-1) do subconjunto solução
    found_flag = [False]       # Lista mutável para permitir modificação dentro da função aninhada

    # Inicia o rastreamento de memória e o cronômetro antes da busca
    tracemalloc.start()
    start = time.perf_counter()

    # --------------------------------------------------------------------------
    # Função recursiva de backtracking
    # --------------------------------------------------------------------------
    def _backtrack(index: int, remaining: int, current: list[int], depth: int):
        """
        Parâmetros:
            index     : posição atual no array nums
            remaining : quanto ainda falta para atingir o alvo
            current   : índices (base-1) dos elementos selecionados até agora
            depth     : profundidade atual na árvore de decisão
        """

        # Se já encontramos uma solução, abandona todos os ramos restantes
        if found_flag[0]:
            return

        metrics["nodes_visited"] += 1                        # Conta este nó como visitado
        if depth > metrics["max_depth"]:                     # Atualiza profundidade máxima, se necessário
            metrics["max_depth"] = depth

        # --- Caso base 1: soma atingida → solução encontrada ---
        if remaining == 0:
            solution.extend(current)   # Copia os índices da solução para a variável externa
            found_flag[0] = True       # Sinaliza que a busca pode parar
            return

        # --- Caso base 2: chegou ao fim do array sem completar a soma ---
        if index == len(nums):
            return

        # --- Poda por insuficiência: soma dos elementos restantes não basta ---
        remaining_sum = sum(nums[index:])   # Soma de todos os elementos a partir do índice atual
        if remaining_sum < remaining:        # Impossível atingir o alvo mesmo usando tudo
            metrics["nodes_pruned"] += 1
            return

        # --- Ramo 1: INCLUIR nums[index] ---
        if nums[index] <= remaining:                              # Só inclui se não ultrapassar o alvo
            current.append(index + 1)                            # Adiciona índice base-1 à solução parcial
            _backtrack(index + 1, remaining - nums[index], current, depth + 1)
            if not found_flag[0]:                                # Se não achou solução neste ramo...
                current.pop()                                    # ...desfaz a escolha (backtrack)
        else:
            metrics["nodes_pruned"] += 1   # Elemento excede o restante → poda este ramo

        # --- Ramo 2: EXCLUIR nums[index] ---
        if not found_flag[0]:   # Só explora se ainda não encontrou solução
            _backtrack(index + 1, remaining, current, depth + 1)

    # --------------------------------------------------------------------------
    # Dispara a busca a partir do primeiro elemento, com a soma alvo completa
    # --------------------------------------------------------------------------
    _backtrack(0, target, [], 0)

    # Para o cronômetro e coleta o pico de memória após o término da busca
    end = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Registra as métricas finais
    metrics["time_ms"]   = (end - start) * 1000   # Converte segundos para milissegundos
    metrics["memory_kb"] = peak / 1024             # Converte bytes para kilobytes
    metrics["found"]     = found_flag[0]

    # Retorna a solução encontrada (ou None) junto com as métricas
    return (solution if found_flag[0] else None), metrics

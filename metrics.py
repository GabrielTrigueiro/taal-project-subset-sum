from __future__ import annotations


def print_result(solution: list[int] | None, nums: list[int], target: int):
    """Exibe o resultado do algoritmo no formato exigido."""
    sep = "-" * 40
    print(f"\n{sep}")
    print("RESULTADO")
    print(sep)
    if solution is not None:
        subset_values = [nums[i - 1] for i in solution]
        print("YES")
        print(len(solution))
        print(" ".join(str(i) for i in solution))
        print(f"\n  Subconjunto: {{ {', '.join(str(v) for v in subset_values)} }}")
        print(f"  Soma: {sum(subset_values)} = {target}")
    else:
        print("NO")


def print_metrics(metrics: dict):
    """Exibe métricas comportamentais, sintáticas e de qualidade."""
    sep = "=" * 50
    print(f"\n{sep}")
    print(f"  ANÁLISE — {metrics['method']}")
    print(sep)

    method = metrics["method"]

    # --------------------------------------------------------------------------
    # Análise Comportamental — adaptada para cada método
    # --------------------------------------------------------------------------
    print("\n[Análise Comportamental]")

    if method == "Programação Dinâmica":
        # DP não realiza poda — preenche toda a tabela de forma sistemática
        print(f"  Células DP computadas  : {metrics['nodes_visited']}")
        print(f"  Tamanho da tabela DP   : {metrics['dp_table_size']} células  (n+1) × (T+1)")
        print(f"  Eficiência de poda     : N/A — DP preenche todas as células da tabela")

    elif method == "Estratégia Gulosa":
        # Greedy avalia cada elemento uma única vez, sem exploração de subproblemas
        print(f"  Elementos analisados   : {metrics['nodes_visited']}")
        print(f"  Elementos aceitos      : {metrics['elements_accepted']}")
        print(f"  Elementos rejeitados   : {metrics['nodes_pruned']}  (excederam o alvo restante)")

    else:
        # Backtracking e Branch and Bound — métricas de exploração e poda
        print(f"  Estados explorados  : {metrics['nodes_visited']}")
        print(f"  Estados podados     : {metrics['nodes_pruned']}")

        total = metrics["nodes_visited"] + metrics["nodes_pruned"]
        if total > 0:
            efficiency = metrics["nodes_pruned"] / total * 100
            print(f"  Eficiência de poda  : {efficiency:.1f}%  ({metrics['nodes_pruned']}/{total} ramos eliminados)")
        else:
            print("  Eficiência de poda  : N/A")

        if "max_depth" in metrics:
            print(f"  Profundidade máxima : {metrics['max_depth']}")
        if "max_queue_size" in metrics:
            print(f"  Tamanho máx. fila   : {metrics['max_queue_size']}")

    # --------------------------------------------------------------------------
    # Métricas de Qualidade
    # --------------------------------------------------------------------------
    print("\n[Métricas de Qualidade]")

    if method == "Estratégia Gulosa":
        if metrics["found"]:
            print("  Qualidade da solução: Aproximada (heurística — pode não ser a única solução possível)")
        else:
            print("  Qualidade da solução: Sem solução encontrada  ⚠ heurística pode ter falhado")
    else:
        print(f"  Qualidade da solução: {'Ótima (exata)' if metrics['found'] else 'Sem solução'}")

    print(f"  Tempo de execução   : {metrics['time_ms']:.4f} ms")
    print(f"  Pico de memória     : {metrics['memory_kb']:.2f} KB")

    # --------------------------------------------------------------------------
    # Análise Sintática / Complexidade
    # --------------------------------------------------------------------------
    print("\n[Análise Sintática / Complexidade]")
    print(f"  Complexidade        : {metrics['complexity']}")

    if method == "Estratégia Gulosa":
        print(f"  Observação          : Heurística sem garantia de encontrar a solução exata")
    elif method == "Programação Dinâmica":
        print(f"  Observação          : Pseudopolinomial — eficiente para T pequeno, cresce com T")

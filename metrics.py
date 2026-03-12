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

    # --- Análise Comportamental ---
    print("\n[Análise Comportamental]")
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

    # --- Métricas de Qualidade ---
    print("\n[Métricas de Qualidade]")
    print(f"  Qualidade da solução: {'Ótima (exata)' if metrics['found'] else 'Sem solução'}")
    print(f"  Tempo de execução   : {metrics['time_ms']:.4f} ms")
    print(f"  Pico de memória     : {metrics['memory_kb']:.2f} KB")

    # --- Análise Sintática / Complexidade ---
    print("\n[Análise Sintática / Complexidade]")
    print(f"  Complexidade        : {metrics['complexity']}")
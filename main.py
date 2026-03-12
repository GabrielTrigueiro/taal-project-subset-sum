from algorithms.backtracking import backtracking
from algorithms.branch_bound import branch_and_bound
from io_handler import get_input
from metrics import print_result, print_metrics


ALGORITHMS = {
    "1": "Subset Sum",
}

METHODS = {
    "1": "Backtracking",
    "2": "Branch and Bound",
}


def menu_choice(prompt: str, options: dict[str, str]) -> str:
    """Exibe um menu numerado e retorna a escolha válida do usuário."""
    while True:
        print(prompt)
        for key, label in options.items():
            print(f"  {key}. {label}")
        choice = input("Escolha: ").strip()
        if choice in options:
            return choice
        print(f"  Opção inválida. Escolha entre: {', '.join(options.keys())}\n")


def run():
    print("\n" + "=" * 50)
    print("  PROJETO EXPERIMENTAL — TÉCNICAS DE ALGORITMOS")
    print("=" * 50)

    # Passo 1: escolher algoritmo
    algo_choice = menu_choice("\nAlgoritmo:", ALGORITHMS)
    print(f"\n  >> {ALGORITHMS[algo_choice]} selecionado.\n")

    # Passo 2: escolher método
    method_choice = menu_choice("Método de resolução:", METHODS)
    print(f"\n  >> {METHODS[method_choice]} selecionado.\n")

    # Passo 3: escolher tipo de entrada
    input_choice = menu_choice(
        "Tipo de entrada:",
        {"1": "Arquivo", "2": "Manual"},
    )
    print()

    # Passo 4: ler entrada
    try:
        target, nums = get_input(input_choice)
    except (KeyboardInterrupt, EOFError):
        print("\nEntrada cancelada.")
        return

    print(f"\n  Conjunto : {nums}")
    print(f"  Alvo (T) : {target}")

    # Passo 5: executar algoritmo selecionado
    if method_choice == "1":
        solution, metrics = backtracking(nums, target)
    else:
        solution, metrics = branch_and_bound(nums, target)

    # Passo 6: exibir resultados e métricas
    print_result(solution, nums, target)
    print_metrics(metrics)


def main():
    while True:
        run()
        print()
        again = input("Executar novamente? (s/n): ").strip().lower()
        if again != "s":
            print("\nEncerrando. Até mais!\n")
            break


if __name__ == "__main__":
    main()

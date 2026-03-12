import os


def parse_input(lines: list[str]) -> tuple[int, list[int]]:
    """Analisa entrada: 'n T' depois 'a1 a2 ... an'. Retorna (alvo, nums)."""
    data = [line.strip() for line in lines if line.strip()]
    if len(data) < 2:
        raise ValueError("Primeira linha deve conter 'n T'.")

    first = data[0].split()
    if len(first) < 2:
        raise ValueError("Primeira linha deve conter 'n T'.")
    n, target = int(first[0]), int(first[1])

    second = data[1].split()
    if len(second) != n:
        raise ValueError(f"Esperado {n} elementos, encontrado {len(second)}.")
    nums = [int(x) for x in second]

    if any(x <= 0 for x in nums):
        raise ValueError("Todos os elementos devem ser inteiros positivos.")
    if target <= 0:
        raise ValueError("O alvo T deve ser um inteiro positivo.")

    return target, nums


def get_input_from_file() -> tuple[int, list[int]]:
    """Solicita ao usuário um caminho de arquivo e o analisa."""
    while True:
        path = input("Caminho do arquivo: ").strip()
        if not os.path.isfile(path):
            print(f"  Arquivo '{path}' não encontrado. Tente novamente.")
            continue
        try:
            with open(path, "r") as f:
                lines = f.readlines()
            if len(lines) < 2:
                print("  O arquivo deve ter pelo menos 2 linhas.")
                continue
            return parse_input(lines)
        except ValueError as e:
            print(f"  Erro no formato do arquivo: {e}")
        except Exception as e:
            print(f"  Erro ao ler arquivo: {e}")


def get_input_manual() -> tuple[int, list[int]]:
    """Solicita ao usuário que informe a entrada manualmente."""
    print("  Formato: primeira linha 'n T', segunda linha 'a1 a2 ... an'")
    while True:
        try:
            line1 = input("  n T: ").strip()
            first = line1.split()
            if len(first) < 2:
                print("  Informe dois valores na primeira linha.")
                continue
            n = int(first[0])
            line2 = input(f"  {n} elemento(s): ").strip()
            return parse_input([line1, line2])
        except ValueError as e:
            print(f"  Entrada inválida: {e}. Tente novamente.")


def get_input(choice: str) -> tuple[int, list[int]]:
    """Direciona a coleta de entrada com base na escolha do usuário."""
    if choice == "1":
        return get_input_from_file()
    else:
        return get_input_manual()

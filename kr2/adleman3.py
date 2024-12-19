import random
from sympy import Matrix, mod_inverse, gcd, pprint

# Параметры задачи
p = 37  # Простое число, модуль группы Z*_p
g = 2    # Генератор группы
a = 13   # Элемент группы, для которого ищем логарифм

print(f"Условие задачи: Найти логарифм log_g({a}) по модулю p = {p}, где g = {g}\n")

# Факторная база: только простые делители p-1
def factor_base(p):
    """Возвращает список простых чисел, делящих p-1."""
    return [2, 3, 5]

S = factor_base(p)
print(f"Факторная база S = {S}\n")

mod = p - 1  # Порядок мультипликативной группы Z*_p

def decompose(x, base, p):
    """
    Пытается разложить число x по факторной базе base.
    Возвращает список показателей степеней или None, если разложение невозможно.
    """
    exponents = []
    temp = x
    for prime in base:
        exp = 0
        while temp % prime == 0:
            temp //= prime
            exp += 1
        exponents.append(exp)
    # Если после деления осталась единица, значит разложение удалось
    return exponents if temp == 1 else None

def solve_modular_linear_system(A, b, mod):
    """
    Решает систему линейных уравнений A * x = b (mod mod).
    Возвращает решение в виде списка или None, если решения нет.
    """
    A = A.copy()
    b = b.copy()
    n, m = A.shape

    for i in range(n):
        A.row_op(i, lambda x, _: x % mod)
        b[i] = b[i] % mod

    row = 0
    for col in range(m):
        # Найдём главный элемент
        pivot = None
        for r in range(row, n):
            if gcd(A[r, col], mod) == 1:
                pivot = r
                break

        if pivot is None:
            continue  # Перейдём к следующему столбцу

        # Поменяем текущую строку с строкой pivot
        if pivot != row:
            A.row_swap(pivot, row)
            b[row], b[pivot] = b[pivot], b[row]

        # Найдём мультипликативный обратный для главного элемента
        inv = mod_inverse(A[row, col], mod)
        if inv is None:
            continue  # Не удается найти обратный, пропускаем

        # Нормализуем главную строку
        A.row_op(row, lambda x, j: (x * inv) % mod)
        b[row] = (b[row] * inv) % mod

        # Обнуляем остальные элементы в текущем столбце
        for r in range(n):
            if r != row and A[r, col] != 0:
                factor = A[r, col]
                A.row_op(r, lambda x, j: (x - factor * A[row, j]) % mod)
                b[r] = (b[r] - factor * b[row]) % mod

        row += 1

    # Проверка на наличие решения
    for r in range(n):
        if all(A[r, c] == 0 for c in range(m)) and b[r] != 0:
            return None  # Нет решения

    # Извлекаем решение
    solution = [0] * m
    for r in range(row):
        leading = None
        for c in range(m):
            if A[r, c] != 0:
                leading = c
                break
        if leading is not None:
            solution[leading] = b[r]

    return solution

# Шаг 2: Поиск разложений g^k по факторной базе
print("Шаг 2: Поиск разложений g^k по факторной базе\n")
relations = []
ks = []
required_relations = len(S)
max_attempts = 1000  # Максимальное количество попыток для поиска разложений
attempts = 0

while len(relations) < required_relations and attempts < max_attempts:
    # k = random.randint(1, mod - 1)
    k = random.choice([1,6,10])
    b = pow(g, k, p)  # b = g^k mod p
    exponents = decompose(b, S, p)
    if exponents is not None:
        # Проверяем, не было ли уже такого разложения
        if exponents not in relations:
            relations.append(exponents)
            ks.append(k)
            # Формируем строку разложения
            factorization_str = " * ".join([f"{S[j]}^{exponents[j]}" for j in range(len(S)) if exponents[j] != 0])
            if factorization_str == "":
                factorization_str = "1"
            print(f"Попытка {attempts + 1}: k = {k}, g^{k} mod {p} = {b}, разложение: {factorization_str}")
    attempts += 1

if len(relations) < required_relations:
    print("\nНедостаточно разложений. Попробуйте увеличить количество попыток или расширить факторную базу.")
    exit(1)

print("\nВсе необходимые разложения найдены:")
for i, rel in enumerate(relations):
    # Формируем строку разложения
    factorization_str = " * ".join([f"{S[j]}^{rel[j]}" for j in range(len(S)) if rel[j] != 0])
    if factorization_str == "":
        factorization_str = "1"
    print(f"{i + 1}: g^{ks[i]} = {factorization_str} (mod {p})")

# Шаг 3: Решение системы сравнений
print("\nШаг 3: Решение системы сравнений\n")

A = Matrix(relations)
b_matrix = Matrix(ks)

# Печать матриц A и b
print(f"Система линейных уравнений (mod {mod}):")
print("Матрица A:")
pprint(A)
print("Вектор b:")
pprint(b_matrix)

# Решаем систему A * x = b mod (p-1)
solution = solve_modular_linear_system(A, b_matrix, mod)

if solution is None:
    print("Система уравнений не имеет решений. Необходимо собрать дополнительные разложения.")
    exit(1)

# Приводим решение по модулю
logs = [int(val % mod) for val in solution]

print("Логарифмы элементов факторной базы (по модулю p-1):")
for i, log_val in enumerate(logs):
    print(f"log_g({S[i]}) = {log_val} (mod {mod})")

# Шаг 4: Поиск log_g(a)
print("\nШаг 4: Поиск log_g(a)\n")

while True:
    k = random.randint(0, mod - 1)
    b_val = (a * pow(g, k, p)) % p
    exponents = decompose(b_val, S, p)
    if exponents is not None:
        # Вычисляем log_g(a)
        sum_exp = sum(e * l for e, l in zip(exponents, logs))
        x = (sum_exp - k) % mod
        # Формируем строку разложения
        factorization_str = " * ".join([f"{S[j]}^{exponents[j]}" for j in range(len(S)) if exponents[j] != 0])
        if factorization_str == "":
            factorization_str = "1"
        print(f"Найдено разложение для a * g^{k}: {a} * g^{k} = {factorization_str} (mod {p})")
        print(f"log_g({a}) = {x} (mod {mod})")
        # if x == 26:
        break

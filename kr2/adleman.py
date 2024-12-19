import random
import numpy as np
from sympy import Matrix, mod_inverse

# Параметры задачи
p = 37  # Модуль группы Z*_p
g = 2  # Генератор группы
a = 13  # Элемент, для которого ищем логарифм

# Шаг 1: Факторная база (простые числа меньшие p)
def factor_base(p):
    base = [2, 3, 5]
    return base

S = factor_base(p)
print(f"Факторная база: {S}\n")

# Функция для проверки разложения по факторной базе
def decompose(x, base, p):
    """Проверяет, можно ли разложить x по факторной базе."""
    exponents = []
    for prime in base:
        exp = 0
        while x % prime == 0 and x > 1:
            x //= prime
            exp += 1
        exponents.append(exp)
    return exponents if x == 1 else None

# Шаг 2: Поиск разложений g^k по факторной базе
relations = []
ks = []

print("Шаг 2: Поиск разложений g^k по факторной базе")
while len(relations) < len(S):
    # k = random.randint(1, p - 2)
    k = random.choice([1,6,10])
    b = pow(g, k, p)  # b = g^k mod p
    exponents = decompose(b, S, p)
    if exponents:
        relations.append(exponents)
        ks.append(k)
        print(f"k = {k}, g^{k} mod {p} = {b}, разложение: {exponents}")

print("\nВсе разложения найдены:")
for i, rel in enumerate(relations):
    print(f"{i+1}: g^{ks[i]} = {S[0]}^{rel[0]} * {S[1]}^{rel[1]} * {S[2]}^{rel[2]} (mod {p})")

# Шаг 3: Решаем систему сравнений
print("\nШаг 3: Решение системы сравнений")
A = Matrix(relations)
b = Matrix(ks)
mod = p - 1
A_mod = A.applyfunc(lambda x: x % mod)
b_mod = b.applyfunc(lambda x: x % mod)

print("Матрица коэффициентов A:")
print(A_mod)
print("\nПравая часть b:")
print(b_mod)

solution = A_mod.solve_least_squares(b_mod)
logs = [int(sol % mod) for sol in solution]

print("\nЛогарифмы элементов факторной базы:")
for i, log_val in enumerate(logs):
    print(f"log_g({S[i]}) = {log_val} (mod {mod})")

# Шаг 4: Найти log_g(a)
print("\nШаг 4: Поиск log_g(a)")
while True:
    # k = random.randint(0, p - 2)
    k = 2
    b = (a * pow(g, k, p)) % p
    print(f"Пробуем k = {k}, вычисляем b = a * g^k mod {p} = {b}")
    exponents = decompose(b, S, p)
    if exponents:
        print(f"b = {b} разложено как: {S[0]}^{exponents[0]} * {S[1]}^{exponents[1]} * {S[2]}^{exponents[2]} (mod {p})")
        x = sum(exp * log for exp, log in zip(exponents, logs)) - k
        x %= mod
        print(f"log_g({a}) = {x} (mod {mod})")
        break

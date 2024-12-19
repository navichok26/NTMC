from sympy import mod_inverse, factorint

def pohlig_hellman_log(g, a, p):
    """
    Реализация алгоритма Похли-Хеллмана для вычисления дискретного логарифма.
    g: генератор группы
    a: элемент, для которого ищется логарифм
    p: модуль группы
    """
    n = p - 1
    factors = factorint(n)  # Возвращает словарь {простое: степень}
    print(f"Факторизация порядка группы: {n} -> {factors}")
    
    x_mods = []
    
    for q, e in factors.items():
        x_q = 0
        g_q = pow(g, n // q, p)
        a_q = pow(a, n // q, p)
        print(f"\nОбработка простого множителя {q}^{e}")
        for j in range(e):
            exponent = n // (q ** (j + 1))
            g_inv = mod_inverse(g, p)
            c = (a * pow(g_inv, x_q, p)) % p
            c = pow(c, exponent, p)
            
            # Решаем уравнение g_q^d ≡ c mod p, где d ∈ {0, 1, ..., q-1}
            r_ij = [pow(g_q, d, p) for d in range(q)]
            if c in r_ij:
                d = r_ij.index(c)
                print(f"  Шаг j={j}: c={c}, найден d={d}")
                x_q += d * (q ** j)
            else:
                raise ValueError(f"Не удалось найти d для q={q}, j={j}")
        x_mods.append((x_q, q ** e))
        print(f"  x ≡ {x_q} mod {q**e}")
    
    # Объединяем результаты с помощью Китайской теоремы об остатках
    x = 0
    for x_i, m_i in x_mods:
        n_i = n // m_i
        inv = mod_inverse(n_i, m_i)
        x += x_i * n_i * inv
        x %= n
    return x

# Входные данные
p = 101  # Модуль группы
g = 2    # Генератор
a = 3   # Элемент, для которого ищется логарифм

# Решение
result = pohlig_hellman_log(g, a, p)
print(f"\nlog_{g} {a} mod {p} = {result}")

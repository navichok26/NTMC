from sympy import factorint

def factorize_and_calculate(g, a, n):
    # Step 1: Factorize n-1
    factors = factorint(n - 1)
    formatted_factors = " * ".join([f"{factor}^{power}" for factor, power in factors.items()])
    print(f"раскладываем {n-1}: {formatted_factors}")

    p_list = list(factors.keys())
    for i, p in enumerate(p_list):
        print(f"p{i+1} = {p}")

    # Step 2: Precompute values for each prime factor
    a_values = [{} for _ in p_list]

    for idx, p in enumerate(p_list):
        a_values[idx][0] = 1
        a_values[idx][1] = pow(g, n // p, n)
        for i in range(2, p):
            a_values[idx][i] = pow(a_values[idx][1], i, n)

    print("\nсчитаем таблицы:")
    for i, a_dict in enumerate(a_values):
        # Вычисляем ширину колонок для выравнивания
        column_width = max(len(str(value)) for value in a_dict.values()) + 2
        index_width = max(len(str(key)) for key in a_dict.keys()) + 2

        # Заголовок таблицы
        header = f"a{i+1}:".ljust(4) + "|" + "|".join(f"{str(key).ljust(column_width)}" for key in a_dict.keys())
        values = "    |" + "|".join(f"{str(value).ljust(column_width)}" for value in a_dict.values())
        print(f"{header}|")
        print(f"{values}|")
        print()

    # Step 3: Calculate b0 and x0 for each factor
    x_values = []
    for idx, p in enumerate(p_list):
        b0 = pow(a, n // p, n)
        x0 = next(key for key, value in a_values[idx].items() if value == b0)
        print(f"b0_{idx+1} = {a}^{n // p} mod {n} = {b0}, x0_{idx+1} = {x0}")
        x_values.append(x0)

    # Step 4: Print modular equations
    m = []
    a_list = []
    print("\nсистема:")
    for i, (key, value) in enumerate(factors.items()):
        modulus = key ** value
        print(f"x = {x_values[i]} mod {modulus}")
        a_list.append(x_values[i])
        m.append(modulus)

    # Step 5: Return results for further processing (e.g., CRT)
    return a_list, m

def chinese_remainder_theorem(a_list, m_list):
    M = 1
    for m in m_list:
        M *= m

    m_products = [M // m for m in m_list]

    result = 0
    for i in range(len(a_list)):
        mi_inverse = pow(m_products[i], -1, m_list[i])
        result += a_list[i] * m_products[i] * mi_inverse

    return result % M

# Example usage
g = 2
a = 7
n = 61

# Factorize and calculate modular equations
a_list, m_list = factorize_and_calculate(g, a, n)

# Solve using Chinese Remainder Theorem
result = chinese_remainder_theorem(a_list, m_list)

# Print the final result
print(f"\nx = log{a}")
print(f"x = {result}")
print(f"ответ: {result}")

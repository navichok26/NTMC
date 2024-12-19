from sympy import factorint

def hellman(g, a, n):
    output = []

    def log(msg):
        output.append(msg)

    factors = factorint(n - 1)
    formatted_factors = " * ".join([f"{factor}^{power}" for factor, power in factors.items()])
    log(f"раскладываем {n-1}: {formatted_factors}\n")

    p_list = list(factors.keys())
    for i, p in enumerate(p_list):
        log(f"p{i+1} = {p}")

    a_values = [{0: 1} for _ in p_list]
    log(f"\nзначения для первых элементов таблиц всегда = 1\n")

    for idx, p in enumerate(p_list):
        a_values[idx][1] = pow(g, n // p, n)
        log(f"считаем значения таблицы a{idx+1}")
        log(f"a{idx+1}_1 = g^(n/p) mod n = {g}^{n}/{p} mod {n} = {g}^{n//p} mod {n} = {a_values[idx][1]}")

        for i in range(2, p):
            a_values[idx][i] = pow(a_values[idx][1], i, n)
            log(f"a{idx+1}_{i} = a{idx+1}_1^{i} mod {n} = {a_values[idx][i]}")
        log("")

    log("посчитали таблицы:")
    for i, a_dict in enumerate(a_values):
        column_width = max(len(str(value)) for value in a_dict.values()) + 2
        index_width = max(len(str(key)) for key in a_dict.keys()) + 2
        header = f"a{i+1}:".ljust(4) + "|" + "|".join(f"{str(key).ljust(column_width)}" for key in a_dict.keys())
        values = "    |" + "|".join(f"{str(value).ljust(column_width)}" for value in a_dict.values())
        log(f"{header}|")
        log(f"{values}|")
        log("")

    x_values = []
    for idx, p in enumerate(p_list):
        j = factors[p]
        b = a
        x_partial = []
        log(f"{idx}) для p = {p}; степень j = {j}\nx mod ")

        for k in range(j):
            b_k = pow(b, n // (p ** (k + 1)), n)
            x_k = next(key for key, value in a_values[idx].items() if value == b_k)
            x_partial.append(x_k)

            y = sum(x_partial[l] * (p ** l) for l in range(k + 1))
            b = (a * pow(g, -y, n)) % n

            log(f"  Шаг {k + 1}:\n    b = (a * g^(-y))^({n} / {p}^{k + 1}) mod {n}\n      = ({a} * {g}^(-{y}))^({n // (p ** (k + 1))}) mod {n}\n      = {b_k}\n   x{k} = {x_k}\n    y = {y}")
        log("")

        x = sum(x_partial[k] * (p ** k) for k in range(j))
        x_values.append(x)

    m = []
    a_list = []
    log("система:")
    for i, (key, value) in enumerate(factors.items()):
        modulus = key ** value
        log(f"x = {x_values[i]} mod {modulus}")
        a_list.append(x_values[i])
        m.append(modulus)

    log("\nm (список модулей):")
    for i, mod in enumerate(m, start=1):
        log(f"m{i} = {mod}" + (", " if i < len(m) else "\n"))

    def chinese_remainder_theorem(a_list, m_list):
        M = 1
        for m in m_list:
            M *= m
        log(f"\nОбщий модуль (M): {M}\n")

        m_products = [M // m for m in m_list]
        result = 0

        log("Расчеты для каждого элемента системы:")
        for i in range(len(a_list)):
            log(f"\nДля уравнения x ≡ {a_list[i]} (mod {m_list[i]}):")
            log(f"  M{i + 1} = M / m{i + 1} = {M} / {m_list[i]} = {m_products[i]}")
            mi_inverse = pow(m_products[i], -1, m_list[i])
            log(f"  Обратное к M{i + 1} (mod m{i + 1}): {mi_inverse}")
            term = a_list[i] * m_products[i] * mi_inverse
            log(f"  Термин: {a_list[i]} * {m_products[i]} * {mi_inverse} = {term}")
            result += term

        result = result % M
        log(f"\nРезультат (x): {result} (mod {M})")
        return result

    result = chinese_remainder_theorem(a_list, m)
    solve = "\n".join(output)

    return result, solve

g = 6
a = 14
n = 109
result = hellman(g, a, n)

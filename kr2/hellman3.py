from sympy import factorint

def factorize_and_calculate(g, a, n):
    # Step 1: Factorize n-1
    factors = factorint(n - 1)
    print(f"Factors of {n-1}: {factors}\n")

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

    print("\nPrecomputed values as tables:")
    for i, a_dict in enumerate(a_values):
        print(f"a{i+1}")
        headers = "{:>5}".format("") + "".join("{:>5}".format(k) for k in a_dict.keys())
        values = "{:>5}".format("a") + "".join("{:>5}".format(v) for v in a_dict.values())
        print(headers)
        print(values)
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
    print("\nModular equations:")
    for i, (key, value) in enumerate(factors.items()):
        modulus = key ** value
        print(f"x = {x_values[i]} mod {modulus}")
        a_list.append(x_values[i])
        m.append(modulus)

    # Step 5: Return results for further processing (e.g., CRT)
    return a_list, m, x_values

# Example usage:
g = 2
a = 7
n = 61

a, m, x = factorize_and_calculate(g, a, n)
M = m[0] * m[1] * m[2]
m_list = [m[1]*m[2],
          m[0]*m[2],
          m[0]*m[1]]

Z=[]
result = 0
for i in range(3):
    tmp = pow(m_list[i], -1, m[i])
    Z.append(tmp % m[i])
    print(f"{m_list[i]} * {Z[i]} * {a[i]}; {m_list[i]*Z[i]*a[i]}")  
    result += m_list[i]*Z[i]*a[i]

print(result)
print(result % M)

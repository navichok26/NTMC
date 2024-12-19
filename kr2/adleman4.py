from sympy import factorint

# Input parameters
n = 109
g = 6
S = [2, 3, 5]
print(f"1)")
print(f"факторная база: {S}\n\n2)")

def find_log_a(a, n, g, S):
    """
    Function to calculate log(a) mod (n-1) using the given parameters.
    
    Args:
        a (int): The number for which to find the logarithm.
        n (int): The modulo base.
        g (int): The generator.
        S (list): The set of allowed prime factors.

    Returns:
        int: The value of log(a) mod (n-1).
    """
    single_factor_dict = {}

    for k in range(1, n):
        if k == 1 or g**k > n:
            val = pow(g, k, n)  # (g^k) mod n
            factors = factorint(val)

            all_in_S = all(prime in S for prime in factors.keys())

            if all_in_S:
                # Check if the factorization consists of only one number in the first degree
                if len(factors) == 1 and list(factors.values())[0] == 1:
                    single_factor_dict[val] = k
                    print(f"возьмём случайное k = {k}: b = {g}^{k} = {val} mod {n} => log{val} = {k}")

    print(f"\nполучили систему уравнений:")
    for base, value in single_factor_dict.items():
        print(f"log({base}) = {value}")
    print(f"\nтак получилось, что случайно подобрали удачные k, что систему уравнений решать не надо")
    print(f"пропускаем пункт 3\n\n4)")
    for k in range(1, n):
        product = (a * pow(g, k, n)) % n  # a * g^k 
        factors = factorint(product)
        

        all_in_S = all(prime in S for prime in factors.keys())
        if all_in_S:
            print(f"k = {k}: {a} * {g}^{k} = {product} mod {n}, раскладывается в S")
        else:
            print(f"k = {k}: {a} * {g}^{k} = {product} mod {n}, не раскладывается в S")
        log_a = 0
        str1 = ""
        str2 = ""
        if all_in_S:
            for prime, power in factors.items():
                str1 += f"{power}*log{prime} + "
                if prime in single_factor_dict:
                    log_a += single_factor_dict[prime] * power
                    str2 += f"{power}*{single_factor_dict[prime]} + "
            log_a -= k
            log_a = log_a % (n-1)
            print(f"log{a} + {k}*log{g} = {str1[:-3]} mod {n-1}")
            print(f"переходим к значениям логарифмов:")
            print(f"log{a} + {k} = {str2[:-3]} mod {n-1}")
            print(f"сокращаем и переносим")
            print(f"log{a} = {log_a} mod {n-1}")
            print(f"ответ: {log_a}")
            return log_a

    print("No valid logarithm found.")
    return None

# Example usage
a = 14
result = find_log_a(a, n, g, S)

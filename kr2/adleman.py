from sympy import factorint

def adleman(g, a, n):
    """
    Function to calculate log(a) mod (n-1) using the given parameters.

    Args:
        a (int): The number for which to find the logarithm.
        n (int): The modulo base.
        g (int): The generator.
        S (list): The set of allowed prime factors.

    Returns:
        tuple: The value of log(a) mod (n-1) and the full log output.
    """

    S = [2, 3, 5]
    output = []

    def log(msg):
        output.append(msg)

    single_factor_dict = {}

    log(f"1)\nфакторная база: {S}\n\n2)")

    for k in range(1, n):
        if k == 1 or g**k > n:
            val = pow(g, k, n)  # (g^k) mod n
            factors = factorint(val)

            all_in_S = all(prime in S for prime in factors.keys())

            if all_in_S:
                if len(factors) == 1 and list(factors.values())[0] == 1:
                    single_factor_dict[val] = k
                    log(f"возьмём случайное k = {k}: b = {g}^{k} = {val} mod {n} => log{val} = {k}")

    log(f"\nполучили систему уравнений:")
    for base, value in single_factor_dict.items():
        log(f"log({base}) = {value}")
    log(f"\nтак получилось, что случайно подобрали удачные k, что систему уравнений решать не надо")
    log(f"пропускаем пункт 3\n\n4)")

    for k in range(1, n):
        product = (a * pow(g, k, n)) % n  # a * g^k 
        factors = factorint(product)

        all_in_S = all(prime in S for prime in factors.keys())
        if all_in_S:
            log(f"k = {k}: {a} * {g}^{k} = {product} mod {n}, раскладывается в S")
        else:
            log(f"k = {k}: {a} * {g}^{k} = {product} mod {n}, не раскладывается в S")

        if all_in_S:
            log_a = 0
            str1 = ""
            str2 = ""

            for prime, power in factors.items():
                str1 += f"{power}*log{prime} + "
                if prime in single_factor_dict:
                    log_a += single_factor_dict[prime] * power
                    str2 += f"{power}*{single_factor_dict[prime]} + "

            log_a -= k
            log_a = log_a % (n - 1)

            log(f"log{a} = {str1[:-3]} - {k} mod {n-1}")
            log(f"переходим к значениям логарифмов:")
            log(f"log{a} = {str2[:-3]} - {k} mod {n-1}")
            log(f"сокращаем и переносим")
            log(f"log{a} = {log_a} mod {n-1}")
            log(f"ответ: {log_a}")

            return log_a, "\n".join(output)

    log("No valid logarithm found.")
    return None, "\n".join(output)

# Example usage
if __name__ == "__main__":
    g = 6
    a = 14
    n = 109

    result, log_output = adleman(g, a, n)
    print(log_output)

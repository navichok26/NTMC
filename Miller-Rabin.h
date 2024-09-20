#ifndef MILLER_RABIN_H
#define MILLER_RABIN_H

#include <iostream>
#include <cstdlib>
#include <cmath>

BN phi(BN n) {
    BN result = n;
    BN p;
    BN zero, one;
    zero = 0; one = 1; p = 2;
    while (p * p <= n) {
        if (n % p == zero) {
            while (n % p == zero) {
                n = n / p;
            }
            result = result - result / p;
        }
        p = p + one;
    }
    if (n > one) {
        result = result - result / n;
    }
    return result;
}

bool test_miller_rabin(BN n, int t) {
    BN zero, one, two, three;
    zero = 0; one = 1; two = 2; three = 3;
    if (n <= three) {
        cout << "Для проверки числа на простоту, оно должно быть больше 3" << endl;
        return false;
    }
    BN r = n - one;
    BN s = zero;
    while (r % two == zero) {
        r = r / two;
        s = s + one;
    }
    for (int i = 0; i < t; i++) {
        BN tmp;
        tmp = rand();
        BN b = two + tmp % (n - three);
        BN y = b.pow_mod(r, n);
        if (y != one) {
            BN j = one;
            while (j < s && y != n - one) {
                y = y * y % n;
                if (y == one) {
                    return false;
                }
                j = j + one;
            }
            if (y != n - one) {
                return false;
            }
        }
    }
    return true;
}

void error_phi(BN n, int t) {
    BN phi_val = phi(n);
    double X = std::pow(phi_val.to_double() / (4 * n.to_double()), t);
    cout << "Вероятность ошибки = " << X << endl;
}


#endif // MILLER_RABIN_H

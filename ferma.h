#ifndef FERMAT_H
#define FERMAT_H

#include "big_number.h"
#include <iostream>

BN* Ferma_algorithm(BN n) {
    BN x = n.root(2);
    BN* d = new BN[2];
    BN one, y, z;
    one = 1;
    if (x.square() == n) {
        d[0] = x;
        d[1] = x;
        return d;
    }
    while (y.square() != z) {
        x = x + one;
        if (x == (n + one) / 2) {
            std::cout << "n is prime\n";
            return d;
        }
        z = x.square() - n;
        y = z.root(2);
    }
    d[0] = x + y;
    d[1] = x - y;
    return d;
}

void run_ferma() {

    BN n;
    cout << "Введите число для факторизации: ";
    n.cin_base10();

    BN* result = Ferma_algorithm(n);
    cout << "Результат факторизации методом Ферма: ";
    cout << "d1 = "; 
    result[0].cout_base10(); 
    cout << ", d2 = "; 
    result[1].cout_base10(); 
    cout << endl;
    delete[] result;
}

#endif // FERMAT_H

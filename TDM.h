#ifndef TDM_H
#define TDM_H

#include <iostream>
#include <vector>
#include "big_number.h"
#include "Miller-Rabin.h"
#include <cmath>

using namespace std;

vector<BN> TDM_algo(const BN &num) {
    BN n = num;
    vector<BN> d(3);
    BN temp;
    d[0] = 3;
    d[1] = 5;
    d[2] = 7;

    vector<BN> p;
    BN sqrt = n.root(2);
    int k = 0;
    BN zero, one, two, six;
    zero = 0; one = 1; two = 2; six = 6;

    while (n != one) {
        if (n % 2 != zero) {
            BN r = n % d[k];
            BN q = n / d[k];
            if (k > 0 && zero < r && r < d[k] && q < d[k] && n % d[k - 1] != zero) {
                p.push_back(n);
                return p;
            } else if (r == zero) {
                p.push_back(d[k]);
                n = q;
            } else {
                if (q > d[k] && d[k] <= sqrt) {
                    k++;
                    if (k > 2) {
                        temp = d[k - 2] + six;
                        d.push_back(temp);
                    }
                } else {
                    p.push_back(n);
                    return p;
                }
            }
        } else {
            p.push_back(two);
            n = n / 2;
        }
    }
    return p;
}

void run_TDM() {
    int reliability = 5;
    BN num, one, three;
    one = 1; three = 3;
    num.cin_base10();

    if (test_miller_rabin(num, reliability)) {
        num.cout_base10();
        cout << " простое." << endl;
        error_phi(num, reliability);
    } else if (num <= one) {
        cout << "число должно быть > 1" << endl;
    } else if (num <= three) {
        return;
    } else {
        vector<BN> p = TDM_algo(num);

        BN zero;
        num.cout_base10();
        cout << " = ";

        for (size_t i = 0; i < p.size(); i++) {
            if (i != 0) {
                cout << " * ";
            }
            p[i].cout_base10();
        }
    }

    cout << endl;
}

#endif // TDM_H
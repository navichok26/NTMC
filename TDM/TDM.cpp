#include <iostream>
#include <vector>
#include "BigNum.h"
#include "Miller-Rabin.h"
#include <cmath>

using namespace std;

vector<BN> TDM(const BN &num) {
    BN n = num;
    vector<BN> d(3);
    BN temp;
    d[0] = 3; 
    d[1] = 5; 
    d[2] = 7;
    
    vector<BN> p; 
    BN sqrt = n.sqrt_BN();
    int k = 0;
    BN zero = 0;

    while (n != 1) {
        if (n % 2 != 0) {
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
                        if (k % 2 != 0) {
                            temp = d[k - 1] + 2;
                        } else {
                            temp = d[k - 1] + 4;
                        }
                        d.push_back(temp); 
                    }
                } else {
                    p.push_back(n); 
                    return p;
                }
            }
        } else {
            p.push_back(2);
            n = n / 2;
        }
    }
    return p;
}


int main() {
    int reliability = 5;
    BN num, one = 1, three = 3;
    num.cin_base10();

    if (test_miller_rabin(num, reliability)) {
        num.cout_base10();
        cout << " простое." << endl;
        error_phi(num, reliability);
    } else if (num <= one) {
        cout << "число должно быть > 1" << endl;
    } else if (num <= three) {
        return 0;
    } else {
        vector<BN> p = TDM(num); 

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

    // BN a, b, c;
    // a = 9876;
    // b = 12345;
    // c = a.gcd(b);
    // cout << endl << "Наибольший общий делитель: ";
    // c.cout_base10();

    return 0;
}
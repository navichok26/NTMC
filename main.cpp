#include <iostream>
#include <string>

#include "TDM.h"
#include "alway.h"
#include "ferma.h"

using namespace std;

int main(int argc, char* argv[]) {

    if (argc < 2) {
        cerr << "Ошибка: не указан алгоритм.\n";
        cerr << "Использование: ./program [tdm|alway|ferma|pollard]\n";
        return 1;
    }

    string algo = argv[1];

    if (algo == "tdm" || algo == "lab1") {
        cout << "Запущен алгоритм TDM\n";
        run_TDM();
    } 
    
    else if (algo == "alway" || algo == "lab2") {
        cout << "Запущен алгоритм alway\n";
        run_Alway();
    } 
    
    else if (algo == "ferma" || algo == "lab3") {
        cout << "Запущен алгоритм ferma\n";
        run_ferma();
    } 
    
    else if (algo == "pollard" || algo == "lab4") {
        cout << "Запущен алгоритм Полларда\n";
        cout << "Метод Полларда ещё не реализован\n";
    } 
    
    else {
        cerr << "Ошибка: неизвестный аргумент '" << algo << "'.\n";
        cerr << "Использование: ./program [tdm|alway|ferma|pollard]\n";
        return 1;
    }

    return 0;
}

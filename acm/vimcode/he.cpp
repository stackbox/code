#include <iostream>
#include <fstream>
using namespace std;

int main() {
    int a,b;
    ifstream in("he.txt");
    in >> a >> b;
    cout << a << " "<< b;
    return 0;
}


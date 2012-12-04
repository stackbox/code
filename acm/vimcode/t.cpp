#include <iostream>
using namespace std;
int fun(int);

int main(){
    int a(3);
    static int b;
    b+=fun(a);
    cout << a << " " << b << endl;
    b+=fun(a);
    
    cout << a << " " << b << endl;
    return 0;
}

static int a(10);
int fun(int x)
{
    static int b(5);
    b += a;
    cout << a << " " << b << endl;
    return b;
}

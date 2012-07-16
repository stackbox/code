#include <iostream>
using namespace std;

long feb(long n)
{
    if(n == 0) return 0;
    if(n == 1) return 1;
    else return feb(n-1) + feb(n-2);
}

int main()
{
    cout << feb(4) << endl;
    cin.get();
    return 0;
}

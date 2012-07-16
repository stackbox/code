#include <iostream>
using namespace std;

long test(long n)
{
    long result = 1;
    for(long i = 1; i <= n; i++)
    {
        result *= i;
    }
    return result;
}


int main()
{
    cout << test(5) << endl;
    system("pause");
    return 0;
}

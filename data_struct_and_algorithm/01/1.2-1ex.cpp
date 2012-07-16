#include <iostream>
using namespace std;

template <class T>
bool Input(T& myNum)
{
    int times = 3;
    T input;
    while(times--)
    {
        cin >> input;
        if(input >= 0)
        {
            myNum = input;
            return true;
        }
    }
    return false;
}

int main()
{
    float a;
    if(Input(a))
    {
        cout  << a << endl;
    }
    
    system("pause");
    return 0;
}

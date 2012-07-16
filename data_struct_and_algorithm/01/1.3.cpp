#include <iostream>
using namespace std;

template <class T>
inline void Swap(T& a,T& b)
{
    T temp = a;
    a = b;
    b = temp;
}

template <class T>
void Perm(T list[],int k,int m)
{
    int i;
    if(k == m)
    {
        for(i = 0; i <= m; i++)
            cout << list[i];
        cout << endl;
    }
    else
        for(i = k; i <= m; i++)
        {
            Swap(list[k],list[i]);
            Perm(list,k+1,m);
            Swap(list[k],list[i]);
        }
}

int main()
{
    char a[] = {'a','b','c','d','e'};
    Perm(a,0,4);
    
    cin.get();
    return 0;
}

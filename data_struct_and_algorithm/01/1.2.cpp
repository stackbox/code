#include <iostream>
#include <stdio.h>
using namespace std;

template<class T>
T Sum(T a[],int n)
{
    T tsum = 0;
    for(int i = 0; i < n; i++)
        tsum += a[i];
    return tsum;
}

template<class T>
T Rsum(T a[],int n)
{
    if(n > 0)
        return Rsum(a,n-1) + a[n-1];
    return 0;
}


int main()
{
    double a[] = {1.0,2.0,3.0,4.0};
    cout << Sum(a,4) << endl;
    cout << Rsum(a,4) << endl;
    return 0;
}

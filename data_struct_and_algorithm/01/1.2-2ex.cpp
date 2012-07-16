#include <iostream>
using namespace std;

template <class T>
bool Ascending(T list[],int n)
{
    for(int i = 0; i < n-1; i++)
    {
        if(list[i] > list[i+1])
        return false;
    }
    return true;
}

int main()
{
    int list1[] = {1,2,3,4,5};
    int list2[] = {1,2,3,5,4};
    
    if(Ascending(list1,5)) cout << "true" << endl;
    
    if(!Ascending(list2,5)) cout << "false" << endl;
    
    system("pause");
    return 0;
}

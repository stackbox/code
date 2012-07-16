#include <iostream>
#include <algorithm>
using namespace std;

int main()
{
    int n,t,i;
    cin >> n;
    while(n--)
    {
	int arr[1001];
	cin >> t;
	for(i=0; i < t; i++)
	    cin >> arr[i];
	sort(arr,arr+t);
	for(i=0; i < t-1; i++)
	    cout << arr[i] << " ";
	cout << arr[t-1] << endl;
    }
    return 0;
}


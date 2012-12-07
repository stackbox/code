#include <iostream>
using namespace std;

int main()
{
    int A,B,n,i,start,end,arr[51];
    while(cin >> A >> B >> n)
    {
	if(A==0 && B==0 && n==0) break;
	arr[1]=1;
	arr[2]=1;
	for(i=3; i <51; i++)
	{
	    arr[i]=(A*arr[i-1]%7 + B*arr[i-2]%7)%7;
	    for(int j=1; j < i-1; j++)
	    {
		if(arr[j]==arr[i-1] && arr[j+1] == arr[i])
		{
		    start=j;
		    end=i-1;
		    break;
		}
	    }
	}
	if(n <= end) cout << arr[n] << endl;
	    else {
		int pos = (n-start)%(end-start);
		cout << arr[start+pos] << endl;
	    }
    }
    return 0;
}




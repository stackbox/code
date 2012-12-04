#include <iostream>
#include <cstring>
using namespace std;

const int prime_arr[12]={2,3,5,7,11,13,17,19,23,29,31,37};
int flag[20];

bool isprime(int n)
{
    int i;
    for(i=0; i < 12; i++)
    {
	if(prime_arr[i] == n) return true;
	if(prime_arr[i] > n) return false;
    }
    return false;
}


void dfs(int arr[],int n,int pos)
{
    if(pos == n && isprime(arr[n]+1))
    {
	for(int i=1; i < n; i++)
	    cout << arr[i] << " ";
	cout << arr[n] << endl;
    }
    else
    {
	for(int i=2; i <= n; i++)
	{
	    if(!flag[i]&& isprime(i+arr[pos]))
	    {
		arr[pos+1] = i;
		flag[i]=1;
		dfs(arr,n,pos+1);
		flag[i]=0;
	    }
	}
    }
}

int main()
{
    int arr[20],n,icase=1;
    while(cin >> n)
    {
	memset(flag,0,sizeof(flag));
	flag[0]=1;
	flag[1]=1;
        arr[1]=1;
	cout << "Case " << icase++ << ":" << endl;
        dfs(arr,n,1);
	cout << endl;
    }
    return 0;
}


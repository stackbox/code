#include <iostream>
using namespace std;

int main() {
    int n,u,d,sum;
    while(cin >> n >> u >> d)
    {
	if(n==0) break;
	if((n-u)%(u-d)==0) sum=2*(n-u)/(u-d)+1;
	else sum=2*((n-u)/(u-d)) + 3;
	cout << sum << endl;
    }
    return 0;
}

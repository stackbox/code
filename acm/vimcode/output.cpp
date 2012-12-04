#include <iostream>
using namespace std;

int main()
{
    int N,M,i,sum,tmp,flag=0;
    cin >> N;
    while(N--) {
	cin >> M;
	for(i=0,sum=0;i < M; i++) {
	    cin >> tmp;
	    sum += tmp;
	}
	if(flag!=0) cout << endl;
	cout << sum << endl;
	flag=1;
    }
    return 0;
}

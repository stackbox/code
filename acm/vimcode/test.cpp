#include <iostream>
#include <cstring>
using namespace std;

int prime[1000002];

void initPrime() {
    memset(prime,-1,sizeof(prime));
    int  i,j,k,pos = 0;
    for(i = 2; i < 1000002; i++) {
	if(prime[i] == -1) {
	    pos++;
	    for(j = i; j < 1000002; j += i) {
		prime[j] = pos;
	    }
	}
    }
    prime[1] = 0;
}

int main() {
    int n;
    initPrime();
    while(scanf("%d",&n) != EOF) 
    {
	printf("%d\n",prime[n]);
    }
    return 0;
}

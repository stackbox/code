#include <iostream>
#include <cstring>
using namespace std;

int qixi[500005];
int initQixi() {
    memset(qixi,0,500005);
    int i,j;
    for(i = 1; i <= 250001 ; i++) {
	for(j = 2*i; j <= 500000; j += i) {
	    qixi[j] += i;
	}
    }
}

int main() {
    int T,n;
    initQixi();
    cin >> T;
    while(T--) {
	cin >> n;
	cout << qixi[n] << endl;
    }
    return 0;
}

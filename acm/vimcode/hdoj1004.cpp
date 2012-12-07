#include <iostream>
#include <algorithm>
using namespace std;

int main()
{
    string s[1001],max;
    int N,num,tmp,i;
    while(cin >> N) {
	if(N==0) break;
	for(i=0; i < N; i++)
	    cin >> s[i];
	sort(s,s+N);
	max=s[0];
	num=1;
	tmp=1;
	for(i=0;i < N; i++) {
	    while(s[i]==s[i+1]) {
		i++;
		tmp++;
	    }
	    if(tmp > num) {
		num=tmp;
		max=s[i];
	    }
	    tmp=1;
	}
	cout << max << endl;
    }
    return 0;
}

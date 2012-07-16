#include <iostream>
#include <cstring>
using namespace std;

int main()
{
    char in[10005];
    
    int times,N;
    cin >> N;
    while(N--) {
	cin >> in;
	for(int i=0; i < strlen(in); i++) {
	    cout << in[i];
	    times=1;
	    while(1) {
		if(in[i]==in[i+1]) {
		    times++;
		    i++;
		} else {
		    break;
		}
	    }
	   if(times!=1) cout << times;
	}
	cout << endl;
    }
    return 0;
}

#include <iostream>
using namespace std;

int main() {
    int N,i,preFloor,aimFloor,sumSec;
    while(cin >> N)
    {
	if(N==0) break;
	preFloor=0;
	sumSec=0;
	for(i=0; i < N; i++) {
	    cin >> aimFloor;
	    if(aimFloor > preFloor) {
		sumSec += (6*(aimFloor-preFloor)+5);
		preFloor=aimFloor;
	    }
	    else {
		sumSec += (4*(preFloor-aimFloor)+5);
		preFloor=aimFloor;
	    }
	}
	cout << sumSec << endl;
    }
    return 0;
}

#include <iostream>
using namespace std;

int main()
{
    int T,N,arr[100001],i,s,e,startPos,endPos,maxSum,lastSum;
    cin >> T;
    for(int k=1; k <= T; k++) {
	cin >> N;
	for(i=1;i <= N; i++)
	    cin >> arr[i];
	startPos=1;
	endPos=1;
	s=1;
	e=1;
	maxSum=arr[1];
	lastSum=arr[1];
	for(i=2;i <= N; i++)
	{
	    if(lastSum >=0 ) {
		e=i;
		lastSum += arr[i];
	    } else {
		s=i;
		e=i;
		lastSum = arr[i];
	    }
	    if(lastSum > maxSum) {
	        startPos=s;	
		endPos=e;
		maxSum=lastSum;
	    }
	}
        if(k!=1) cout << endl;
	cout << "Case " << k << ":\n" << maxSum;
	cout << " " << startPos << " " << endPos <<endl; 
    }
    return 0;
}


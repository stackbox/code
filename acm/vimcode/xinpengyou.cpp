#include <iostream>
using namespace std;

int euler(int x) {
    int result = 1;
    for(int i = 2;  i*i <= x; ++i) {
	if( x%i == 0)
	{
	    x /= i;
	    result *= (i -1);
	    while(x % i == 0) {
		x /= i;
		result *= i;
	    }
	}
    }
    if( x > 1)
    {
	result *= (x-1);
    }
    return result;
}

int main() {
    int CN,N;
    cin >> CN;
    while(CN--) {
	cin >> N;
	cout << euler(N) << endl;
    }
    return 0;
}


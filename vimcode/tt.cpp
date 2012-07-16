#include <iostream>
#include <cmath>
#include <sstream>
#include <algorithm>
#include <cstring>
using namespace std;

int Gcd(int m,int n) {
    return m==0 ? n : Gcd(n%m,m);
}

int main() {
    int T;
    cin >> T;
    while(T--) {
	string s;
	cin >> s;
	istringstream input(s);
	char ch;
	int dot = s.find_first_of('.',0);
	int start = s.find_first_of('(',0);
	int end = s.find_first_of(')',0);
	int x = 0,y = 0,p = 0,q = 0;
	if(start == string::npos) {
	    p = s.length() - dot - 1;
	    input >> x >> ch >> x;
	    int demo1 = (int)(pow(10.0,p));
	    int gcd1 = Gcd(x,demo1);
	    cout << x/gcd1 << "/" << demo1/gcd1 << endl;
	}
	else
	{
	    if(s[dot+1] != '(') {
	        input >> x >> ch >> x >> ch >> y;
 	    } else {
		input >> x >> ch >> ch >> y;
	    }
	    p = start - dot -1;
	    q = end - start -1;

	    int numer2 = (int) (y + pow(10.0,q)*x - x);
	    int demo2 = (int) (pow(10.0,p+q) - pow(10.0,p));
	    int gcd2 = Gcd(numer2,demo2);
	    cout << numer2/gcd2 << "/" << demo2/gcd2 << endl;
	}
    }
    return 0;
}

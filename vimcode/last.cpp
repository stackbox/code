#include <iostream>
#include <cmath>
#include <cstring>
#include <algorithm>
#include <sstream>
using namespace std;

int Gcd(int m,int n) {
    return m==0 ? n : Gcd(n%m, m);
}

int main() {
    int T;
    cin >> T;
    while(T--) {
	string s;
	cin >> s;
	istringstream input(s);
	size_t dot = s.find_first_of('.',0);
	size_t start = s.find_first_of('(',0);
	size_t end = s.find_first_of(')',0);
	if(start == string::npos) {
	    int t;
	    char ch;
	    input >> t >> ch >> t;
	    int numer,demo;
	    numer = t;
	    demo = (int)(pow(10,s.length() - dot - 1));
	    int gcd1 = Gcd(numer,demo);
	    cout << numer/gcd1 << "/" << demo/gcd1 << endl; 
	}
	else {
	   int t,numer1,demo1,numer2,demo2;
	   char ch;
	   input >> t >> ch >> t >> ch >> numer2;
	   numer1 = t;
	   demo1 = (int)(pow(10,start-dot-1));
	   int gcd2 = Gcd(numer1,demo1);
	   numer1 /= gcd2;
	   demo1 /= gcd2;
	   
	   demo2 = (int)(pow(10,end - dot -2) - pow(10,end - start -1));
	   int gcd3 = Gcd(numer2,demo2);
	   numer2 /= gcd3;
	   demo2  /= gcd3;
           
	   cout << numer2 << " " << demo2 << endl;
	   int numer3 = demo1*numer2 + demo2*numer1;
	   int demo3 = demo1*demo2;

	   cout << numer3/Gcd(numer3,demo3) << "/" << demo3/Gcd(numer3,demo3) << endl;

	}
    }
    return 0;
}

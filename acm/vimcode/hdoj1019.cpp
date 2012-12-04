#include <iostream>
using namespace std;

int Gcd(int m,int n) {
    return m==0 ? n : Gcd(n%m, m);
}

int Lcm(int m,int n) {
    return (m*(n/Gcd(m,n)));
}

int main()
{
    int n,k,i,lcm,tmp;
    cin >> n;
    while(n--) {
	cin >> k;
	cin >> lcm;
	for(i=1; i < k; i++) {
	    cin >> tmp;
	    if(lcm%tmp != 0) {
		lcm = Lcm(lcm,tmp);
	    }
	}
	cout << lcm << endl;
    }
    return 0;
}
	    
	

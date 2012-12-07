#include <iostream>
using namespace std;
int main()
{
    const int wheeler = 168;
    int s[3],i;
    while(cin >> s[0] >> s[1] >> s[2]) {
	for(i=0; i <3; i++) {
	    if(s[i] <= wheeler) break;
	}
	if(i==3) cout << "NO CRASH" << endl;
	else cout << "CRASH " << s[i] << endl;
    }
    return 0;
}

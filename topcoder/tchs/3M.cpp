#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>
using namespace std;


class KidsWordGame
{
	public:
		static bool ok(string a,string b);
		int getCheater(vector <string> first, vector <string> second, vector <string> third);
};

bool KidsWordGame::ok(string a,string b)
{
	if((b.length() == a.length() + 1) && (b.find(a) != string::npos)) return true;
	else return false;
}

int KidsWordGame::getCheater(vector <string> first, vector <string> second, vector <string> third)
{
	int n = max(first.size(),max(second.size(),third.size()));
	vector <string>::iterator iterA = first.begin();
	vector <string>::iterator iterB = second.begin();
	vector <string>::iterator iterC = third.begin();

	string s = first.front();
	for(int i = 0; i < n; i++)
	{
		if(i == first.size()) break;
		if(i== 0 || ok(s, *(iterA + i))) s = *(iterA+i);
		else return 3;

		if(i == second.size()) break;
		if(ok(s, *(iterB + i))) s = *(iterB+i);
		else return 1;

		if(i == third.size()) break;
		if(ok(s, *(iterC + i))) s = *(iterC+i);
		else return 2;
	}
	return -1;
}

int main()
{

  	vector <string> first(1,"ello");
	vector <string> second(1,"hello");
	vector <string> third(1,"ello");



	KidsWordGame s;
	s.getCheater(first,second,third);
	cout << "end" << endl;

    return 0;
}

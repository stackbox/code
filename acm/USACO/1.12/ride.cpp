/*
ID: xi-lin2
LANG: C++
PROG: ride 
*/

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int getValue(string &s);

int main()
{
	ifstream fin("ride.in");
	ofstream fout("ride.out");
	string in;
	int val1,val2;
	fin >> in;
	val1 = getValue(in);
	fin >> in;
	val2 = getValue(in);
	if(val1 == val2)
		fout << "GO" << endl;
	else
		fout << "STAY" << endl;


return 0;
}

int getValue(string &s)
{
	int count = 1;
	for(int i = 0; i < s.length(); i++)
	{
		count = count * (s[i] - 'A'+ 1) % 47;
	}
	return count;
}

	

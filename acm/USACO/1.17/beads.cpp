/*
ID: xi-lin2
LANG: C++
PROG: beads
*/

#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int count(string s,int pos);
int countTmp(string s,int pos,int flag);

int main()
{
	int length,i,j,pre;
	string s;
	ifstream fin("beads.in");
	ofstream fout("beads.out");

	fin >> length;

	cout << length << " " ;
	fin >> s;
	cout << s << endl;

	for(int i = 0; i  < length; i++)
		cout << count(s,i) << endl;
		


	return 0;
}

int count(string s, int pos)
{
	int posA,posB;
	posA = pos;
	if(pos == 0) posB = s.length() -1;
	else posB = pos-1;

	return countTmp(s,posA,1)+countTmp(s,posB,-1);
}

int countTmp(string s, int pos,int flag)
{
	int count = 0;
	char key = s[pos];
	int pre = pos;
	int tag;
	if(flag > 0) tag = 1;
	else tag = -1;

	while(1)
	{
		if(s[pre] == key || s[pre] == 'w')
		{
			count ++;
			break;
		}
		pre += tag;
		if(pre >= s.length()) pre = 0;
		if(pre < 0) pre = s.length() -1;
	}
	cout << "$$$" << key<< count << endl;
	return count;
}
	
			


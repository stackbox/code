#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;

class KingSort
{
	public:
		static int getV(string s);
		static bool cmp(string a,string b);
		vector <string> getSortedList(vector <string> kings);
};

int KingSort::getV(string s)
{
	string num1[10] = {"","I","II","III","IV","V","VI","VII","VIII","IX"};
	string num2[6] = {"","X","XX","XXX","XL","L"};
	for(int i = 0; i < 6; i++)
		for(int j = 0; j < 10; j++)
		{
			string tmp = num2[i] + num1[j];
			if(tmp == s)
				return (10*i + j);
		}
	return -1;
}

bool KingSort::cmp(string a,string b)
{
	istringstream ina(a);
	istringstream inb(b);
	string acA,acB;
	ina >> acA;
	inb >> acB;
	if(acA != acB)
	{
		return acA < acB;
	}
	else
	{
		ina >> acA;
		inb >> acB;
		return getV(acA) < getV(acB);
	}
}

vector <string> KingSort::getSortedList(vector <string> kings)
{
	sort(kings.begin(),kings.end(),cmp);
	return kings;
}
int main()
{

	return 0;
}



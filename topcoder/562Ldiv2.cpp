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

class CucumberMarket
{
	public:
		string check(vector <int> price, int budget, int k);
};

bool cmp(int a,int b)
{
	if( a > b) return true;
	else return false;
}

string CucumberMarket::check(vector <int> price, int budget, int k)
{
	sort(price.begin(),price.end(),cmp);
	int sum = 0;
	for(int i = 0; i < k; i++)
	{
		sum += price[i];
	}
	if(sum > budget) return "NO";
	else return "YES";
		
}

int main()
{

	return 0;
}



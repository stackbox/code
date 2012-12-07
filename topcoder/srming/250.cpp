#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

class FoxAndVacation
{
	public:
		int maxCities(int total, vector <int> d);
};

int FoxAndVacation::maxCities(int total, vector <int> d)
{
	sort(d.begin(),d.end());
	int counts=0,sum=0;
	for(vector <int>::iterator iter = d.begin(); iter != d.end() ; iter++)
	{
		sum += *iter;
		if(sum > total) break;
		counts++;
	}
	return counts;
}
int main()
{

	return 0;
}



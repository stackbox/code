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

class BestSeller
{
	public:
		string findBestSeller(vector <string> items);
};

string BestSeller::findBestSeller(vector <string> items)
{
	sort(items.begin(),items.end());
	string tmp = items.front(),best;
	int count = 0,max = -1;
	for(vector <string>::iterator iter = items.begin(); iter != items.end(); iter++)
	{
		if(*iter == tmp) {
			count++;
			if(count > max) {
				max = count;
				best = tmp;
			}
		}
		else
		{
			tmp = *iter;
			count = 1;
		}
	}
	return best; 
}
int main()
{

	return 0;
}

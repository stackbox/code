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

class WinningTrick
{
	public:
		double minimumSpeed(vector <int> speed, int yourSpeed);

};

double WinningTrick::minimumSpeed(vector <int> speed, int yourSpeed)
{
	int maxV = -1;
	for(vector <int>::iterator iter = speed.begin(); iter != speed.end(); iter++)
	{
		if(*iter > maxV)
			maxV = *iter;
	}

	if(yourSpeed >= maxV) return 0.0;
	else
	{
		double reV = (double)(maxV - yourSpeed);
		return reV/2.0;
	}
}
int main()
{

	return 0;
}



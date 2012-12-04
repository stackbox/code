#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <string.h>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

class SpeedRadar
{
	public:
		double averageSpeed(int minLimit, int maxLimit, vector <int> readings);
};

double SpeedRadar::averageSpeed(int minLimit, int maxLimit, vector <int> readings)
{
	int count = 0,sum = 0;
	for(vector <int> ::iterator iter = readings.begin(); iter != readings.end(); iter++)
	{
		if( *iter > maxLimit || *iter < minLimit)
			count++;
		else sum += *iter;
	}
	double ave = sum*1.0/(readings.size() - count);
	if(count*1.0/readings.size() > 0.1) return 0.0;
	else return ave;
}

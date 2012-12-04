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

class PairingPawns
{
	public:
		int savedPawnCount(vector <int> start);
};

int PairingPawns::savedPawnCount(vector <int> start)
{
	for(vector <int>::iterator iter = start.end() -1; iter > start.begin(); iter--)
	{
		*(iter-1) += (*iter)/2;
	}
	return start.front();
}
int main()
{

	return 0;
}



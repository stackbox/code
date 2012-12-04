#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <vector>
#include <cmath>
#include <vector>
#include <numeric>
#include <algorithm>
using namespace std;

class PastingPaintingDivTwo
{
	public:
		long long countColors(vector <string> clipboard, int T);
};

long long PastingPaintingDivTwo::countColors(vector <string> clipboard, int T)
{
	int blacknumbers = 0,same = 0,i,j;
	for(i = 0; i < clipboard.size(); i++)
	{
		for(j = 0; j < clipboard[i].length(); j++)
		{
			if(clipboard[i][j] == 'B') blacknumbers ++;
		}
	}

	for(i = 1; i < clipboard.size(); i++)
	{
		for(j = 1; j < clipboard[i].length(); j++)
		{
			if(clipboard[i][j] == clipboard[i-1][j-1] && clipboard[i][j] == 'B') same++;
		}
	}

	long long numbers = blacknumbers * T - same * (T-1);
	return numbers;

}
int main()
{
	vector <string> clip;
	clip.push_back("bbb");
PastingPaintingDivTwo s;
 cout << s.countColors(clip,10000);



	return 0;
}



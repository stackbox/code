#include <iostream>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <string.h>
#include <vector>
#include <cmath>
#include <numeric>
#include <algorithm>

using namespace std;


class ApocalypseSomeday
{
	public:
		int getNth(int n);
};

int ApocalypseSomeday::getNth(int n)
{
	int x = 665;
	while(n > 0)
	{
		char str[10];
		sprintf(str,"%d",x);
		x++;
		string s = str;
		if(s.find("666",0) != string::npos) --n;
	}
	return x-1;
}


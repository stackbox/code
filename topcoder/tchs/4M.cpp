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

class CompositionTimeSignature
{
	public:
		string getTimeSignature(string duration);
};

string CompositionTimeSignature::getTimeSignature(string duration)
{
	int dura[50];
	int length = duration.length();
	for(int i = 0; i < length; i++)
	{
		switch(duration[i])
		{
			case 'W':
				dura[i] = 16;
				break;
			case 'H':
				dura[i] = 8;
				break;
			case 'Q':
				dura[i] = 4;
				break;
			case 'E':
				dura[i] = 2;
				break;
			case 'S':
				dura[i] = 1;
				break;
		}
	}
	int sum = 0;
	for(int i = 0; i < length; i++)
		sum += dura[i];
	int signature[4] = {6,8,12,16};
	int times = -1,flag = 0;

	for(int i = 0; i < 4; i++)
	{
		int cnt = 0;
		if(sum % signature[i] == 0)
		{
			int acc = 0;
			for(int j = 0 ; j < length; j++)
			{
				acc += dura[j];
				

				if( acc> signature[i])
				{
					cnt ++;
					acc %= signature[i];
				}

				if(acc % signature[i] == 0 ) 
				{
					acc = 0;
					continue;

				}
			}
			cout << "times:" << cnt << endl;
			if(cnt < times || times < 0)
			{
				times = cnt;
				flag = i;
			}
		}
	}
	if(times == -1) return "?/?";
	if(flag == 0) return "3/8";
	else if(flag == 1) return "2/4";
	else if(flag == 2) return "3/4";
	else if(flag == 3) return "4/4";
	else return "?/?";
}

int main()
{
CompositionTimeSignature s;
cout << s.getTimeSignature("W");


	return 0;
}



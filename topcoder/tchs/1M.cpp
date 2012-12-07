#include <iostream>
#include <sstream>
#include <stdlib.h>
#include <string.h>
#include <vector>
#include <numeric>
#include <cstring>
#include <cmath>
#include <algorithm>
using namespace std;



class SymbolFrequency
{
	public:
		double language(vector <string> frequencies, vector <string> text);
};

double SymbolFrequency::language(vector <string> frequencies, vector <string> text)
{
	int total = 0;
	int cnt[26] ;
	for(int i = 0 ; i < 26; i++)
		cnt[i] = 0;
	double dev, bestdev ;

	for(vector <string>::iterator iter = text.begin(); iter != text.end(); iter++)
	{
		string tmp = *iter;
		for(int i = 0; i < tmp.length(); i++)
		{
			char c = tmp[i];
			if(c >= 'a' && c <= 'z') {
				cnt[c-'a']++;
				total++;
			}
		}
	}
	bestdev = -1.0;
	for(vector <string>::iterator iter = frequencies.begin(); iter != frequencies.end(); iter++)
	{
		dev = 0.0;
		istringstream tmpStr(*iter);
		char ch;
		int per;
		
		double pre[26];
		for(int i = 0; i < 26; i++)
			pre[i] = 0;
		while(tmpStr >> ch >>per)
			pre[ch - 'a'] = total * per *1.0/100.0;
		for(int i = 0; i < 26; i++)
			dev += pow(cnt[i] - pre[i],2.0);
		if(bestdev < 0 || bestdev > dev)
			bestdev = dev;
	}
	return bestdev;
}


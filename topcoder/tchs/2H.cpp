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

string s,alph,best;
int bestpower;


class Wizarding
{
	public:
		static void solve(int depth,string c);
		string counterspell(string spell, string rules);
};

void Wizarding::solve(int depth,string c)
{
	if(depth == s.length())
	{
		if(c == "") return;

		int power = 1;
		for(int i = 0; i < c.length(); i++)
		{
			power *= (c[i] - 'A' + 1);
			power %= 77077;
		}

		if(power > bestpower) {
			bestpower = power;
			best = c;
		}
		else if(power == bestpower) {
			if(c.length() < best.length()) best = c;
			else if(c.length() == best.length() && c < best) best = c;
		}
	}
	else
	{
		solve(depth+1, c + s[depth]);

		solve(depth+1, c);

		if(alph[s[depth] - 'A'] != '-')
			solve(depth+1, c + alph[s[depth] - 'A']);
	}
}

string Wizarding::counterspell(string spell,string rules)
{
	s = spell;
	alph = rules;
	cout << alph << endl;
	bestpower = -1;
	solve(0,"");
	return best;
}


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


class FountainOfLife
{
	public:
		double elixirOfDeath(int elixir, int poison, int pool);
};

double FountainOfLife::elixirOfDeath(int elixir, int poison, int pool)
{
	if(poison <= elixir) return -1.0;
	else
	{
		double sec = pool * 1.0 / (poison  - elixir);
		return sec;
	}
}

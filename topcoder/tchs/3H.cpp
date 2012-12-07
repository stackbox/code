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


class BestDecomposition
{
	public:
		int maxProduct(int n);
};

int BestDecomposition::maxProduct(int n)
{
	int product = 1;
	while(n > 4)
	{
		product *= 3;
		product %= 10007;
		n -= 3;
	}
	product *= n;
	product %= 10007;
	return product;
}

int main()
{
	return 0;
}

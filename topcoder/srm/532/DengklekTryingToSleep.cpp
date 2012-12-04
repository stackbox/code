#include <vector>
#include <list>
#include <map>
#include <set>
#include <deque>
#include <stack>
#include <bitset>
#include <algorithm>
#include <functional>
#include <numeric>
#include <utility>
#include <sstream>
#include <iostream>
#include <iomanip>
#include <cstdio>
#include <cmath>
#include <cstdlib>
#include <ctime>

using namespace std;

class DengklekTryingToSleep {
public:
	int minDucks(vector <int>);
};

int DengklekTryingToSleep::minDucks(vector <int> ducks) {
	sort(ducks.begin(),ducks.end());
	return (ducks.back() - ducks.front() - ducks.size() + 1);
}


//Powered by [KawigiEdit] 2.0!

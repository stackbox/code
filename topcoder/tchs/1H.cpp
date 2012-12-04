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

int rows,cols;
bool data[52][52],visited[52][52];

class TroytownKeeper
{
	public:
		static void dfs(int x,int y);
		int limeLiters(vector <string> maze);
};


void TroytownKeeper::dfs(int x, int y)
{
	if(x < 0 || y < 0 || x >= rows || y >= cols || data[x][y] || visited[x][y]) return;
	visited[x][y] = true;
	dfs(x+1,y);
	dfs(x-1,y);
	dfs(x,y+1);
	dfs(x,y-1);
}
int TroytownKeeper::limeLiters(vector <string> maze) 
{
	rows = maze.size() + 2;
	cols = maze.front().length() + 2;

	string da[50];
	int pos = 0;
	for(vector <string>::iterator iter = maze.begin(); iter != maze.end(); iter++)
	{
		da[pos++] = *iter;
	}

	for(int i = 0; i < 52; i++)
		for(int j = 0; j < 52; j++)
		{
			data[i][j] = false;
			visited[i][j] = false;
		}

	for(int i = 0; i < rows - 2; i++)
		for(int j = 0; j < cols - 2; j++)
		{
			data[i+1][j+1] = (da[i][j] == '#');
		}

	dfs(0,0);
	int ans = 0;
	for(int i = 0; i < rows; i++)
		for(int j = 0; j < cols - 1; j++)
			if(visited[i][j] ^ visited[i][j+1]) ans++;
	
	for(int i = 0; i < rows-1; i++)
		for(int j = 0; j < cols; j++)
			if(visited[i][j] ^ visited[i+1][j]) ans++;
	return ans;
}



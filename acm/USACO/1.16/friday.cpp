/*
ID: xi-lin2
LANG: C++
PROG: friday
*/

#include <iostream>
#include <fstream>
#include <string>
using namespace std;
static int monthDays[12] = {31,28,31,30,31,30,31,31,30,31,30,31};
bool isPrimer(int year)
{
	if(year%4 == 0 && year%100 != 0 || year%400 == 0)
		return true;
	else return false;
}

int getSum(int years,int month)
{
	int sum = 0;
	for(int i = 0; i < years-1; i++)
	{
		if(isPrimer(1900+i))
			sum += 366;
		else sum += 365;
	}
	for(int i = 0; i < month - 1; i++)
	{
		sum += monthDays[i];
	}
	sum += 13;
	if(month > 2 && isPrimer(1900+years-1))
		sum ++;
	return sum;
}

int main()
{
    int years, counts[7];
    ifstream fin("friday.in");
	ofstream fout("friday.out");
	fin >> years;
	for(int i =0; i < 7; i++)
		counts[i] = 0;
	for(int i = 1; i <= years; i++)
	{
		for(int j = 1; j <= 12; j++)
		{
			int sum = getSum(i,j);
			counts[sum%7]++;
		}
	}
	fout << counts[6] << " " << counts[0];
	for(int i = 1; i <= 5; i++)
		fout << " " << counts[i];
	fout << endl;
	return 0;
}


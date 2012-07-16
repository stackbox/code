#include <iostream>
#include <sstream>
#include <stdio.h>
using namespace std;

int main()
{
    int s[7][12]={657,997,1,32,30,20,1,92,411,464,71,704,
	             88,56,78,775,4,109,2,881,803,660,91,969,
		     912,705,20,7,614,44,133,68,19,814,48,79,
		     69,565,394,9,14,43,86,16,76,544,220,93,
		     273,128,151,6,13,972,596,495,145,118,35,19,
		     151,67,529,96,44,70,466,614,517,18,745,323,
		     9,635,3,179,76,0,0,3,83,595,9,2};

    char row;
    int colum;
    string input;

    while(cin >> input)
    {
	istringstream in(input);
	in >> row >> colum;
	cout <<"value: " << s[row-'a'][colum-1] << endl<<endl;

    }
    return 0;
}

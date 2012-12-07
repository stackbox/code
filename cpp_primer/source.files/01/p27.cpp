#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main()
{
    ofstream outfile("out_file");
    ifstream infile("in_file");
    if(!infile) {
        cerr <<"Unable to open input file!\n";
        return -1;
    }
    if(!outfile) {
        cerr <<"Unable to open output file!\n";
        return -2;
    }
    
    string word;
    while(infile >> word) {
        outfile << word << ' ';
    }
    
    cin.get();
    return 0;
}

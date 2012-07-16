#include <iostream>
#include <string>
#include <vector>

#define DEBUG
using namespace std;

int main()
{
    #ifdef DEBUG
    cout << "Beginning execution of main()\n" ;
    #endif
    
    string word;
    vector< string > text;
    while( cin >> word )
    {
        #ifdef DEBUG
        cout << "word read: " << word << endl;
        #endif
        text.push_back( word);
    }
    
    cin.get();
    return 0;
}
    

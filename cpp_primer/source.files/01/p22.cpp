#include <iostream>
#include <cassert>
using namespace std;

int main()
{
    int element_count = 0;
    // __FILE__ 等宏前后的 下划线是两个 
    if(element_count == 0)
    cerr << "Error : "  << __FILE__
         <<" : Line : " << __LINE__
         << " element_count must be non-zero.\n";
    cout << "Date : " << __DATE__ << endl;
    cout << "TIME : " << __TIME__ << endl;
    
    int filename = 0;
    assert( filename != 0 );
    cin.get();
    return 0;
}

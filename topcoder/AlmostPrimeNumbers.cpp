// BEGIN CUT HERE
// PROBLEM STATEMENT
// An integer N greater than 1 is called almost prime if and only if the following conditions hold:

N is not prime.  In other words, it is divisible by some positive integer other than 1 and itself.
Each positive divisor of N (other than 1) is greater than 10.


Return the smallest almost prime number that is strictly greater than m.


DEFINITION
Class:AlmostPrimeNumbers
Method:getNext
Parameters:int
Returns:int
Method signature:int getNext(int m)


CONSTRAINTS
-m will be between 1 and 10^6, inclusive.


EXAMPLES

0)
200

Returns: 209

201 is divisible by 3, which is less than 10, so 201 is not almost prime.  202, 204, 206, and 208 are all divisible by 2.  203 is divisible by 7, 205 by 5, and 207 by 3.  So, the smallest almost prime number greater than 200 is 209 = 11*19.

1)
666

Returns: 667

667 = 23*29, so it's almost prime.

2)
1000

Returns: 1003

3)
1591

Returns: 1633

4)
6

Returns: 121

The smallest almost prime number is 11*11 = 121.

// END CUT HERE
#line 59 "AlmostPrimeNumbers.cpp"
#include <string>
#include <vector>
class AlmostPrimeNumbers {
	public:
	int getNext(int m) {
		
	}
};

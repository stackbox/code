def fac(n):
	if n < 0 : raise ValueError("factorial of a negative number is not defined")
	if type(n) != int : raise ValueError("argument is not an integer")
	if n == 0 : return 1
	if n == 1 : return 1
	return n*fac(n-1)

# alternative implementation
from functools import reduce
def fac(n):
	if n < 0 : raise ValueError("factorial of a negative number is not defined")
	if type(n) != int : raise ValueError("argument is not an integer")
	if n == 0 : return 1
	if n == 1 : return 1
	return reduce(lambda x,y:x*y,range(3,n+1))
	

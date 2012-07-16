#include <iostream>
#include <stdio.h>
using namespace std;

int Factorial(int n);

int main()
{
  printf("5! = %d\n",Factorial(5));
  getchar();
  return 0;
}



int Factorial(int n)
{
  if(n <= 1) return 1;
  else return n*Factorial(n-1);
}

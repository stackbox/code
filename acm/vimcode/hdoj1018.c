#include <stdio.h>
#include <math.h>
#define PI 3.1415926
#define nature 2.718281828

int main()
{
    int k,n;
    scanf("%d",&k);
    while(k--)
    {
	scanf("%d",&n);
	double s= n*log10(n*1.0/nature)+0.5*log10(2*PI*n) + 1.0;
	printf("%d\n",(int)s);
    }
    return 0;
}

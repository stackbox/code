#include <stdio.h>

int main()
{
    int i;
    double sum=2.5;
    int t=2;
    printf("n e\n");
    printf("- -----------\n");
    printf("0 1\n1 2\n2 2.5\n");
    for(i=3; i <=9; i++) {
	t *= i;
	sum += 1.0/t;
	printf("%d %.9lf\n",i,sum);
    }
    return 0;
}




#include <stdio.h>
#include <string.h>

long pro(long x) {
    long n=x,sum;
    while(n >= 10) {
	sum=0;
	while(n!=0) {
	    sum += n%10;
	    n /= 10;
	}
	n=sum;
    }
    return n;
}

int main()
{
    long sum,i;
    char s[1001];
    while(scanf("%s",s)!=EOF) {
	if(strcmp(s,"0")==0) break;
	for(i=0,sum=0;i < strlen(s); i++)
	{
	    sum += s[i]-'0';
	}
	printf("%d\n",pro(sum));
    }
    return 0;
}


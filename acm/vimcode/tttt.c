#include<stdio.h>
int main()
{
    int N,a,b,i=1;
    scanf("%d",&N);
    while(i<=N)
    {
        scanf("%d%d",&a,&b);
        printf("%d\n",a+b);
        ++i;
    }
}

#include<stdio.h>
int main()
{
    int N,total_time,floor,temp;
    while(scanf("%d",&N)!=EOF)
    {
        if(N==0)
        break;
                total_time=0;
        temp=0;
        while(N--)
        {

            scanf("%d",&floor);
            if(floor>temp)
            total_time+=(floor-temp)*6+5;
            else total_time+=(temp-floor)*4+5;
            temp=floor;
        }
        printf("%d\n",total_time);
    }
    return 0;

}


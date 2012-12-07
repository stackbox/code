#include <stdio.h>

int get_length(int n)
{
	int count  = 1;
	int n_tmp = n;
	while(n_tmp != 1) {
		if(n_tmp%2 == 0) n_tmp /= 2;
		else n_tmp = 3*n_tmp + 1;
		
		count ++; 
	}
	return count;
}

int main()
{
	int max,i,j,k;
	while(scanf("%d%d",&i,&j) != EOF) 
	{
		max = 0;
		int start = i > j ? j:i;
		int end   = i < j ? j:i;
		
		for (k = start; k <= end; k++)
		{
			int tmp = get_length(k);
			if (tmp > max) max = tmp;
		}
		printf("%d %d %d\n",i,j,max);
	}
	return 0;
}

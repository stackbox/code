# include <stdio.h>
void max(int x[],int n);

int main(void)
{
	int a[10];
	int *p = a;

	printf("ÇëÊäÈë10¸öÊı×Ö£º\n");
	for (p = a; p<a + 10; p++)
		scanf("%d", p);
	    printf("\n");
		max (a, 10);
           
		for (p = a; p<a + 10; p++)
			printf("%4d", *p);
		printf("\n");

		return 0;
}
		    

void max (int x[], int n)
{
	int i, j, t;
	for (j = 0; j<n-1; j++)
		for (i = 0; i<n -j-1 ; i++)
		{
			if (x[i]>x[i+1])
			{
				t = x[i];
				x[i] = x[i+1];
				x[i+1] = t;
			}
		}

}

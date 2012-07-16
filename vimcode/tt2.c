#include <stdio.h>
int main()
{
    char a = 0xfb;
    void *ptr = &a;
    printf("%x\n",*(unsigned char*)ptr);
    
    if((*(char *)ptr) != 0xfb)
	printf("ok\n");
    printf("%x\n",a);

    return 0;
}

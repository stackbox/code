%{
#include <stdio.h>
#include <stdlib.h>
%}
%%
[0-9] printf("shuzi");
[A-Za-z] printf("zimu");
%%
int yywrap(void) {
    return 1;
}

int main()
{
    yylex();
    return 0;
}


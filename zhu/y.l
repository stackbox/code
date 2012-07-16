%{
#include <stdio.h>
#include <stdlib.h>
#define CREATE
#define TABLE
#define ID
#define NUMBER
%}


%%

CREATE {printf("it is CREATE\n");return CREATE;}
TABLE  {printf("it is TABLE\n");return TABLE;}
[A-Za-z][A-Za-z0-9]* {printf("it is an ID\n");return ID;}
[0-9]+ {printf("it is a number\n");return NUMBER;}
"(" |
")" {printf("it is kuohao!\n");return yytext[0];}

%%

int yywrap()
{
    return 1;
}

int main(){
while(1){
yylex();
}
return 0;
}




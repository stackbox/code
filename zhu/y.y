
%{
#include <stdio.h>
#include <stdlib.h>
#define CREATE
#define TABLE
%}


%%

CREATE {return CREATE;}
TABLE  {return TABLE;}

%%

int main(){
yylex();
return 0;
}

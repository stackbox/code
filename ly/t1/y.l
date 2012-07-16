%{
#include "y.tab.h"
%}

%%
CREATE { return CREATE;}
TABLE  { return TABLE;}
CHAR   { return CHAR;}
INT    { return INT;}

[A-Za-z][A-Za-z0-9_]* {
    yylval.yych=(char *)malloc(strlen(yytext)+1);
    strcpy(yylval.yych,yytext);
    return ID;
	}
[0-9]+ {
    yylval.yych=(char *)malloc(strlen(yytext)+1);
    strcpy(yylval.yych,yytext);
    return NUMBER;
    	}
";"	|
"("	|
")"	|
","	{return yytex[0];}

%%


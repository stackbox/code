%{
enum TYPE {INT,CHAR};
struct Createfieldsdef {
	char *field;
	enum TYPE type;
	int lengh;
	struct Createfieldsdef *next_fdef;
	};

struct Createstruct{
	char *table;
	struct Createfieldsdef *fdef;
	};
%}

%union
{
	char *yych;
	struct Createfieldsdef *cfdef_var;
	struct Createstruct *cs_var;
}
%token CREATE TABLE CHAR INT ID NUMBER
%nonassoc <yych> table field type
%nonassoc <cfdef_var> fieldsdefinition field_type
%nonassoc <cs_var> createsql

%%


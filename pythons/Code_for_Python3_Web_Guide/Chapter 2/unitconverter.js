conversion_map = {
	"inch cm":1.0/2.54,
	"cm inch":2.54
};

$("button").button().click(function(){
		value=$("input[name='from']").val();
		f=$("select[name='tounit'] option:selected").val();
		t=$("select[name='fromunit'] option:selected").val();
		if(f != t){
			c=conversion_map[f+' '+t];
			result=parseFloat(value)*c;
		}else{
			result = value;
		}
		$("input[name='to']").val(result);
		//alert(c+'['+f+' '+t+']');
	}
);

$("form *").addClass("ui-widget");
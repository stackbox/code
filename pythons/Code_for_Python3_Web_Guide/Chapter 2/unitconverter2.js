function convert(button,cmap){
	var form = $(button).parent();
	var value = form.children("input[name='from']").val();
	var f = form.children("select[name='tounit']").children("option:selected").val();
	var t = form.children("select[name='fromunit']").children("option:selected").val();
	alert(value+' '+f+'_'+t);
	var result = value;
	if(f != t){
		var c=cmap[f+'_'+t];
		alert(c);
		result=parseFloat(value)*c;
		if (isNaN(result)){ 
			result = "unknown conversion factor"; 
		}else{
			result = result.toFixed(4);
		}
	}
	form.children("input[name='to']").val(result);
};


jQuery.fn.unitconverter = function(options){

	var cmap = $.extend({},$.fn.unitconverter.conversion_map,options);

	var from = new Array();
	var to = new Array();
	
	for (var key in cmap){
		var units = key.split("_");
		from.push(units[0]);
		to.push(units[1]);
	}
	
	var id = "unitconverter"+new String(Math.floor(Math.random() * 255 * 255));
	var html = '<form id="'+id+'"><input name="from" type="text" value="1" />';
	html += '<select name="fromunit">';
	html +=	'<option selected="true">'+from.pop()+'</option>';
	var len = from.length;
	for (var i=0; i<len; i++){ html += '<option>'+from.pop()+'</option>'};
	html += '</select> = ';
	html += '<input name="to" type="text" readonly="true" />';
	html += '<select name="tounit">';
	html +=	'<option selected="true">'+to.pop()+'</option>';
	var len = to.length;
	for (var i=0; i<len; i++){ html += '<option>'+to.pop()+'</option>'};
	html += '</select>';
	html += '<button name="convert" type="button">convert</button></form>';
	
	//alert(html);
	
	this.append(html);
	
	$("#"+id+" button").button({
			icons: {
				primary: 'ui-icon-refresh'
			},
			text: false
        }).click(function(){return convert(this,cmap);});
	$("#"+id).css('float','left');	
	$("#"+id).css('background-color',$("#"+id+" button").css('background-color'));	
	$("#"+id).css('background-image',$("#"+id+" button").css('background-image'));	
	$("#"+id).css('background-repeat',$("#"+id+" button").css('background-repeat'));	
	$("#"+id).addClass("ui-widget");
	
	return this;
};

jQuery.fn.unitconverter.conversion_map = {
	"inch_cm":1.0/2.54,
	"cm_inch":2.54
}

jQuery.fn.sheet = function(options){

	var opts = $.extend({},$.fn.sheet.defaults,options);

	/* private logging function */
	function log(s){
		$('#logging').append(s);
	}

	/* create a cols x rows grid */
	var t='<table class="sheet ui-helper-reset ui-widget" cellspacing="0">';
	t=t+'<thead class="ui-widget-header"><tr class="ui-helper-reset"><th></th>';
	for(i=0;i<opts.cols;i=i+1){
		t=t+'<th class="ui-helper-reset">'+String.fromCharCode(65+i)+"</th>";
	}
	t=t+'</tr></thead><tbody class="ui-widget-content" >';
	for(i=0;i<opts.rows;i=i+1){
		t=t+'<tr class="ui-helper-reset"><td class="rowindex ui-helper-reset ui-widget-header">'+(i+1)+"</td>";
		for(j=0;j<opts.cols;j=j+1){
			id=String.fromCharCode(65+j)+(i+1)
			t=t+'<td class="cell ui-helper-reset ui-widget-content" id="'+id+'"><span class="formula ui-helper-hidden"></span></td>';
			/* create a global variable */
			window[id]=0
		}
		t=t+"</tr>";
	}
	t=t+"</tbody></table>";
	this.append(t);
	
	function setvalue(value, settings) { 
		/* determine cell index and update global var */
		currentcell=$(this).attr( 'id');
		currentresult=eval(value);
		if (typeof(currentresult) == 'undefined'){
			currentresult='#undef';
			window[currentcell]=0;
		}else{
			window[currentcell]=currentresult;
		}
		/* update all other cells */
		var changed = false;
		var depth = 0;
		do{
			depth++;
			$('.sheet').find('.cell').each(function (index,element){
				cell=$(element).attr('id');
				if(currentcell != cell){
					span=$(element).children('span').first();
					orig = window[cell];
					window[cell]=0;
					formula=span.text();
					if(formula.length > 0){
						result=eval(formula);
						if (result != orig) { changed = true; }
						if (typeof(result) == 'undefined'){
							result='#undef';
						}else{
							window[cell]=result;
						}
					}else{
						result = ' ';
					}
					if(opts.logging){ log(depth+': '+cell+' '+formula+'='+result+'['+orig+']<br>'); }
					/* replaceWith() would replace the td element itself and using the text() function on the td remoces its span child (at least in IE8)*/
					$(element).empty().append('<span class="formula ui-helper-hidden replaced">'+formula+'</span>'+result);
					/*$(element).text(result);*/
				}
			});
		}while(changed && (depth < opts.cols*opts.rows));
		if ( depth >= opts.cols*opts.rows) currentresult = '#Circular!';
		return('<span class="formula ui-helper-hidden">'+value+'</span>'+currentresult);
	}

	function getvalue(org, settings){
		d=$(org)
		return d.filter(".formula").text()
	}

	/* make every cell editable with the jEditable plugin */
	this.find(".cell").each(function (index,element) {
		$(this).editable(setvalue,{type:'text',onblur:'cancel',data:getvalue})
	});

	$(".cell").css({'width':opts.width,'border-collapse':'collapse'});

	/* add some functions from the built-in Math object to global namespace */
	window['sin']= Math.sin;
	window['cos']= Math.cos;
	window['tan']= Math.tan;
	
	return this;
}

jQuery.fn.sheet.defaults = {
	rows : 4,
	cols : 4,
	width: '100px',
	logging: false
}

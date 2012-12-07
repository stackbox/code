$(function(){

$.ajaxSetup({cache:false,type:"GET"});
		
function shiftforms(rel){
		//alert('shiftforms called '+rel);
		$(".content form").each(function(i,e){
			//  alert('form '+$(e).attr('action')+'->'+rel+'/'+$(e).attr('action'));
			// necessary workaround because attr('action',val) fails on a form if it contains an input field with name=action
			$(e).get(0).setAttribute('action',rel+'/'+$(e).attr('action'));
			$('[type=submit]',e).bind('click',function(event){
				var f = $(this).parents('form');
				var n = $(this).attr('name');
				if (n != ''){ n = '&'+n+'='+$(this).attr('value');}
				$(".content").load(f.attr('action'), f.serialize()+n,function(){shiftforms(rel)});
				return false;
			});
		});
		$("button[name=first]").button({
            icons: {
                primary: "ui-icon-arrowthickstop-1-w"
			},	
			text: false
        });
		$("button[name=previous]").button({
            icons: {
                primary: "ui-icon-arrowthick-1-w"
			},	
			text: false
        });
		$("button[name=next]").button({
            icons: {
                primary: "ui-icon-arrowthick-1-e"
			},	
			text: false
        });
		$("button[name=last]").button({
            icons: {
                primary: "ui-icon-arrowthickstop-1-e"
			},	
			text: false
        });
		
		$("button[name=search]").button({
            icons: {
                primary: "ui-icon-search"
			},	
			text: false
        }).click(function(){
			$("input[name=pattern]",$(".content form").first()).remove();
			$("input[name=pattern]").each(function(i,e){
				var val=$(e).val();
				var col=$(e).next().text();
				$(".content form").first().append('<input type="hidden" name="pattern" value="'+col+','+val+'">');
			});
			$("button[name=first]").click(); // .submit() on form would trigger default, this is more explicit
		});
		
		$("button[name=clear]").button({
            icons: {
                primary: "ui-icon-refresh"
			},	
			text: false
        });
		$("button[name=addnew]").button({
            icons: {
                primary: "ui-icon-plus"
			},	
			text: false
        });
		
	};

function edit(rel,t){
		var id=$(t).attr('id');
		// this one points to the corrected relative url, e.g.  contacts/.
		var act=$(".content form").first().attr('action');
		act=act.replace(/\/\.$/,'/edit?id=')
		//alert('oink2!'+act+id);
		$(".content").load(act+id,function(){shiftforms(rel)});
	};
	
$(".navigation a").click(function (){
	//alert('click on entity');
	var rel = $(this).attr('href');
	
	// change action attributes of form elements
	$(".content").load($(this).attr('href'),function(){shiftforms(rel)});
	
	// create a named function in order to be able to remove it again by name
	function reledit(){edit(rel,this)};

	$("table.entitylist tr").die('dblclick');
	$("table.entitylist tr").live('dblclick',reledit);
	
	$("table.entitylist tr").die('click');
	$("table.entitylist tr").live('click',function(){
		$(this).toggleClass("ui-state-highlight").toggleClass("selected");
	});
	
	return false;
});

//alert('ok');
$(".notsorted").live('click',function(){
	//alert('notsorted '+$(this).text());
	$("input[name=sortorder]").remove();
	$(".content form").first().append('<input type="hidden" name="sortorder" value="'+$("div.colname",this).text()+',asc">');
	$("button[name=first]").click(); // .submit() on form would trigger default, this is more explicit
}).live('mouseenter mouseleave',function(){
	$(this).toggleClass("ui-state-highlight");
});
$(".sorted-asc").live('click',function(){
	//alert('sorted-asc '+$(this).text())
	$("input[name=sortorder]").remove();
	$(".content form").first().append('<input type="hidden" name="sortorder" value="'+$("div.colname",this).text()+',desc">');
	$("button[name=first]").click(); // .submit() on form would trigger default, this is more explicit
}).live('mouseenter mouseleave',function(){
	$(this).toggleClass("ui-state-highlight");
});
$(".sorted-desc").live('click',function(){
	//alert('sorted-desc '+$(this).text())
	$("button[name=clear]").click();
}).live('mouseenter mouseleave',function(){
	$(this).toggleClass("ui-state-highlight");
});

}); // end document ready function
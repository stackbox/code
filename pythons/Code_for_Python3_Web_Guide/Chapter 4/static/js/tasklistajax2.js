$.ajaxSetup({cache:false});

function itemmakeup(data,status,req){
		$(".done-button").button(  {icons: {primary: 'ui-icon-check'     }, text:false});
		$(".del-button").button(  {icons: {primary: 'ui-icon-trash'     }, text:false});
		$("#items input.duedate").sort(
			function(a,b){return $(a).val() > $(b).val() ? 1 : -1;},
			function(){ return this.parentNode; }).addClass("just-sorted");
		// disable input fields and done button on items that are already marked as completed
		$(".done .done-button").button( "option", "disabled", true );
		$(".done input").attr("disabled","disabled");
		$( "#items .editable-date" ).datepicker({ 
			dateFormat: $.datepicker.ISO_8601,
			onClose: function(dateText,datePicker){ if(dateText != ''){$(this).removeClass("inline-label");}} 
		});	
	};
	
	
$(document).ready(function(){
	$(".header").addClass("ui-widget ui-widget-header");
	$(".add-button").button(   {icons: {primary: 'ui-icon-plusthick' }, text:false}).click(function(){
        $(".inline-label").each(function() {
			if($(this).val() === $(this).attr('title')) {
				$(this).val('');
			};
        })
		var dd=$(this).siblings(".duedate").val();
		var ds=$(this).siblings(".description").val();
		$.get("add",{description:ds, duedate:dd},function(data,status,req){
			$("#items").load("list",itemmakeup);
		});
        return false; // prevent the normal action of the button click
    });
    $(".logoff-button").button({icons: {primary: 'ui-icon-closethick'}, text:false}).click(function(){
		location.href = $(this).val();
		return false;
	});
	$(".login-button").button( {icons: {primary: 'ui-icon-play'      }, text:false});
	$(":text").addClass("textinput");
	$(":password").addClass("textinput");
	$( ".editable-date" ).datepicker({ 
		dateFormat: $.datepicker.ISO_8601,
		onClose: function(dateText,datePicker){ if(dateText != ''){$(this).removeClass("inline-label");}} 
	});
	
	// give username field focus (only if it's there)
	$("#username").focus();
    
    
	$(".newitem input").addClass("ui-state-highlight");

	$(".done-button").live("click",function(){
			var item=$(this).siblings("[name='id']").val();
			var done=$(this).siblings(".completed").val();
			$.get("done",{id:item, completed:done},function(data,status,req){
				$("#items").load("list",itemmakeup);
			});
			return false;
		});
	
	$(".del-button").live("click",function(){
			var item=$(this).siblings("[name='id']").val();
			$.get("delete",{id:item},function(data,status,req){
				$("#items").load("list",itemmakeup);
			});
			return false;
    });
	
	$("#items").load("list",itemmakeup); // get the individual task items
	
	// have a go hero: refresh the list of tasks autonomically every minute
	// this way you may see changes made from elsewhere even if you leave your app running
	window.setInterval(function(){$("#items").load("list",itemmakeup);},6000);
	
});
$(document).ready(function(){
	$(".header").addClass("ui-widget ui-widget-header");
	//$(":submit").button();
	$(".add-button").button(   {icons: {primary: 'ui-icon-plusthick' }, text:false}).click(function(){
        $(".inline-label").each(function() {
			if($(this).val() === $(this).attr('title')) {
				$(this).val('');
			};
        })
        // note that we do not prevent propagation of the event so the normal submit still happens
    });
    // remove the disables attribute to ensure a submit can access the values of input fields
	$(".del-button").button(   {icons: {primary: 'ui-icon-trash'     }, text:false}).click(function(){
        $(this).siblings("input").removeAttr("disabled");
    });
	$(".done-button").button(  {icons: {primary: 'ui-icon-check'     }, text:false});
	$(".logoff-button").button({icons: {primary: 'ui-icon-closethick'}, text:false});
	$(".login-button").button( {icons: {primary: 'ui-icon-play'      }, text:false});
	$(":text").addClass("textinput");
	$(":password").addClass("textinput");
	$( ".editable-date" ).datepicker({ 
		//dateFormat: $.datepicker.ISO_8601,
		onClose: function(dateText,datePicker){ if(dateText != ''){$(this).removeClass("inline-label");}} 
	});
	
	// sort on duedate regardless of the dateFormat. targets all forms except the one with the add button
	// because we want to keep that one on the last line.
	$("#items form input.duedate").not("form.add input.duedate").sort(
		function(a,b){
			try {
				da=$.datepicker.parseDate($(a).datepicker('option','dateFormat'),$(a).val());
				db=$.datepicker.parseDate($(b).datepicker('option','dateFormat'),$(b).val());
				da > db ? -1 : 1 ;
				//alert(da+' '+db+' '+r); 
			}catch(e){
				return -1
			}},
		function(){ return this.parentNode; }).addClass("just-sorted");

    // give username field focus (only if it's there)
	$("#username").focus();
    
    // disable input fields and done button on items that are already marked as completed
    $(".done .done-button").button( "option", "disabled", true );
    $(".done input").attr("disabled","disabled");
	
	$(".add input").addClass("ui-state-highlight");

});
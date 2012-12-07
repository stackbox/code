$.ajaxSetup({cache:false,type:"GET"});

$("#wordsearch").live('submit',function(){ // submit event associated w. form, NOT button
	$("#content").load('searchwords',{'words':$("#wordsearch input").val()});
	return false; // prevent default
});
$("#tagsearch").live('submit',function(){
	$("#content").load('searchtags',{'tags':$("#tagsearch input").val()});
	return false;
});
$("#topicsearch").live('submit',function(){
	location.href="show?topic="+$("#topicsearch input").val();
	return false;
});
$("#tagcloud").load('tagcloud');

// autocomplete stuff
//
$("#topicsearch input").autocomplete({source:'gettopics',minLength:2});
// more involved, for comma separated lists, from demo : 
// http://jqueryui.com/demos/autocomplete/#multiple-remote
function split( val ) {
	return val.split( /,\s*/ );
}
function extractLast( term ) {
	return split( term ).pop();
}

$("#wordsearch input").autocomplete({
	source: function( request, response ) {
		$.getJSON( "getwords", {
			term: extractLast( request.term )
		}, response );
	},
	search: function() {
		// custom minLength
		var term = extractLast( this.value );
		if ( term.length < 2 ) {
			return false;
		}
	},
	focus: function() {
		// prevent value inserted on focus
		return false;
	},
	select: function( event, ui ) {
		var terms = split( this.value );
		// remove the current input
		terms.pop();
		// add the selected item
		terms.push( ui.item.value );
		// add placeholder to get the comma-and-space at the end
		terms.push( "" );
		this.value = terms.join( ", " );
		return false;
	}
});

$("#tagsearch input, #editarea input[name=tags]").autocomplete({
	source: function( request, response ) {
		$.getJSON( "gettags", {
			term: extractLast( request.term )
		}, response );
	},
	search: function() {
		// custom minLength
		var term = extractLast( this.value );
		if ( term.length < 2 ) {
			return false;
		}
	},
	focus: function() {
		// prevent value inserted on focus
		return false;
	},
	select: function( event, ui ) {
		var terms = split( this.value );
		// remove the current input
		terms.pop();
		// add the selected item
		terms.push( ui.item.value );
		// add placeholder to get the comma-and-space at the end
		terms.push( "" );
		this.value = terms.join( ", " );
		return false;
	}
});

// textarea functionality
$("#insertimage").click(function(){
	$("#imagedialog").dialog("open");
});

$.fn.setCursorPosition = function(pos) {
	if ($(this).get(0).setSelectionRange) {
	  $(this).get(0).setSelectionRange(pos, pos);
	} else if ($(this).get(0).createTextRange) {
	  var range = $(this).get(0).createTextRange();
	  range.collapse(true);
	  range.moveEnd('character', pos);
	  range.moveStart('character', pos);
	  range.select();
	}
};

$.fn.getCursorPosition = function() {
	var el = $(this)[0];
	if (el.selectionStart) { 
		return el.selectionStart; 
	} else if (document.selection) { 
		el.focus(); 

		var r = document.selection.createRange(); 
		if (r == null) { 
			return 0; 
		} 

		var re = el.createTextRange(), 
			rc = re.duplicate(); 
		re.moveToBookmark(r.getBookmark()); 
		rc.setEndPoint('EndToStart', re); 

		return rc.text.length; 
	}  
	return 0;
}

$(".selectable-image").live('click',function(){
	$("#imagedialog").dialog("close");

	var insert = "<" + $(this).attr("id").substring(3) + "," + $(this).attr("alt") + ">";
	
	var Area = $("#edittopic textarea");
	var area = Area[0];
	var oldposition = Area.getCursorPosition();
	
	//Break up the text around the cursor
	var pre  = area.value.substring(0, oldposition);
	var post = area.value.substring(oldposition);

	//Put the text in the textarea
	area.value = pre + insert + post;
 
	//Adjust the selection to point just after the inserted text
	Area.focus().setCursorPosition(oldposition + insert.length);
});
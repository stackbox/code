$.ajaxSetup({cache:false,type:"GET"});

function prepnavbar(response, status, XMLHttpRequest){
	$("#firstpage").button({
			text: false,
			icons: {
				primary: "ui-icon-seek-start"
			}
	});
	$("#previouspage").button({
			text: false,
			icons: {
				primary: "ui-icon-seek-prev"
			}
	});
	$("#mine").button({
			text: false,
			icons: {
				primary: "ui-icon-tag"
			}
	});
	$("#nextpage").button({
			text: false,
			icons: {
				primary: "ui-icon-seek-next"
			}
	});
	$("#lastpage").button({
			text: false,
			icons: {
				primary: "ui-icon-seek-end"
			}
	});
	$("#addbook").button({
			text: false,
			icons: {
				primary: "ui-icon-plusthick"
			}
	});
	t=$("#toolbar").buttonset();
	$("span",t).css({padding:"0px"});
	
	$(".bookrow:odd").addClass('oddline');
};

$("#booklist").load('/books/list',prepnavbar);

function getparams(){
	var m=0;
	// apparently the checked attr of a checkbox is magic: it returns true/false, not the contents!
	if ( $("#mine").attr("checked")==true ) { m = 1}
	return { offset:Number($("#firstid").text()),
	         limit:Number($("#limitid").text()),
			 pattern:$("#pattern").val(),
			 mine:m
		   };
};

$("#mine").live('click',function(){
	// this function is fired *after* the click toggled the checked attr
	var data = getparams();
	if (data.mine) { 
		$("#mine").removeAttr("checked");
	} else {
		$("#mine").attr("checked","yes");
	}
	$("#booklist").load('/books/list',data,prepnavbar);
	return true;
});

$("#firstpage").live('click',function(){
	var data = getparams();
	data.offset=0;
	$("#booklist").load('/books/list',data,prepnavbar);
	return true;
});
$("#previouspage").live('click',function(){
	var data = getparams();
	data.offset -= data.limit;
	if(data.offset<0){ data.offset=0;}
	$("#booklist").load('/books/list',data,prepnavbar);
	return true;
});
$("#nextpage").live('click',function(){
	var data = getparams();
	var n=Number($("#nids").text())
	data.offset += data.limit;
	if(data.offset>=n){ data.offset=n-data.limit;}
	if(data.offset<0){ data.offset=0;}
	$("#booklist").load('/books/list',data,prepnavbar);
	return true;
});
$("#lastpage").live('click',function(){
	var data = getparams();
	var n=Number($("#nids").text())
	data.offset = n-data.limit;
	if(data.offset<0){ data.offset=0;}
	$("#booklist").load('/books/list',data,prepnavbar);
	return true;
});
$("#pattern").live('keyup',function(event){
	if (event.keyCode == '13') {
		event.preventDefault();
		data = getparams();
		data.offset=0;
		$("#booklist").load('/books/list',data,prepnavbar);
	}
	return true;
});
$("#addbook").live('click',function(){
	window.location.href="/books/addbook";
	return true;
});

// this part applies to addbook elements only
$(".buttonbar").buttonset();
$("#newbook button[name=submit]").button({
			text: false,
			icons: {
				primary: "ui-icon-plusthick"
			}
});
$("#newbook button[name=cancel]").button({
			text: false,
			icons: {
				primary: "ui-icon-trash"
			}
});


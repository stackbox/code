var xmlHttp

function showStu(str)
{
if(len(str) < 8) {
	document.getElementById("txtHint").innerHTML="<p>学号长度过短</p>"
	return
}else if(len(str) > 8) {
	document.getElementById("txtHint").innerHTML="<p>学号长度过长</p>"
} else if(len(str) == 8){
	document.getElementById("txtHint").innerHTML=""
	xmlHttp=GetXmlHttpObject()
	xmlHttp.onreadystatechange=stateChanged
	var url="getstu.php?q="+str
	
	url=url+"&sid="+Math.random()
	xmlHttp.open("GET",url,true);
	xmlHttp.send();

}

}

function len(s) { 
	var l = 0; 
	var a = s.split(""); 
	for (var i=0;i<a.length;i++) { 
	if (a[i].charCodeAt(0)<299) { 
	l++; 
	} else { 
	l+=2; 
	} 
	} 
return l; 
}

function stateChanged()
{
	if(xmlHttp.readyState==4 && xmlHttp.status==200)
	{
	document.getElementById("txtHint").innerHTML=xmlHttp.responseText;
	}
}

function GetXmlHttpObject()
{
var xmlhttp;
if (window.XMLHttpRequest)
  {// code for IE7+, Firefox, Chrome, Opera, Safari
  xmlhttp=new XMLHttpRequest();
  //alert("success create")
  }
else
  {// code for IE6, IE5
  xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
  }
  return xmlhttp;
}
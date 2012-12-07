	
	//functions.js
	
	//Create a boolean variable to check for a valid IE instance.
	var xmlhttp = false;
	
	//Check if we are using IE.
	try {
		//If the javascript version is greater than 5.
		xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
	} catch (e) {
		//If not, then use the older active x object.
		try {
			//If we are using IE.
			xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
		} catch (E) {
			//Else we must be using a non-IE browser.
			xmlhttp = false;
		}
	}
	
	//If we are using a non-IE browser, create a JavaScript instance of the object.
	if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
		xmlhttp = new XMLHttpRequest();
	}
	
	//A variable used to distinguish whether to open or close the calendar.
	var showCalendar = true;
	
	function showHideCalendar() {
		
		//The location we are loading the page into.
		var objID = "calendar";
		
		//Change the current image of the minus or plus.
		if (showCalendar == true){
			//Show the calendar.
			document.getElementById("opencloseimg").src = "images/mins.gif";
			//The page we are loading.
			var serverPage = "calendar.php";
			//Set the open close tracker variable.
			showCalendar = false;
			
			var obj = document.getElementById(objID);
			xmlhttp.open("GET", serverPage);
			xmlhttp.onreadystatechange = function() {
				if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
					obj.innerHTML = xmlhttp.responseText;
				}
			}
			xmlhttp.send(null);
		} else {
			//Hide the calendar.
			document.getElementById("opencloseimg").src = "images/plus.gif";
			showCalendar = true;
			
			document.getElementById(objID).innerHTML = "";
		}
		
		
	}
	
	function createform (e){
		
		theObject = document.getElementById("createtask");
		
		theObject.style.visibility = "visible";
		theObject.style.height = "200px";
		theObject.style.width = "200px";
		
		var posx = 0;
		var posy = 0;
		
		posx = e.clientX + document.body.scrollLeft;
		posy = e.clientY + document.body.scrollTop;
		
		theObject.style.left = posx + "px";
		theObject.style.top = posy + "px";
		
		//The location we are loading the page into.
		var objID = "createtask";
		var serverPage = "theform.php";
		
		var obj = document.getElementById(objID);
		xmlhttp.open("GET", serverPage);
		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
				obj.innerHTML = xmlhttp.responseText;
			}
		}
		xmlhttp.send(null);
		
	}
		
	function closetask (){
		
		theObject = document.getElementById("createtask");
		
		theObject.style.visibility = "hidden";
		theObject.style.height = "0px";
		theObject.style.width = "0px";
		
		acObject = document.getElementById("autocompletediv");
		
		acObject.style.visibility = "hidden";
		acObject.style.height = "0px";
		acObject.style.width = "0px";
	}
	
	function findPosX(obj){
		var curleft = 0;
		if (obj.offsetParent){
			while (obj.offsetParent){
				curleft += obj.offsetLeft
				obj = obj.offsetParent;
			}
		} else if (obj.x){
			curleft += obj.x;
		}
		return curleft;
	}
	
	function findPosY(obj){
		var curtop = 0;
		if (obj.offsetParent){
			while (obj.offsetParent){
				curtop += obj.offsetTop
				obj = obj.offsetParent;
			}
		} else if (obj.y){
			curtop += obj.y;
		}
		return curtop;
	}
	
	function autocomplete (thevalue, e){
		
		theObject = document.getElementById("autocompletediv");
		
		theObject.style.visibility = "visible";
		theObject.style.width = "152px";
		
		var posx = 0;
		var posy = 0;
		
		posx = (findPosX (document.getElementById("yourname")) + 1);
		posy = (findPosY (document.getElementById("yourname")) + 23);
		
		theObject.style.left = posx + "px";
		theObject.style.top = posy + "px";
		
		var theextrachar = e.which;
		
		if (theextrachar == undefined){
			theextrachar = e.keyCode;
		}
		
		//The location we are loading the page into.
		var objID = "autocompletediv";

		//Take into account the backspace.
		if (theextrachar == 8){
			if (thevalue.length == 1){
				var serverPage = "autocomp.php";
			} else {
				var serverPage = "autocomp.php" + "?sstring=" + thevalue.substr (0, (thevalue.length -1));
			}
		} else {
			var serverPage = "autocomp.php" + "?sstring=" + thevalue + String.fromCharCode (theextrachar);
		}
		
		var obj = document.getElementById(objID);
		xmlhttp.open("GET", serverPage);
		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
				obj.innerHTML = xmlhttp.responseText;
			}
		}
		xmlhttp.send(null);
	}
	
	function setvalue (thevalue){
		acObject = document.getElementById("autocompletediv");
		
		acObject.style.visibility = "hidden";
		acObject.style.height = "0px";
		acObject.style.width = "0px";
		
		document.getElementById("yourname").value = thevalue;
	}
	
	function validateform (thevalue){
		
		serverPage = "validator.php?sstring=" + thevalue;
		objID = "messagebox";
		
		var obj = document.getElementById(objID);
		xmlhttp.open("GET", serverPage);
		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
				obj.innerHTML = xmlhttp.responseText;
			}
		}
		xmlhttp.send(null);
	}
	
	function checkfortasks (thedate, e){
		
		theObject = document.getElementById("taskbox");
		
		theObject.style.visibility = "visible";
		
		var posx = 0;
		var posy = 0;
		
		posx = e.clientX + document.body.scrollLeft;
		posy = e.clientY + document.body.scrollTop;
		
		theObject.style.left = posx + "px";
		theObject.style.top = posy + "px";
		
		serverPage = "taskchecker.php?thedate=" + thedate;
		objID = "taskbox";
		
		var obj = document.getElementById(objID);
		xmlhttp.open("GET", serverPage);
		xmlhttp.onreadystatechange = function() {
			if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
				obj.innerHTML = xmlhttp.responseText;
			}
		}
		xmlhttp.send(null);
	}
	
	function hidetask (){
		tObject = document.getElementById("taskbox");
		
		tObject.style.visibility = "hidden";
		tObject.style.height = "0px";
		tObject.style.width = "0px";
	}
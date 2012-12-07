<?php

	//validator.php

	//Add in our database connector.
	require_once ("dbconnector.php");
	//And open a database connection.
	$db = opendatabase();
	
	//Setup the dynamic query string.
	$querystr = "SELECT userid FROM user WHERE name = LOWER('" . mysql_real_escape_string ($_GET['sstring']) . "')";
	
	if ($userquery = mysql_query ($querystr)){
		if (mysql_num_rows ($userquery) == 0){
			//Then return with an error.
			?><span style="color: #FF0000;">Name not found...</span><?php	
		} else {
			//At this point we would go to the processing script.
			?><span style="color: #FF0000;">Form would now submit...</span><?php
		}
	} else {
		echo mysql_error();
	}
		
?>
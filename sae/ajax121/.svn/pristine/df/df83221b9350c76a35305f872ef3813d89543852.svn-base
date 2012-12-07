<?php

	//wordgrabber.php
	
	//Require in the database connection.
	require_once ("dbconnector.php");
	//Open the database.
	$db = opendatabase();
	
	//Then perform a query to grab a random word from our database.
	$querystr = "SELECT content FROM block ORDER BY RAND() LIMIT 1";
	
	if ($myquery = mysql_query ($querystr)){
		$mydata = mysql_fetch_array ($myquery);
		echo $mydata['content'];
	} else {
		echo mysql_error();
	}
	
?>
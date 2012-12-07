<?php

	//dbconnector.php

	//Define the mysql connection variables.
	define ("MYSQLHOST", "localhost");
	define ("MYSQLUSER", "apressauth");
	define ("MYSQLPASS", "tasks");
	define ("MYSQLDB", "taskdb");
	
	function opendatabase(){
		$db = mysql_connect (MYSQLHOST,MYSQLUSER,MYSQLPASS);
		try {
			if (!$db){
				$exceptionstring = "Error connection to database: <br />";
				$exceptionstring .= mysql_errno() . ": " . mysql_error();
				throw new exception ($exceptionstring);
			} else {
				mysql_select_db (MYSQLDB,$db);
			}
			return $db;
		} catch (exception $e) {
			echo $e->getmessage();
			die();
		}
	}
	
?>
<?php

	//taskchecker.php

	//Add in the database connector.
	require_once ("dbconnector.php");
	//Open the database.
	$db = opendatabase();
	
	//Setup the dynamic query string.
	$querystr = "SELECT description FROM task WHERE thedate='" . addslashes ($_GET['thedate']) . "'";
	
	if ($datequery = mysql_query ($querystr)){
		if (mysql_num_rows ($datequery) > 0){
			?>
			<div style="width: 150px; background: #FFBC37; border-style: solid; border-color: #000000; border-width: 1px;">
				<div style="padding: 10px;">
					<?php
						while ($datedata = mysql_fetch_array ($datequery)){
							if (!get_magic_quotes_gpc()){
								echo stripslashes ($datedata['description']);
							} else {
								echo $datedata['description'];
							}
						}
					?>
				</div>
			</div>
			<?php
		}
	} else {
		echo mysql_error();
	}
	
	//Close the database connection.
	mysql_close ($db);
	
?>
<?php

	//autocomp.php

	//Add in our database connector.
	require_once ("dbconnector.php");
	//And open a database connection.
	$db = opendatabase();
	
	$foundarr = array ();
	
	//Setup the dynamic query string.
	$querystr = "SELECT name FROM user WHERE name LIKE LOWER('%" . mysql_real_escape_string ($_GET['sstring']) . "%') ORDER BY name ASC";
	
	if ($userquery = mysql_query ($querystr)){
		while ($userdata = mysql_fetch_array ($userquery)){
			if (!get_magic_quotes_gpc()){
				$foundarr[] = stripslashes ($userdata['name']);
			} else {
				$foundarr[] = $userdata['name'];
			}
		}
	} else {
		echo mysql_error();
	}
	
	//If we have any matches, then we can go through and display them.
	if (count ($foundarr) > 0){
		?>
		<div style="background: #CCCCCC; border-style: solid; border-width: 1px; border-color: #000000;">
			<?php
				for ($i = 0; $i < count ($foundarr); $i++){
					?><div style="padding: 4px; height: 14px;" onmouseover="this.style.background = '#EEEEEE'" onmouseout="this.style.background = '#CCCCCC'" onclick="setvalue ('<?php echo $foundarr[$i]; ?>')"><?php echo $foundarr[$i]; ?></div><?php
				}
			?>
		</div>
		<?php
	}
	
?>
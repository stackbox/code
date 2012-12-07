<?php

	//validator.php

	//A list of valid names.
	//Again, this would usually come from a database.
	$names = array ("Lee Babin","Joe Smith","John Doe");
	
	if (!in_array (strtolower ($_GET['sstring']), strtolower ($names))){
		//Then return with an error.
		?><span style="color: #FF0000;">Name not found...</span><?php
	} else {
		//At this point we would go to the processing script.
		?><span style="color: #FF0000;">Form would now submit...</span><?php
	}
?>
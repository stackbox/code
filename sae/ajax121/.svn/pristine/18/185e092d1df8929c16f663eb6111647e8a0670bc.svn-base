<?php
	
	//autocomp.php	

	//A list of all names.
	//Generally this would be in a database of some sort.
	$names = array ("Lee Babin","Joe Smith","John Doe");
	$foundarr = array ();
	
	//Go through the names array and load any matches into the foundarr array.
	if ($_GET['sstring'] != ""){
		for ($i = 0; $i < count ($names); $i++){
			if (substr_count (strtolower ($names[$i]), strtolower ($_GET['sstring'])) > 0){
				$foundarr[] = $names[$i];
			}
		}
	}
	
	//If we have any matches.
	if (count ($foundarr) > 0){
		//Then display them.
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
<?php

	//taskchecker.php
	
	//Actual Task dates.
	//This would normally be loaded from a database.
	$tasks = array ("2005-11-10" => 'Check mail.',"2005-11-20" => 'Finish Chapter 3');
	
	$outputarr = array ();
	
	//Run through and check for any matches.
	while ($ele = each ($tasks)){
		if ($ele['key'] == $_GET['thedate']){
			$outputarr[] = $ele['value'];
		}
	}
	
	//If we have any matches...
	if (count ($outputarr) > 0){
		?>
		<div class="taskchecker">
			<div class="tcpadding">
				<?php
					for ($i = 0; $i < count ($outputarr); $i++){
						echo $outputarr[$i] . "<br />";
					}
				?>
			</div>
		</div>
		<?php
	}
?>
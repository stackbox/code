<?php

	//calendar.php

	//Check if the month and year values exist
	if ((!$_GET['month']) && (!$_GET['year'])) {
		$month = date ("n");
		$year = date ("Y");
	} else {
		$month = $_GET['month'];
		$year = $_GET['year'];
	}
	
	//Calculate the viewed month
	$timestamp = mktime (0, 0, 0, $month, 1, $year);
	$monthname = date("F", $timestamp);

	//Now let's create the table with the proper month
	?>
	<table style="width: 105px; border-collapse: collapse;" border="1" cellpadding="3" cellspacing="0" bordercolor="#000000">
		<tr style="background: #FFBC37;">
		<td colspan="7" style="text-align: center;" onmouseover="this.style.background='#FECE6E'" onmouseout="this.style.background='#FFBC37'">
			<span style="font-weight: bold;"><?php echo $monthname . " " .  $year; ?></span>
		</td>
		</tr>
		<tr style="background: #FFBC37;">
		<td style="text-align: center; width: 15px;" onmouseover="this.style.background='#FECE6E'" onmouseout="this.style.background='#FFBC37'">
			<span style="font-weight: bold;">Su</span>
		</td>
		<td style="text-align: center; width: 15px;" onmouseover="this.style.background='#FECE6E'" onmouseout="this.style.background='#FFBC37'">
			<span style="font-weight: bold;">M</span>
		</td>
		<td style="text-align: center; width: 15px;" onmouseover="this.style.background='#FECE6E'" onmouseout="this.style.background='#FFBC37'">
			<span style="font-weight: bold;">Tu</span>
		</td>
		<td style="text-align: center; width: 15px;" onmouseover="this.style.background='#FECE6E'" onmouseout="this.style.background='#FFBC37'">
			<span style="font-weight: bold;">W</span>
		</td>
		<td style="text-align: center; width: 15px;" onmouseover="this.style.background='#FECE6E'" onmouseout="this.style.background='#FFBC37'">
			<span style="font-weight: bold;">Th</span>
		</td>
		<td style="text-align: center; width: 15px;" onmouseover="this.style.background='#FECE6E'" onmouseout="this.style.background='#FFBC37'">
			<span style="font-weight: bold;">F</span>
		</td>
		<td style="text-align: center; width: 15px;" onmouseover="this.style.background='#FECE6E'" onmouseout="this.style.background='#FFBC37'">
			<span style="font-weight: bold;">Sa</span>
		</td>
		</tr>
		<?php				
			$monthstart = date("w", $timestamp);
			//if ($monthstart == 0){
				//$monthstart = 7;
			//}
			$lastday = date("d", mktime (0, 0, 0, $month + 1, 0, $year));
			$startdate = -$monthstart;

			//Figure out how many rows we need.
			$numrows = ceil (((date("t",mktime (0, 0, 0, $month + 1, 0, $year)) + $monthstart) / 7));
			
			//Let's make an appropriate number of rows...
			for ($k = 1; $k <= $numrows; $k++){
				?><tr><?php
				//Use 7 columns (for 7 days)...
				for ($i = 0; $i < 7; $i++){
					$startdate++;
					if (($startdate <= 0) || ($startdate > $lastday)){
						//If we have a blank day in the calendar.
						?><td style="background: #FFFFFF;">&nbsp;</td><?php
					} else {
																
						if ($startdate == date("j") && $month == date("n") && $year == date("Y")){
							?><td onclick="createform(event)" style="text-align: center; background: #FFBC37;" onmouseover="this.style.background='#FECE6E'; checkfortasks ('<?php echo $year . "-" . $month . "-" . $startdate; ?>',event);" onmouseout="this.style.background='#FFBC37'; hidetask();"><?php echo date ("j"); ?></td><?php
						} else {
							?><td onclick="createform(event)" style="text-align: center; background: #A2BAFA;" onmouseover="this.style.background='#CAD7F9'; checkfortasks ('<?php echo $year . "-" . $month . "-" . $startdate; ?>',event);" onmouseout="this.style.background='#A2BAFA'; hidetask();"><?php echo $startdate; ?></td><?php
						}
					}
				}
				?></tr><?php
			}
		?>				
	</table>
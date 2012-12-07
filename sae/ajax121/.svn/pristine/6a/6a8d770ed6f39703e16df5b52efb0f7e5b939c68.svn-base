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
		<tr>
		<td colspan="7" class="calendartodayoff" onmouseover="this.className='calendartodayover'" onmouseout="this.className='calendartodayoff'">
			<span style="font-weight: bold;"><?php echo $monthname . " " .  $year; ?></span>
		</td>
		</tr>
		<tr>
		<td class="calendartodayoff" onmouseover="this.className='calendartodayover'" onmouseout="this.className='calendartodayoff'">
			<span style="font-weight: bold;">Su</span>
		</td>
		<td class="calendartodayoff" onmouseover="this.className='calendartodayover'" onmouseout="this.className='calendartodayoff'">
			<span style="font-weight: bold;">M</span>
		</td>
		<td class="calendartodayoff" onmouseover="this.className='calendartodayover'" onmouseout="this.className='calendartodayoff'">
			<span style="font-weight: bold;">Tu</span>
		</td>
		<td class="calendartodayoff" onmouseover="this.className='calendartodayover'" onmouseout="this.className='calendartodayoff'">
			<span style="font-weight: bold;">W</span>
		</td>
		<td class="calendartodayoff" onmouseover="this.className='calendartodayover'" onmouseout="this.className='calendartodayoff'">
			<span style="font-weight: bold;">Th</span>
		</td>
		<td class="calendartodayoff" onmouseover="this.className='calendartodayover'" onmouseout="this.className='calendartodayoff'">
			<span style="font-weight: bold;">F</span>
		</td>
		<td class="calendartodayoff" onmouseover="this.className='calendartodayover'" onmouseout="this.className='calendartodayoff'">
			<span style="font-weight: bold;">Sa</span>
		</td>
		</tr>
		<?php				
			$monthstart = date("w", $timestamp);
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
							?><td onclick="createform(event)" class="calendartodayoff" onmouseover="this.className='calendartodayover'; checkfortasks ('<?php echo $year . "-" . $month . "-" . $startdate; ?>',event);" onmouseout="this.className='calendartodayoff'; hidetask();"><?php echo date ("j"); ?></td><?php
						} else {
							?><td onclick="createform(event)" class="calendaroff" onmouseover="this.className='calendarover'; checkfortasks ('<?php echo $year . "-" . $month . "-" . $startdate; ?>',event);" onmouseout="this.className='calendaroff'; hidetask();"><?php echo $startdate; ?></td><?php
						}
					}
				}
				?></tr><?php
			}
		?>				
	</table>
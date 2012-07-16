<?php
$con = mysql_connect(SAE_MYSQL_HOST_M.':'.SAE_MYSQL_PORT,SAE_MYSQL_USER,SAE_MYSQL_PASS);
if (!$con)
 {
 die('Could not connect: ' . mysql_error());
 }
 else
 {
 echo "succeed connect";
 }
 $db_select=mysql_select_db("app_ajax121",$con);
 if(!$db_select)
 {
 die('error');
 }
 else
 {
 echo "<br/>";
 echo "succeed selected";
 }
 
 $sno = _GET["q"];
 $result = mysql_query("SELECT * FROM St WHERE sno=".$sno);
 if(!$result)
 {
 echo "<br/>error";
 echo "result error";
 }
 else
 {
 echo "success";
 }
 mysql_close($con);

?>
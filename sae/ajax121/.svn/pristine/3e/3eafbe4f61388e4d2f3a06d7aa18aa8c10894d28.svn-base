<?php
$a[]="Anna";
$a[]="Birttany";
$a[]="Cinderella";
$a[]="Diana";
$a[]="Eva";
$a[]="Inga";
$a[]="Amanda";
$a[]="Raquel";
$a[]="Cindy";
$a[]="Doris";
$a[]="Eve";
$a[]="Evita";
$a[]="Sunniva";
$a[]="Tove";
$a[]="Unni";
$a[]="Violet";
$a[]="Liza";
$a[]="Elizabeth";
$a[]="Ellen";
$a[]="Wenche";
$a[]="Vicky";

$q=$_GET["q"];
if(strlen($q) > 0)
{
$hint="";
for($i=0;$i<count($a);$i++)
{
if(strtolower($q)==strtolower(substr($a[$i],0,strlen($q))))
{
if($hint=="")
{
$hint=$a[$i];
}
else
{
$hint=$hint." ,".$a[$i];
}
}
}
}


if($hint =="")
{
$response="no suggestion";
}
else
{
$response=$hint;
}
echo $response;
?>
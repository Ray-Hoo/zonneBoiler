<?php

function mysqli_result($res,$row=0,$col=0){
    $numrows = mysqli_num_rows($res);
    if ($numrows && $row <= ($numrows-1) && $row >=0){
        mysqli_data_seek($res,$row);
        $resrow = (is_numeric($col)) ? mysqli_fetch_row($res) : mysqli_fetch_assoc($res);
        if (isset($resrow[$col])){
            return $resrow[$col];
        }
    }
    return false;
}

$username="username";
$password="password";
$database="temperatuur_database";

$con=mysqli_connect('ip-adres:poortnummer',$username,$password);

if (mysqli_connect_errno()) {
  echo "Failed to connect to the SQL-database: " . mysqli_connect_error();
  exit;
}

mysqli_select_db($con,$database) or die( "Unable to select the database");

$query="SELECT * FROM tempLog ORDER BY tempLog.datetime DESC LIMIT 1";
$result=mysqli_query($con,$query);

$num=mysqli_fetch_row($result)[0];

mysqli_close($con);


        $dateAndTemps = array();
        $datetime = mysqli_result($result,0,"datetime");
        $temperature = mysqli_result($result,0,"temperature");

        $dateAndTemps["Date"] = $datetime;
        $dateAndTemps["Temperature"] = $temperature;

        $tempValues=$dateAndTemps;

header('Content-Type: application/json');
echo json_encode($tempValues);

?>
